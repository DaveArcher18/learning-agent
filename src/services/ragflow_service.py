"""
RAGFlow Service Module

Manages RAGFlow Docker container lifecycle, health monitoring, and knowledge base operations
optimized for mathematical content processing with BGE-M3 integration.

This module focuses on:
- RAGFlow Docker container management  
- Health checks and service monitoring
- Knowledge base lifecycle management
- Document upload and indexing orchestration
- Mathematical content optimization
"""

import logging
import time
import subprocess
import requests
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import json
import docker
from pathlib import Path

from src.core.config import ConfigManager

logger = logging.getLogger(__name__)

class RAGFlowStatus(Enum):
    """RAGFlow service status states"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    ERROR = "error"

@dataclass
class KnowledgeBaseInfo:
    """Knowledge base information structure"""
    id: str
    name: str
    description: str
    chunk_count: int
    document_count: int
    embedding_model: str
    created_at: str
    mathematical_optimized: bool = False

@dataclass
class DocumentInfo:
    """Document information structure"""
    id: str
    name: str
    size: int
    status: str
    chunks: int
    upload_time: str
    processing_time: Optional[float] = None
    mathematical_content: bool = False

class RAGFlowServiceError(Exception):
    """Custom exception for RAGFlow service errors"""
    def __init__(self, message: str, service_status: str = None):
        self.service_status = service_status
        super().__init__(message)

class RAGFlowService:
    """
    RAGFlow service management with mathematical content optimization.
    
    Features:
    - Docker container lifecycle management
    - Health monitoring and automatic recovery
    - Knowledge base operations optimized for BGE-M3
    - Document processing with mathematical content support
    - Performance monitoring and optimization
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize RAGFlow service.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.docker_client = None
        self.base_url = self.config.get("ragflow.api.base_url", "http://localhost:9380")
        self.api_key = self.config.get("ragflow.api.key", "")
        self.container_name = self.config.get("ragflow.docker.container_name", "ragflow-server")
        self.compose_file = self.config.get("ragflow.docker.compose_file", "docker-compose.ragflow.yml")
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker client initialized for RAGFlow management")
        except Exception as e:
            logger.error("Failed to initialize Docker client", extra={"error": str(e)})
        
        # Health check configuration
        self.health_check_interval = self.config.get("ragflow.health.check_interval", 30)
        self.max_startup_time = self.config.get("ragflow.health.max_startup_time", 300)
        
        logger.info("RAGFlow service initialized", extra={
            "base_url": self.base_url,
            "container_name": self.container_name,
            "health_check_interval": self.health_check_interval
        })
    
    def start_service(self, force_rebuild: bool = False) -> bool:
        """
        Start RAGFlow service using Docker Compose.
        
        Args:
            force_rebuild: Whether to force rebuild containers
            
        Returns:
            bool: True if service started successfully
        """
        try:
            logger.info("Starting RAGFlow service", extra={"force_rebuild": force_rebuild})
            
            # Build command
            cmd = ["docker-compose", "-f", self.compose_file, "up", "-d"]
            if force_rebuild:
                cmd.extend(["--build", "--force-recreate"])
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=self.max_startup_time
            )
            
            if result.returncode != 0:
                logger.error(
                    "Failed to start RAGFlow service",
                    extra={"error": result.stderr, "stdout": result.stdout}
                )
                return False
            
            # Wait for service to be healthy
            if self._wait_for_healthy_status():
                logger.info("RAGFlow service started successfully")
                return True
            else:
                logger.error("RAGFlow service failed to become healthy")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("RAGFlow service startup timed out")
            return False
        except Exception as e:
            logger.error("Error starting RAGFlow service", extra={"error": str(e)})
            return False
    
    def stop_service(self) -> bool:
        """
        Stop RAGFlow service.
        
        Returns:
            bool: True if service stopped successfully
        """
        try:
            logger.info("Stopping RAGFlow service")
            
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "down"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("RAGFlow service stopped successfully")
                return True
            else:
                logger.error(
                    "Failed to stop RAGFlow service",
                    extra={"error": result.stderr}
                )
                return False
                
        except Exception as e:
            logger.error("Error stopping RAGFlow service", extra={"error": str(e)})
            return False
    
    def restart_service(self) -> bool:
        """
        Restart RAGFlow service.
        
        Returns:
            bool: True if service restarted successfully
        """
        logger.info("Restarting RAGFlow service")
        
        if self.stop_service():
            time.sleep(5)  # Brief pause
            return self.start_service()
        return False
    
    def get_service_status(self) -> RAGFlowStatus:
        """
        Get current RAGFlow service status.
        
        Returns:
            RAGFlowStatus: Current service status
        """
        try:
            # Check Docker container status
            if not self.docker_client:
                return RAGFlowStatus.ERROR
            
            try:
                container = self.docker_client.containers.get(self.container_name)
                container_status = container.status
                
                if container_status == "running":
                    # Check if API is responding
                    if self._check_api_health():
                        return RAGFlowStatus.HEALTHY
                    else:
                        return RAGFlowStatus.RUNNING
                elif container_status == "created":
                    return RAGFlowStatus.STARTING
                else:
                    return RAGFlowStatus.STOPPED
                    
            except docker.errors.NotFound:
                return RAGFlowStatus.STOPPED
                
        except Exception as e:
            logger.error("Error checking RAGFlow status", extra={"error": str(e)})
            return RAGFlowStatus.ERROR
    
    def _check_api_health(self) -> bool:
        """Check if RAGFlow API is responding"""
        try:
            health_url = f"{self.base_url}/v1/system/health"
            response = requests.get(health_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def _wait_for_healthy_status(self, timeout: int = None) -> bool:
        """
        Wait for RAGFlow service to become healthy.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if service became healthy
        """
        timeout = timeout or self.max_startup_time
        start_time = time.time()
        
        logger.info("Waiting for RAGFlow service to become healthy", extra={"timeout": timeout})
        
        while time.time() - start_time < timeout:
            status = self.get_service_status()
            
            if status == RAGFlowStatus.HEALTHY:
                return True
            elif status == RAGFlowStatus.ERROR:
                return False
            
            time.sleep(5)  # Check every 5 seconds
        
        return False
    
    def get_service_logs(self, lines: int = 100) -> str:
        """
        Get RAGFlow service logs.
        
        Args:
            lines: Number of recent log lines to retrieve
            
        Returns:
            str: Service logs
        """
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "logs", "--tail", str(lines)],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=30
            )
            
            return result.stdout if result.returncode == 0 else result.stderr
            
        except Exception as e:
            logger.error("Error getting RAGFlow logs", extra={"error": str(e)})
            return f"Error retrieving logs: {str(e)}"
    
    def create_knowledge_base(
        self, 
        name: str, 
        description: str = "",
        mathematical_optimized: bool = True
    ) -> Optional[str]:
        """
        Create a new knowledge base optimized for mathematical content.
        
        Args:
            name: Knowledge base name
            description: Knowledge base description
            mathematical_optimized: Whether to optimize for mathematical content
            
        Returns:
            str: Knowledge base ID if successful, None otherwise
        """
        try:
            # Configure for mathematical content if requested
            settings = {
                "name": name,
                "description": description,
                "embedding_model": "bge-m3" if mathematical_optimized else "bge-large-zh-v1.5",
                "chunk_size": 1000 if mathematical_optimized else 512,
                "chunk_overlap": 0.4 if mathematical_optimized else 0.1,
                "mathematical_processing": mathematical_optimized,
                "layout_recognition": True,
                "table_structure_recognition": True,
                "mathematical_notation_preservation": mathematical_optimized
            }
            
            response = requests.post(
                f"{self.base_url}/v1/knowledge_bases",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=settings,
                timeout=30
            )
            
            if response.status_code == 201:
                kb_data = response.json()
                kb_id = kb_data.get("id")
                
                logger.info(
                    "Knowledge base created successfully",
                    extra={
                        "kb_id": kb_id,
                        "name": name,
                        "mathematical_optimized": mathematical_optimized
                    }
                )
                
                return kb_id
            else:
                logger.error(
                    "Failed to create knowledge base",
                    extra={"status_code": response.status_code, "response": response.text}
                )
                return None
                
        except Exception as e:
            logger.error("Error creating knowledge base", extra={"error": str(e)})
            return None
    
    def upload_document(
        self, 
        kb_id: str, 
        file_path: Union[str, Path],
        mathematical_content: bool = True
    ) -> Optional[str]:
        """
        Upload document to knowledge base with mathematical processing.
        
        Args:
            kb_id: Knowledge base ID
            file_path: Path to document file
            mathematical_content: Whether document contains mathematical content
            
        Returns:
            str: Document ID if successful, None otherwise
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error("Document file not found", extra={"file_path": str(file_path)})
                return None
            
            # Prepare file upload using correct RAGFlow API endpoint
            url = f"{self.base_url}/api/v1/datasets/{kb_id}/documents"
            
            start_time = time.time()
            
            # Use multipart form data as expected by RAGFlow
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'application/octet-stream')}
                
                response = requests.post(
                    url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files,
                    timeout=300  # 5 minutes for large documents
                )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    doc_info = data.get("data", [])
                    if doc_info:
                        doc_id = doc_info[0].get("id")
                        processing_time = time.time() - start_time
                        
                        logger.info(
                            "Document uploaded successfully",
                            extra={
                                "doc_id": doc_id,
                                "file_name": file_path.name,
                                "file_size": file_path.stat().st_size,
                                "processing_time": processing_time,
                                "mathematical_content": mathematical_content
                            }
                        )
                        
                        return doc_id
            
            logger.error(
                "Failed to upload document",
                extra={
                    "status_code": response.status_code,
                    "response": response.text[:500],
                    "file_name": file_path.name
                }
            )
            return None
                
        except Exception as e:
            logger.error("Error uploading document", extra={"error": str(e), "file_path": str(file_path)})
            return None
    
    def get_knowledge_bases(self) -> List[KnowledgeBaseInfo]:
        """
        Get list of all knowledge bases.
        
        Returns:
            List[KnowledgeBaseInfo]: List of knowledge base information
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/knowledge_bases",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                kb_list = response.json().get("data", [])
                
                knowledge_bases = []
                for kb_data in kb_list:
                    kb_info = KnowledgeBaseInfo(
                        id=kb_data.get("id"),
                        name=kb_data.get("name"),
                        description=kb_data.get("description", ""),
                        chunk_count=kb_data.get("chunk_count", 0),
                        document_count=kb_data.get("document_count", 0),
                        embedding_model=kb_data.get("embedding_model", ""),
                        created_at=kb_data.get("created_at", ""),
                        mathematical_optimized=kb_data.get("mathematical_processing", False)
                    )
                    knowledge_bases.append(kb_info)
                
                return knowledge_bases
            else:
                logger.error(
                    "Failed to get knowledge bases",
                    extra={"status_code": response.status_code}
                )
                return []
                
        except Exception as e:
            logger.error("Error getting knowledge bases", extra={"error": str(e)})
            return []
    
    def get_documents(self, kb_id: str) -> List[DocumentInfo]:
        """
        Get list of documents in a knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            List[DocumentInfo]: List of document information
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/knowledge_bases/{kb_id}/documents",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                doc_list = response.json().get("data", [])
                
                documents = []
                for doc_data in doc_list:
                    doc_info = DocumentInfo(
                        id=doc_data.get("id"),
                        name=doc_data.get("name"),
                        size=doc_data.get("size", 0),
                        status=doc_data.get("status", "unknown"),
                        chunks=doc_data.get("chunk_count", 0),
                        upload_time=doc_data.get("upload_time", ""),
                        processing_time=doc_data.get("processing_time"),
                        mathematical_content=doc_data.get("mathematical_content", False)
                    )
                    documents.append(doc_info)
                
                return documents
            else:
                logger.error(
                    "Failed to get documents",
                    extra={"status_code": response.status_code, "kb_id": kb_id}
                )
                return []
                
        except Exception as e:
            logger.error("Error getting documents", extra={"error": str(e), "kb_id": kb_id})
            return []
    
    def delete_knowledge_base(self, kb_id: str) -> bool:
        """
        Delete a knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            bool: True if deletion successful
        """
        try:
            response = requests.delete(
                f"{self.base_url}/v1/knowledge_bases/{kb_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Knowledge base deleted successfully", extra={"kb_id": kb_id})
                return True
            else:
                logger.error(
                    "Failed to delete knowledge base",
                    extra={"status_code": response.status_code, "kb_id": kb_id}
                )
                return False
                
        except Exception as e:
            logger.error("Error deleting knowledge base", extra={"error": str(e), "kb_id": kb_id})
            return False
    
    def get_service_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive service metrics.
        
        Returns:
            Dict[str, Any]: Service metrics and performance data
        """
        try:
            # Get basic service status
            status = self.get_service_status()
            
            # Get Docker container stats if available
            container_stats = {}
            if self.docker_client:
                try:
                    container = self.docker_client.containers.get(self.container_name)
                    stats = container.stats(stream=False)
                    
                    # Calculate CPU percentage
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                               stats['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                                  stats['precpu_stats']['system_cpu_usage']
                    cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0.0
                    
                    # Memory usage
                    memory_usage = stats['memory_stats']['usage']
                    memory_limit = stats['memory_stats']['limit']
                    memory_percent = (memory_usage / memory_limit) * 100.0
                    
                    container_stats = {
                        "cpu_percent": round(cpu_percent, 2),
                        "memory_usage_mb": round(memory_usage / 1024 / 1024, 2),
                        "memory_limit_mb": round(memory_limit / 1024 / 1024, 2),
                        "memory_percent": round(memory_percent, 2)
                    }
                    
                except Exception as e:
                    logger.debug("Could not get container stats", extra={"error": str(e)})
            
            # Get knowledge base metrics
            knowledge_bases = self.get_knowledge_bases()
            kb_metrics = {
                "total_knowledge_bases": len(knowledge_bases),
                "total_documents": sum(kb.document_count for kb in knowledge_bases),
                "total_chunks": sum(kb.chunk_count for kb in knowledge_bases),
                "mathematical_optimized_kbs": sum(1 for kb in knowledge_bases if kb.mathematical_optimized)
            }
            
            return {
                "service_status": status.value,
                "api_healthy": self._check_api_health(),
                "container_stats": container_stats,
                "knowledge_base_metrics": kb_metrics,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error("Error getting service metrics", extra={"error": str(e)})
            return {
                "service_status": "error",
                "api_healthy": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def is_available(self) -> bool:
        """
        Check if RAGFlow service is available and healthy.
        
        Returns:
            bool: True if service is available
        """
        try:
            status = self.get_service_status()
            return status in [RAGFlowStatus.RUNNING, RAGFlowStatus.HEALTHY]
        except Exception:
            return False
    
    def get_docker_status(self) -> Dict[str, Any]:
        """
        Get Docker container status information.
        
        Returns:
            Dict[str, Any]: Docker status information
        """
        try:
            if not self.docker_client:
                return {"status": "docker_unavailable", "error": "Docker client not initialized"}
            
            container = self.docker_client.containers.get(self.container_name)
            return {
                "status": container.status,
                "state": container.attrs.get("State", {}),
                "created": container.attrs.get("Created", ""),
                "image": container.image.tags[0] if container.image.tags else "unknown"
            }
        except docker.errors.NotFound:
            return {"status": "not_found", "error": f"Container {self.container_name} not found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_knowledge_base_count(self) -> int:
        """
        Get the number of knowledge bases.
        
        Returns:
            int: Number of knowledge bases
        """
        try:
            knowledge_bases = self.get_knowledge_bases()
            return len(knowledge_bases)
        except Exception:
            return 0
    
    def is_model_loaded(self, model_name: str) -> bool:
        """
        Check if a specific model is loaded.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            bool: True if model is loaded
        """
        try:
            # For now, assume BGE-M3 is loaded if service is available
            # This would need to be implemented based on RAGFlow's actual API
            return self.is_available() and model_name.lower() in ["bge-m3", "bge_m3"]
        except Exception:
            return False
    
    def retrieve_and_answer(self, query: str, messages: List[Dict[str, str]]) -> str:
        """
        Retrieve relevant documents and generate an answer using RAGFlow.
        
        This method implements the full RAGFlow pipeline:
        1. Get or create a knowledge base for mathematical content
        2. Retrieve relevant chunks using RAGFlow's API
        3. Generate an answer using RAGFlow's chat completion
        4. Return formatted response with citations
        
        Args:
            query: User query
            messages: Conversation history (list of role/content dicts)
            
        Returns:
            str: Generated answer with citations and source references
        """
        try:
            if not self.is_available():
                raise RAGFlowServiceError("RAGFlow service not available")
            
            logger.info("Starting RAGFlow retrieve and answer process", extra={
                "query_length": len(query),
                "message_count": len(messages)
            })
            
            # Step 1: Get or create knowledge base for mathematical content
            kb_name = self.config.get("ragflow.knowledge_base", "mathematical_kb")
            kb_id = self._get_or_create_mathematical_kb(kb_name)
            
            if not kb_id:
                raise RAGFlowServiceError("Failed to get or create knowledge base")
            
            # Step 2: Get or create chat assistant for this knowledge base
            chat_id = self._get_or_create_chat_assistant(kb_id)
            
            if not chat_id:
                raise RAGFlowServiceError("Failed to get or create chat assistant")
            
            # Step 3: Format conversation history for RAGFlow
            formatted_messages = self._format_conversation_history(messages, query)
            
            # Step 4: Get completion from RAGFlow using chat API
            response = self._get_chat_completion(chat_id, formatted_messages)
            
            logger.info("RAGFlow retrieve and answer completed successfully", extra={
                "response_length": len(response),
                "kb_id": kb_id,
                "chat_id": chat_id
            })
            
            return response
            
        except Exception as e:
            logger.error("RAGFlow retrieve_and_answer failed", extra={
                "error": str(e),
                "query": query[:100] if query else "",
                "message_count": len(messages)
            })
            raise RAGFlowServiceError(f"Failed to retrieve and answer: {e}")
    
    def _get_or_create_mathematical_kb(self, kb_name: str) -> Optional[str]:
        """
        Get existing mathematical knowledge base or create a new one.
        
        Args:
            kb_name: Name of the knowledge base
            
        Returns:
            str: Knowledge base ID
        """
        try:
            # First try to find existing knowledge base
            response = requests.get(
                f"{self.base_url}/api/v1/datasets",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"name": kb_name},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0 and data.get("data"):
                    # Found existing KB
                    for kb in data["data"]:
                        if kb.get("name") == kb_name:
                            logger.info("Using existing knowledge base", extra={
                                "kb_name": kb_name,
                                "kb_id": kb["id"]
                            })
                            return kb["id"]
            
            # Create new knowledge base if not found
            create_data = {
                "name": kb_name,
                "description": "Mathematical content knowledge base with BGE-M3 embeddings",
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/datasets",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=create_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    kb_id = data["data"]["id"]
                    logger.info("Created new mathematical knowledge base", extra={
                        "kb_name": kb_name,
                        "kb_id": kb_id
                    })
                    return kb_id
            
            logger.error("Failed to create knowledge base", extra={
                "status_code": response.status_code,
                "response": response.text[:200]
            })
            return None
            
        except Exception as e:
            logger.error("Error getting or creating knowledge base", extra={
                "error": str(e),
                "kb_name": kb_name
            })
            return None
    
    def _get_or_create_chat_assistant(self, kb_id: str) -> Optional[str]:
        """
        Get or create a chat assistant for the knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            str: Chat assistant ID
        """
        try:
            chat_name = f"mathematical_assistant_{kb_id[:8]}"
            
            # Try to find existing chat assistant
            response = requests.get(
                f"{self.base_url}/api/v1/chats",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"name": chat_name},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0 and data.get("data"):
                    for chat in data["data"]:
                        if chat.get("name") == chat_name:
                            logger.info("Using existing chat assistant", extra={
                                "chat_name": chat_name,
                                "chat_id": chat["id"]
                            })
                            return chat["id"]
            
            # Create new chat assistant
            create_data = {
                "name": chat_name,
                "avatar": "",
                "dataset_ids": [kb_id],
                "prompt": {
                    "similarity_threshold": 0.2,
                    "keywords_similarity_weight": 0.7,
                    "top_n": 6,  # Good for mathematical content
                    "empty_response": "I don't have information about that in my knowledge base. Could you rephrase your question or ask about mathematical topics I might know?",
                    "opener": "Hi! I'm your mathematical assistant. I can help you with mathematical concepts, theorems, proofs, and academic content. What would you like to know?",
                    "show_quote": True,
                    "prompt": (
                        "You are an expert mathematical assistant with deep knowledge of mathematics, "
                        "including algebra, topology, geometry, analysis, and advanced mathematical concepts. "
                        "Use the provided knowledge base to answer questions accurately and thoroughly. "
                        "Preserve mathematical notation, LaTeX expressions, and cite sources when available. "
                        "If the question involves mathematical concepts not in the knowledge base, "
                        "clearly state this limitation.\n\nKnowledge base:\n{knowledge}\n\n"
                        "Always provide detailed explanations for mathematical concepts and include "
                        "relevant context from the knowledge base."
                    )
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/chats",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=create_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    chat_id = data["data"]["id"]
                    logger.info("Created new chat assistant", extra={
                        "chat_name": chat_name,
                        "chat_id": chat_id,
                        "kb_id": kb_id
                    })
                    return chat_id
            
            logger.error("Failed to create chat assistant", extra={
                "status_code": response.status_code,
                "response": response.text[:200]
            })
            return None
            
        except Exception as e:
            logger.error("Error getting or creating chat assistant", extra={
                "error": str(e),
                "kb_id": kb_id
            })
            return None
    
    def _format_conversation_history(self, messages: List[Dict[str, str]], current_query: str) -> List[Dict[str, str]]:
        """
        Format conversation history for RAGFlow API.
        
        Args:
            messages: Previous conversation messages
            current_query: Current user query
            
        Returns:
            List[Dict]: Formatted messages for RAGFlow
        """
        formatted_messages = []
        
        # Add previous messages (limit to last 10 to avoid token limits)
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        
        for msg in recent_messages:
            if msg.get("role") in ["user", "assistant"]:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg.get("content", "")
                })
        
        # Add current query
        formatted_messages.append({
            "role": "user", 
            "content": current_query
        })
        
        return formatted_messages
    
    def _get_chat_completion(self, chat_id: str, messages: List[Dict[str, str]]) -> str:
        """
        Get chat completion from RAGFlow.
        
        Args:
            chat_id: Chat assistant ID
            messages: Formatted conversation messages
            
        Returns:
            str: Generated response
        """
        try:
            # Use the chat completion API
            completion_data = {
                "question": messages[-1]["content"],  # Current question
                "stream": False,  # Non-streaming for simplicity
                "session_id": None  # Let RAGFlow create a new session
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/chats/{chat_id}/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=completion_data,
                timeout=60  # Allow time for generation
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    result = data.get("data", {})
                    
                    # Handle case where result might be a string instead of dict
                    if isinstance(result, str):
                        return result
                    elif isinstance(result, dict):
                        answer = result.get("answer", "")
                        
                        # Include reference information if available
                        references = result.get("reference", {})
                        if references and references.get("chunks"):
                            citations = self._format_citations(references["chunks"])
                            if citations:
                                answer += f"\n\n**Sources:**\n{citations}"
                        
                        return answer
                    else:
                        # Fallback for unexpected response format
                        return str(result)
                else:
                    error_msg = data.get("message", "Unknown error from RAGFlow")
                    logger.error("RAGFlow API error", extra={"error": error_msg})
                    raise RAGFlowServiceError(f"RAGFlow API error: {error_msg}")
            else:
                logger.error("RAGFlow completion request failed", extra={
                    "status_code": response.status_code,
                    "response": response.text[:200]
                })
                raise RAGFlowServiceError(f"RAGFlow completion failed: {response.status_code}")
                
        except requests.RequestException as e:
            logger.error("Network error in chat completion", extra={"error": str(e)})
            raise RAGFlowServiceError(f"Network error: {e}")
        except Exception as e:
            logger.error("Unexpected error in chat completion", extra={"error": str(e)})
            raise RAGFlowServiceError(f"Chat completion error: {e}")
    
    def _format_citations(self, chunks: List[Dict]) -> str:
        """
        Format citation information from retrieved chunks.
        
        Args:
            chunks: List of retrieved chunk data
            
        Returns:
            str: Formatted citation text
        """
        citations = []
        seen_sources = set()
        
        for i, chunk in enumerate(chunks[:5], 1):  # Limit to top 5 sources
            source = chunk.get("docnm_kwd", chunk.get("doc_name", "Unknown"))
            if source and source not in seen_sources:
                seen_sources.add(source)
                page_info = ""
                if chunk.get("page_number"):
                    page_info = f" (Page {chunk['page_number']})"
                citations.append(f"{i}. {source}{page_info}")
        
        return "\n".join(citations) if citations else "" 