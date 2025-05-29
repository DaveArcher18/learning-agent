"""
Retriever Factory - Modular retrieval system for switching between RAGFlow and Qdrant.

This factory provides a clean abstraction for different retrieval backends,
enabling easy A/B testing and configuration-driven switching.
"""

import logging
import os
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from langchain.schema import BaseRetriever

logger = logging.getLogger(__name__)


class RetrieverConfig:
    """Configuration container for retriever settings."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        self.config = config_dict
        self.retriever_type = config_dict.get('rag', {}).get('retriever', 'qdrant')
        self.ragflow = config_dict.get('ragflow', {})
        self.qdrant = config_dict.get('legacy_qdrant', {})


class BaseRetrieverProvider(ABC):
    """Abstract base class for retriever providers."""
    
    @abstractmethod
    def create_retriever(self, config: RetrieverConfig) -> BaseRetriever:
        """Create and return a configured retriever instance."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this retriever provider is available and properly configured."""
        pass


class RAGFlowRetrieverProvider(BaseRetrieverProvider):
    """RAGFlow retriever provider with advanced layout-aware processing."""
    
    def create_retriever(self, config: RetrieverConfig) -> BaseRetriever:
        """Create RAGFlow retriever with comprehensive document understanding."""
        try:
            # Import here to avoid dependency issues if not installed
            from ragflow_sdk import RAGFlow
            
            ragflow_config = config.ragflow
            endpoint = os.getenv('RAGFLOW_ENDPOINT', f"http://{ragflow_config.get('host', 'localhost')}:{ragflow_config.get('port', 9380)}")
            api_key = os.getenv('RAGFLOW_API_KEY', ragflow_config.get('api_key'))
            kb_name = os.getenv('RAGFLOW_KB_ID', ragflow_config.get('knowledge_base', 'mathematical_kb'))
            
            logger.info(f"Initializing RAGFlow retriever with endpoint: {endpoint}")
            
            # Initialize RAGFlow client
            ragflow = RAGFlow(api_key=api_key, base_url=endpoint)
            
            # Get or create knowledge base
            kb = self._get_or_create_kb(ragflow, kb_name)
            
            # Create custom retriever wrapper
            return RAGFlowRetriever(
                ragflow_client=ragflow,
                knowledge_base=kb,
                top_k=config.config.get('rag', {}).get('top_k', 50),
                final_k=config.config.get('rag', {}).get('final_k', 15),
                similarity_threshold=config.config.get('rag', {}).get('similarity_threshold', 0.5),
                enable_reranking=config.config.get('rag', {}).get('enable_reranking', True)
            )
            
        except ImportError:
            logger.error("RAGFlow SDK not installed. Please install with: pip install ragflow-sdk")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize RAGFlow retriever: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if RAGFlow is properly installed and configured."""
        try:
            import ragflow_sdk
            endpoint = os.getenv('RAGFLOW_ENDPOINT')
            return endpoint is not None
        except ImportError:
            return False
    
    def _get_or_create_kb(self, ragflow, kb_name: str):
        """Get existing knowledge base or create a new one."""
        try:
            # Try to get existing KB
            kbs = ragflow.list_datasets()
            for kb in kbs:
                if kb.name == kb_name:
                    logger.info(f"Using existing knowledge base: {kb_name}")
                    return kb
            
            # Create new KB if not found
            logger.info(f"Creating new knowledge base: {kb_name}")
            kb = ragflow.create_dataset(name=kb_name)
            return kb
            
        except Exception as e:
            logger.error(f"Error managing knowledge base {kb_name}: {e}")
            raise


class QdrantRetrieverProvider(BaseRetrieverProvider):
    """Legacy Qdrant retriever provider."""
    
    def create_retriever(self, config: RetrieverConfig) -> BaseRetriever:
        """Create Qdrant retriever using existing configuration."""
        try:
            from qdrant_client import QdrantClient
            from langchain.vectorstores import Qdrant
            from langchain.embeddings import HuggingFaceEmbeddings
            
            qdrant_config = config.qdrant
            collection_name = qdrant_config.get('collection', 'MoravaKTheory')
            
            logger.info(f"Initializing Qdrant retriever with collection: {collection_name}")
            
            # Initialize Qdrant client
            client = QdrantClient(location=":memory:")  # or configure for persistent storage
            
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5",
                model_kwargs={'device': 'cpu'}
            )
            
            # Create Qdrant vector store
            vectorstore = Qdrant(
                client=client,
                collection_name=collection_name,
                embeddings=embeddings
            )
            
            return vectorstore.as_retriever(
                search_kwargs={"k": qdrant_config.get('db_search_limit', 20)}
            )
            
        except ImportError:
            logger.error("Qdrant dependencies not installed")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant retriever: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Qdrant dependencies are available."""
        try:
            import qdrant_client
            return True
        except ImportError:
            return False


