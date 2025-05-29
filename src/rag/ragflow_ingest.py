"""
Simple wrapper for RAGFlow document ingestion.
This module provides convenience functions for ingesting documents.
"""

from pathlib import Path
from src.rag.processing.ragflow_ingest import RAGFlowIngestor


def ingest_documents(docs_dir: str = './docs', kb_name: str = 'mathematical_kb'):
    """
    Ingest all documents from the specified directory into RAGFlow.
    
    Args:
        docs_dir: Directory containing documents to ingest
        kb_name: Name of the knowledge base
    """
    print(f"📚 Starting document ingestion from {docs_dir}")
    
    ingestor = RAGFlowIngestor()
    docs_path = Path(docs_dir)
    
    result = ingestor.ingest_directory(docs_path, kb_name)
    
    print(f"✅ Ingestion completed:")
    print(f"  Total files: {result.get('total_files', 0)}")
    print(f"  Successful: {result.get('successful', 0)}")
    print(f"  Failed: {result.get('failed', 0)}")
    
    return result


if __name__ == "__main__":
    ingest_documents() 