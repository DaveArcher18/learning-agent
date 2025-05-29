"""
RAGFlow Document Ingestion Module

This module handles the ingestion of documents into RAGFlow knowledge bases,
with specific optimization for mathematical content and academic papers.
"""

import logging
import os
import asyncio
import requests
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DocumentMetadata:
    """Container for document metadata during ingestion."""
    filename: str
    file_path: str
    file_size: int
    document_type: str
    source_info: Dict[str, Any]


class RAGFlowIngestionError(Exception):
    """Custom exception for RAGFlow ingestion errors."""
    pass


class DocumentProcessor:
    """Processes documents for RAGFlow ingestion with mathematical content optimization."""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.md', '.txt', '.docx', '.doc'}
    MATHEMATICAL_KEYWORDS = {
        'theorem', 'proof', 'lemma', 'corollary', 'proposition', 
        'definition', 'equation', 'formula', 'morava', 'k-theory'
    }
    
    def __init__(self, enable_preprocessing: bool = True):
        self.enable_preprocessing = enable_preprocessing
    
    def analyze_document(self, file_path: Path) -> DocumentMetadata:
        """Analyze document and extract metadata."""
        try:
            stat = file_path.stat()
            
            # Determine document type based on content and extension
            doc_type = self._classify_document_type(file_path)
            
            # Extract source information
            source_info = {
                'modification_time': stat.st_mtime,
                'creation_time': stat.st_ctime,
                'is_mathematical': self._contains_mathematical_content(file_path),
                'estimated_pages': self._estimate_page_count(file_path),
            }
            
            return DocumentMetadata(
                filename=file_path.name,
                file_path=str(file_path),
                file_size=stat.st_size,
                document_type=doc_type,
                source_info=source_info
            )
            
        except Exception as e:
            logger.error(f"Error analyzing document {file_path}: {e}")
            raise RAGFlowIngestionError(f"Document analysis failed: {e}")
    
    def _classify_document_type(self, file_path: Path) -> str:
        """Classify document based on filename and content patterns."""
        name_lower = file_path.name.lower()
        
        if 'thesis' in name_lower:
            return 'academic_thesis'
        elif 'paper' in name_lower or 'article' in name_lower:
            return 'research_paper'
        elif file_path.suffix == '.md':
            return 'markdown_notes'
        elif file_path.suffix == '.pdf':
            return 'pdf_document'
        else:
            return 'general_document'
    
    def _contains_mathematical_content(self, file_path: Path) -> bool:
        """Check if document likely contains mathematical content."""
        try:
            if file_path.suffix == '.md':
                # For markdown files, we can do basic text analysis
                content = file_path.read_text(encoding='utf-8')[:5000]  # First 5KB
                content_lower = content.lower()
                
                # Check for mathematical keywords
                math_keywords_found = sum(1 for keyword in self.MATHEMATICAL_KEYWORDS 
                                        if keyword in content_lower)
                
                # Check for LaTeX math indicators
                latex_indicators = ['\\(', '\\[', '$$', '$', '\\begin{', '\\theorem', '\\proof']
                latex_found = sum(1 for indicator in latex_indicators if indicator in content)
                
                return math_keywords_found >= 2 or latex_found >= 3
            
            # For other file types, assume mathematical if in specific directories or names
            return any(keyword in file_path.name.lower() for keyword in self.MATHEMATICAL_KEYWORDS)
            
        except Exception:
            # If we can't read the file, make a conservative assumption
            return True
    
    def _estimate_page_count(self, file_path: Path) -> int:
        """Estimate page count based on file size and type."""
        size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if file_path.suffix == '.pdf':
            # Rough estimate: 100KB per page for academic PDFs
            return max(1, int(size_mb * 10))
        elif file_path.suffix == '.md':
            # Rough estimate: 50KB per "page" for markdown
            return max(1, int(size_mb * 20))
        else:
            return max(1, int(size_mb * 5))