class RAGFlowRetriever(BaseRetriever):
    """Custom LangChain-compatible RAGFlow retriever."""
    
    def __init__(self, ragflow_client, knowledge_base, top_k: int = 50, 
                 final_k: int = 15, similarity_threshold: float = 0.5,
                 enable_reranking: bool = True):
        self.ragflow_client = ragflow_client
        self.knowledge_base = knowledge_base
        self.top_k = top_k
        self.final_k = final_k
        self.similarity_threshold = similarity_threshold
        self.enable_reranking = enable_reranking
        
    def get_relevant_documents(self, query: str):
        """Retrieve relevant documents using RAGFlow's advanced processing."""
        try:
            # Query the knowledge base
            results = self.knowledge_base.search(
                query=query,
                limit=self.top_k,
                similarity_threshold=self.similarity_threshold,
                with_vector=False,  # We don't need raw vectors
                with_payload=True   # We want metadata and content
            )
            
            # Convert to LangChain Document format
            from langchain.schema import Document
            
            documents = []
            for result in results[:self.final_k]:  # Limit to final_k results
                doc = Document(
                    page_content=result.get('content', ''),
                    metadata={
                        'source': result.get('source', ''),
                        'score': result.get('score', 0.0),
                        'chunk_id': result.get('chunk_id', ''),
                        'title': result.get('title', ''),
                        'page_number': result.get('page_number', None),
                        'retriever': 'ragflow'
                    }
                )
                documents.append(doc)
            
            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents from RAGFlow: {e}")
            return []

    async def aget_relevant_documents(self, query: str):
        """Async version of get_relevant_documents."""
        return self.get_relevant_documents(query)


class RetrieverFactory:
    """Factory class for creating retriever instances based on configuration."""
    
    def __init__(self):
        self.providers = {
            'ragflow': RAGFlowRetrieverProvider(),
            'qdrant': QdrantRetrieverProvider()
        }
    
    def create_retriever(self, config_dict: Dict[str, Any]) -> BaseRetriever:
        """
        Create a retriever based on configuration.
        
        Args:
            config_dict: Configuration dictionary containing retriever settings
            
        Returns:
            Configured retriever instance
            
        Raises:
            ValueError: If retriever type is not supported or not available
        """
        config = RetrieverConfig(config_dict)
        retriever_type = config.retriever_type
        
        logger.info(f"Creating retriever of type: {retriever_type}")
        
        if retriever_type not in self.providers:
            available_types = list(self.providers.keys())
            raise ValueError(f"Unsupported retriever type: {retriever_type}. Available: {available_types}")
        
        provider = self.providers[retriever_type]
        
        if not provider.is_available():
            logger.warning(f"Retriever type {retriever_type} is not available, falling back to qdrant")
            # Fallback to Qdrant if RAGFlow is not available
            if retriever_type != 'qdrant' and self.providers['qdrant'].is_available():
                provider = self.providers['qdrant']
            else:
                raise ValueError(f"Retriever type {retriever_type} is not available and no fallback found")
        
        return provider.create_retriever(config)
    
    def list_available_retrievers(self) -> Dict[str, bool]:
        """List all retriever types and their availability status."""
        return {name: provider.is_available() for name, provider in self.providers.items()}


# Global factory instance
retriever_factory = RetrieverFactory()


def get_retriever(config: Dict[str, Any]) -> BaseRetriever:
    """
    Convenience function to create a retriever from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured retriever instance
    """
    return retriever_factory.create_retriever(config) 