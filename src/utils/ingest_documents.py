"""
Document Ingestion Utility

Uploads documents from the data/documents directory to RAGFlow knowledge base
for mathematical content processing.
"""

import logging
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import ConfigManager
from services.ragflow_service import RAGFlowService

logger = logging.getLogger(__name__)

def ingest_documents():
    """
    Ingest all documents from data/documents into the RAGFlow knowledge base.
    """
    try:
        # Initialize configuration and services
        config = ConfigManager()
        ragflow_service = RAGFlowService(config)
        
        # Check RAGFlow availability
        if not ragflow_service.is_available():
            logger.error("RAGFlow service not available")
            return False
        
        logger.info("Starting document ingestion process")
        
        # Get or create knowledge base
        kb_name = config.get("ragflow.knowledge_base", "mathematical_kb")
        kb_id = ragflow_service._get_or_create_mathematical_kb(kb_name)
        
        if not kb_id:
            logger.error("Failed to get or create knowledge base")
            return False
        
        logger.info(f"Using knowledge base: {kb_name} (ID: {kb_id})")
        
        # Find documents in data/documents
        documents_dir = Path("data/documents")
        if not documents_dir.exists():
            logger.error(f"Documents directory not found: {documents_dir}")
            return False
        
        # Upload all documents
        uploaded_count = 0
        failed_count = 0
        
        for file_path in documents_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.md', '.pdf', '.txt', '.docx']:
                logger.info(f"Uploading document: {file_path.name}")
                
                doc_id = ragflow_service.upload_document(
                    kb_id=kb_id,
                    file_path=file_path,
                    mathematical_content=True
                )
                
                if doc_id:
                    uploaded_count += 1
                    logger.info(f"Successfully uploaded: {file_path.name} (ID: {doc_id})")
                else:
                    failed_count += 1
                    logger.error(f"Failed to upload: {file_path.name}")
        
        logger.info(f"Document ingestion completed. Uploaded: {uploaded_count}, Failed: {failed_count}")
        
        # Wait for processing to complete
        if uploaded_count > 0:
            logger.info("Documents uploaded. RAGFlow will process them in the background.")
            logger.info("You can now test queries against the knowledge base.")
        
        return uploaded_count > 0
        
    except Exception as e:
        logger.error(f"Error during document ingestion: {e}")
        return False

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    success = ingest_documents()
    sys.exit(0 if success else 1) 