class SimpleRAGFlowClient:
    """Simplified RAGFlow client that works with direct API calls."""
    
    def __init__(self, endpoint: str, api_key: str = None):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key or ""
        self.session = requests.Session()
        
        # Set up headers
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check if RAGFlow service is healthy."""
        try:
            response = self.session.get(f"{self.endpoint}/health", timeout=10)
            if response.status_code == 200:
                return {'status': 'healthy', 'response_time': response.elapsed.total_seconds()}
            else:
                return {'status': 'degraded', 'status_code': response.status_code}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def list_datasets(self) -> List[Dict[str, Any]]:
        """List available knowledge bases/datasets."""
        try:
            response = self.session.get(f"{self.endpoint}/api/v1/datasets")
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                logger.warning(f"Failed to list datasets: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error listing datasets: {e}")
            return []
    
    def create_dataset(self, name: str, description: str = "", **kwargs) -> Dict[str, Any]:
        """Create a new knowledge base/dataset."""
        try:
            payload = {
                'name': name,
                'description': description,
                'language': kwargs.get('language', 'English'),
                'embedding_model': kwargs.get('embedding_model', 'BAAI/bge-m3'),
                'permission': kwargs.get('permission', 'me'),
                'chunk_method': kwargs.get('chunk_method', 'intelligent'),
                'parser_config': kwargs.get('parser_config', {
                    'chunk_token_count': 1000,
                    'layout_recognize': True,
                    'delimiter': "\\n!?。；！？",
                    'task_page_size': 12
                })
            }
            
            response = self.session.post(f"{self.endpoint}/api/v1/datasets", json=payload)
            if response.status_code in [200, 201]:
                return response.json().get('data', {})
            else:
                logger.error(f"Failed to create dataset: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error creating dataset: {e}")
            return {}


class RAGFlowIngestor:
    """Main class for ingesting documents into RAGFlow knowledge bases."""
    
    def __init__(self, endpoint: str = None, api_key: str = None):
        self.endpoint = endpoint or os.getenv('RAGFLOW_ENDPOINT', 'http://localhost:9380')
        self.api_key = api_key or os.getenv('RAGFLOW_API_KEY')
        self.processor = DocumentProcessor()
        self._client = None
        
    @property
    def ragflow_client(self):
        """Get or create RAGFlow client."""
        if self._client is None:
            self._client = SimpleRAGFlowClient(self.endpoint, self.api_key)
        return self._client
    
    def get_or_create_knowledge_base(self, kb_name: str) -> Any:
        """Get existing knowledge base or create a new one."""
        try:
            # List existing datasets/knowledge bases
            datasets = self.ragflow_client.list_datasets()
            
            # Look for existing KB
            for dataset in datasets:
                if dataset.get('name') == kb_name:
                    logger.info(f"Using existing knowledge base: {kb_name}")
                    return dataset
            
            # Create new KB if not found
            logger.info(f"Creating new knowledge base: {kb_name}")
            dataset = self.ragflow_client.create_dataset(
                name=kb_name,
                description=f"Mathematical knowledge base for {kb_name}",
                language="English",
                embedding_model="BAAI/bge-m3",
                permission="me",
                chunk_method="intelligent",
                parser_config={
                    "chunk_token_count": 1000,
                    "layout_recognize": True,
                    "delimiter": "\\n!?。；！？",
                    "task_page_size": 12
                }
            )
            
            return dataset
            
        except Exception as e:
            logger.error(f"Error managing knowledge base {kb_name}: {e}")
            raise RAGFlowIngestionError(f"Knowledge base management failed: {e}")
    
    def ingest_document(self, file_path: Path, kb_name: str) -> Dict[str, Any]:
        """Ingest a single document into the specified knowledge base."""
        try:
            # Analyze document
            metadata = self.processor.analyze_document(file_path)
            logger.info(f"Ingesting {metadata.filename} ({metadata.file_size} bytes)")
            
            # Get or create knowledge base
            kb = self.get_or_create_knowledge_base(kb_name)
            
            # For now, log the successful preparation
            result = {
                'document': metadata.filename,
                'knowledge_base': kb_name,
                'status': 'analyzed',
                'metadata': metadata.source_info,
                'size_bytes': metadata.file_size,
                'type': metadata.document_type
            }
            
            logger.info(f"✅ Document analyzed: {metadata.filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error ingesting document {file_path}: {e}")
            raise RAGFlowIngestionError(f"Document ingestion failed: {e}")
    
    def ingest_directory(self, directory_path: Path, kb_name: str, 
                        file_pattern: str = "*") -> Dict[str, Any]:
        """Ingest all supported documents from a directory."""
        try:
            if not directory_path.exists():
                raise RAGFlowIngestionError(f"Directory not found: {directory_path}")
            
            # Find all supported files
            supported_files = []
            for pattern in [f"*{ext}" for ext in DocumentProcessor.SUPPORTED_EXTENSIONS]:
                supported_files.extend(directory_path.glob(pattern))
            
            if not supported_files:
                logger.warning(f"No supported documents found in {directory_path}")
                return {'status': 'no_files', 'processed': 0, 'results': []}
            
            logger.info(f"Found {len(supported_files)} documents to ingest")
            
            # Process each file
            results = []
            successful_ingestions = 0
            
            for file_path in supported_files:
                logger.info(f"Processing {file_path.name}...")
                result = self.ingest_document(file_path, kb_name)
                results.append(result)
                
                if result['status'] == 'success':
                    successful_ingestions += 1
                
                # Add small delay to avoid overwhelming the service
                asyncio.sleep(0.5)
            
            return {
                'status': 'completed',
                'total_files': len(supported_files),
                'successful': successful_ingestions,
                'failed': len(supported_files) - successful_ingestions,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error ingesting directory {directory_path}: {e}")
            raise RAGFlowIngestionError(f"Directory ingestion failed: {e}")
    
    def check_ingestion_status(self, kb_name: str) -> Dict[str, Any]:
        """Check the status of document processing in a knowledge base."""
        try:
            kb = self.get_or_create_knowledge_base(kb_name)
            
            # Get list of documents in the knowledge base
            documents = kb.list_documents()
            
            status_summary = {
                'total_documents': len(documents),
                'processed': 0,
                'processing': 0,
                'failed': 0,
                'pending': 0
            }
            
            for doc in documents:
                status = getattr(doc, 'status', 'unknown')
                if status in status_summary:
                    status_summary[status] += 1
                elif status == 'completed':
                    status_summary['processed'] += 1
                else:
                    status_summary['pending'] += 1
            
            return status_summary
            
        except Exception as e:
            logger.error(f"Error checking ingestion status: {e}")
            return {'error': str(e)}


def main():
    """Main function for command-line usage."""
    import argparse
    import yaml
    
    parser = argparse.ArgumentParser(description="Ingest documents into RAGFlow")
    parser.add_argument("--docs-dir", type=str, default="docs", 
                       help="Directory containing documents to ingest")
    parser.add_argument("--kb-name", type=str, default="mathematical_kb",
                       help="Knowledge base name")
    parser.add_argument("--config", type=str, default="config.yaml",
                       help="Configuration file path")
    parser.add_argument("--check-status", action="store_true",
                       help="Check ingestion status only")
    
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Load configuration
        if Path(args.config).exists():
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        
        # Initialize ingestor
        ingestor = RAGFlowIngestor()
        
        if args.check_status:
            # Just check status
            status = ingestor.check_ingestion_status(args.kb_name)
            print(f"Knowledge base '{args.kb_name}' status:")
            for key, value in status.items():
                print(f"  {key}: {value}")
        else:
            # Perform ingestion
            docs_path = Path(args.docs_dir)
            print(f"Starting ingestion from {docs_path} into knowledge base '{args.kb_name}'")
            
            result = ingestor.ingest_directory(docs_path, args.kb_name)
            
            print(f"\nIngestion completed:")
            print(f"  Total files: {result.get('total_files', 0)}")
            print(f"  Successful: {result.get('successful', 0)}")
            print(f"  Failed: {result.get('failed', 0)}")
            
            # Show details for failed ingestions
            failed_files = [r for r in result.get('results', []) if r['status'] == 'error']
            if failed_files:
                print(f"\nFailed ingestions:")
                for failure in failed_files:
                    print(f"  {failure['filename']}: {failure['error']}")
    
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 