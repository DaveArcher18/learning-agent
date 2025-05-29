"""
RAGFlow Setup Module

Initialize RAGFlow with mathematical content processing optimizations.
This module sets up the knowledge base with BGE-M3 embeddings and
mathematical content parsing.
"""

import logging
import os
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


def setup_mathematical_kb(kb_name: str = None) -> Dict[str, Any]:
    """
    Set up RAGFlow knowledge base optimized for mathematical content.
    
    Args:
        kb_name: Name of the knowledge base (defaults to config value)
        
    Returns:
        Setup status and configuration details
    """
    try:
        from src.rag.processing.ragflow_ingest import RAGFlowIngestor
        import yaml
        
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        kb_name = kb_name or config.get('ragflow', {}).get('knowledge_base', 'mathematical_kb')
        
        logger.info(f"Setting up mathematical knowledge base: {kb_name}")
        
        # Initialize RAGFlow ingestor with simplified client
        ingestor = RAGFlowIngestor()
        
        # Check if we can connect to a RAGFlow service
        client = ingestor.ragflow_client
        health = client.health_check()
        
        if health['status'] == 'healthy':
            logger.info("✅ RAGFlow service is healthy")
            
            # Create or get knowledge base
            kb = ingestor.get_or_create_knowledge_base(kb_name)
            
            kb_info = {
                'name': kb_name,
                'status': 'ready',
                'endpoint': ingestor.endpoint,
                'service_health': 'healthy',
                'embedding_model': 'BAAI/bge-m3',
                'mathematical_processing': True,
                'layout_parsing': True,
                'citation_support': True
            }
        else:
            logger.warning(f"RAGFlow service not available: {health}")
            # Still set up for future use
            kb_info = {
                'name': kb_name,
                'status': 'configured_offline',
                'endpoint': ingestor.endpoint,
                'service_health': health['status'],
                'error': health.get('error', 'Service not responding'),
                'embedding_model': 'BAAI/bge-m3',
                'mathematical_processing': True,
                'layout_parsing': True,
                'citation_support': True,
                'note': 'Knowledge base configured but RAGFlow service not available'
            }
        
        logger.info("✅ Mathematical knowledge base setup completed")
        logger.info(f"📊 Knowledge base: {kb_name}")
        logger.info(f"🔗 Endpoint: {ingestor.endpoint}")
        logger.info(f"🏥 Service status: {kb_info['service_health']}")
        logger.info("🧮 Mathematical content processing: Enabled")
        logger.info("📄 Layout-aware parsing: Enabled")
        logger.info("📚 Citation tracking: Enabled")
        
        return kb_info
        
    except Exception as e:
        logger.error(f"Failed to setup mathematical knowledge base: {e}")
        
        # Return a fallback configuration
        fallback_info = {
            'name': kb_name or 'mathematical_kb',
            'status': 'error',
            'error': str(e),
            'note': 'Setup failed, but configuration preserved for retry'
        }
        
        return fallback_info


def verify_ragflow_health() -> Dict[str, Any]:
    """
    Verify RAGFlow service health and configuration.
    
    Returns:
        Health status and service information
    """
    try:
        from src.rag.processing.ragflow_ingest import SimpleRAGFlowClient
        
        endpoint = os.getenv('RAGFLOW_ENDPOINT', 'http://localhost:9380')
        client = SimpleRAGFlowClient(endpoint)
        
        health = client.health_check()
        
        if health['status'] == 'healthy':
            logger.info("✅ RAGFlow health check passed")
        elif health['status'] == 'degraded':
            logger.warning(f"RAGFlow service is degraded")
        else:
            logger.warning(f"RAGFlow service is unhealthy: {health}")
            
        return {
            'status': health['status'],
            'endpoint': endpoint,
            **health
        }
            
    except Exception as e:
        logger.error(f"Error during health verification: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'endpoint': os.getenv('RAGFLOW_ENDPOINT', 'http://localhost:9380')
        }


def ingest_documents_to_ragflow(docs_path: str = "./docs", kb_name: str = None) -> Dict[str, Any]:
    """
    Ingest documents from a directory into RAGFlow.
    
    Args:
        docs_path: Path to documents directory
        kb_name: Knowledge base name (defaults to config)
        
    Returns:
        Ingestion results and status
    """
    try:
        from pathlib import Path
        from src.rag.processing.ragflow_ingest import RAGFlowIngestor
        import yaml
        
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        kb_name = kb_name or config.get('ragflow', {}).get('knowledge_base', 'mathematical_kb')
        docs_directory = Path(docs_path)
        
        if not docs_directory.exists():
            return {
                'status': 'error',
                'error': f"Documents directory not found: {docs_path}"
            }
        
        logger.info(f"Starting document ingestion from {docs_path}")
        
        # Initialize ingestor
        ingestor = RAGFlowIngestor()
        
        # Check service health first
        health = ingestor.ragflow_client.health_check()
        if health['status'] != 'healthy':
            logger.warning(f"RAGFlow service not healthy: {health}")
            return {
                'status': 'service_unavailable',
                'health': health,
                'note': 'Cannot ingest documents - RAGFlow service not available'
            }
        
        # Ingest documents
        results = ingestor.ingest_directory(docs_directory, kb_name)
        
        logger.info(f"✅ Document ingestion completed: {results.get('total_processed', 0)} documents")
        return results
        
    except Exception as e:
        logger.error(f"Error during document ingestion: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Setting up RAGFlow mathematical knowledge base...")
    
    # Verify health first
    health = verify_ragflow_health()
    print(f"🏥 RAGFlow health: {health['status']}")
    
    # Setup knowledge base (works whether service is available or not)
    result = setup_mathematical_kb()
    print(f"✅ Setup completed: {result['name']} - Status: {result['status']}")
    
    # Try document ingestion if service is healthy
    if health['status'] == 'healthy':
        print("📚 Starting document ingestion...")
        ingest_result = ingest_documents_to_ragflow()
        print(f"📚 Ingestion result: {ingest_result['status']}")
    else:
        print("⚠️ Skipping document ingestion - service not available") 