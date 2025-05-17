"""
ingest.py
---------
Document ingestion for LearningAgent.

Usage:
    python ingest.py --path ./docs               # ingest all supported files under ./docs
    python ingest.py --path ./docs/my.pdf        # ingest a single file
    python ingest.py --path ./docs --rebuild     # wipe & rebuild the collection
"""

import argparse
import json
import yaml
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient, models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse
from fastembed import TextEmbedding
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from rich import print as rprint
from rich.progress import Progress

# Load configuration
CONFIG_PATH = "config.yaml"

def load_config():
    """Load configuration from YAML file."""
    if not os.path.exists(CONFIG_PATH):
        rprint(f"[yellow]⚠️ Config file {CONFIG_PATH} not found, using defaults.[/yellow]")
        return {
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "collection": "kb",
        }

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
COLLECTION = CONFIG.get("collection", "kb")
EMBED_MODEL_NAME = CONFIG.get("embedding_model", "BAAI/bge-small-en-v1.5")
# Increase default chunk size and overlap to allow chunks to span multiple pages
CHUNK_SIZE = CONFIG.get("chunk_size", 2000)
CHUNK_OVERLAP = CONFIG.get("chunk_overlap", 200)

# Initialize embedding model for vector creation
embedding_model = TextEmbedding(EMBED_MODEL_NAME)
# Get embedding dimension by creating a sample embedding
VECTOR_SIZE = len(next(embedding_model.embed(["Sample text for dimension calculation"])))

def load_documents(path: str) -> List[Document]:
    """Load documents from a file or directory."""
    path_obj = Path(path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    
    documents = []
    
    if path_obj.is_file():
        # Load a single file
        documents.extend(_load_single_file(path_obj))
    else:
        # Load a directory of files
        for file_path in path_obj.glob("**/*"):
            if file_path.is_file() and _is_supported_file(file_path):
                try:
                    documents.extend(_load_single_file(file_path))
                except Exception as e:
                    rprint(f"[yellow]⚠️ Error loading {file_path}: {e}[/yellow]")
    
    # Combine document content from the same source before chunking
    combined_docs = _combine_documents_by_source(documents)
    
    rprint(f"[green]✅ Loaded {len(combined_docs)} documents[/green]")
    return combined_docs

def _combine_documents_by_source(documents: List[Document]) -> List[Document]:
    """Combine documents from the same source file to allow chunks to span multiple pages."""
    # Group documents by source
    source_docs = {}
    
    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        
        if source not in source_docs:
            source_docs[source] = []
        
        # Add document to the list for this source
        source_docs[source].append(doc)
    
    # Sort documents by page number within each source
    for source in source_docs:
        source_docs[source].sort(key=lambda x: x.metadata.get("page", 0))
    
    # Combine documents from the same source
    combined_docs = []
    for source, docs in source_docs.items():
        # Combine all pages from the source into a single document
        combined_content = ""
        # Use metadata from the first document as a base
        combined_metadata = docs[0].metadata.copy() if docs else {}
        combined_metadata["source"] = source
        combined_metadata["page_count"] = len(docs)
        
        # Combine content with page markers
        for i, doc in enumerate(docs):
            page_num = doc.metadata.get("page", i)
            # Add page marker and content
            if combined_content:
                combined_content += "\n\n"
            combined_content += doc.page_content
        
        combined_docs.append(Document(
            page_content=combined_content,
            metadata=combined_metadata
        ))
    
    return combined_docs

def _load_single_file(file_path: Path) -> List[Document]:
    """Load a single file into documents."""
    if file_path.suffix.lower() == '.pdf':
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        
        # Add additional metadata
        for doc in documents:
            doc.metadata["title"] = file_path.stem
            doc.metadata["file_type"] = "pdf"
            # Ensure page number is stored in metadata for reference
            if "page" not in doc.metadata:
                doc.metadata["page"] = doc.metadata.get("page", 0)
            
        return documents
    
    elif file_path.suffix.lower() in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml']:
        loader = TextLoader(str(file_path))
        documents = loader.load()
        
        # Add additional metadata
        for doc in documents:
            doc.metadata["title"] = file_path.stem
            doc.metadata["file_type"] = file_path.suffix.lower()[1:]  # Remove the dot
            
        return documents
    
    else:
        rprint(f"[yellow]⚠️ Unsupported file type: {file_path}[/yellow]")
        return []

def _is_supported_file(file_path: Path) -> bool:
    """Check if the file type is supported."""
    supported_extensions = ['.txt', '.md', '.pdf', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml']
    return file_path.suffix.lower() in supported_extensions

def create_chunks(documents: List[Document]) -> List[Document]:
    """Split documents into chunks for embedding, allowing chunks to span multiple pages."""
    if not documents:
        return []
    
    # Use token-based splitting for more semantic chunks
    # Increased chunk size and overlap allows for chunks to span multiple pages
    splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    
    chunks = splitter.split_documents(documents)
    
    # Add chunk index to metadata for reference
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks)
    
    rprint(f"[green]✅ Created {len(chunks)} chunks with size {CHUNK_SIZE} and overlap {CHUNK_OVERLAP}[/green]")
    return chunks

def get_or_create_collection(client: QdrantClient, name: str) -> None:
    """Get or create a Qdrant collection."""
    try:
        # Try to get the collection
        collection_info = client.get_collection(name)
        rprint(f"[green]✅ Collection '{name}' exists with {collection_info.points_count} points[/green]")
    except (UnexpectedResponse, Exception):
        # Create the collection if it doesn't exist
        client.create_collection(
            collection_name=name,
            vectors_config=qmodels.VectorParams(
                size=VECTOR_SIZE,
                distance=qmodels.Distance.COSINE
            ),
            optimizers_config=qmodels.OptimizersConfigDiff(
                indexing_threshold=0  # Index immediately
            )
        )
        rprint(f"[green]✅ Created new collection '{name}'[/green]")

def rebuild_collection(client: QdrantClient, name: str) -> None:
    """Recreate a Qdrant collection (delete and create)."""
    try:
        # Delete the collection if it exists
        client.delete_collection(name)
        rprint(f"[yellow]⚠️ Deleted existing collection '{name}'[/yellow]")
    except (UnexpectedResponse, Exception):
        # Collection does not exist
        pass
    
    # Create a new collection
    client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(
            size=VECTOR_SIZE,
            distance=qmodels.Distance.COSINE
        ),
        optimizers_config=qmodels.OptimizersConfigDiff(
            indexing_threshold=0  # Index immediately
        )
    )
    rprint(f"[green]✅ Recreated collection '{name}'[/green]")

def embed_and_upload(client: QdrantClient, chunks: List[Document], collection_name: str) -> None:
    """Embed document chunks and upload to Qdrant."""
    if not chunks:
        rprint("[yellow]⚠️ No chunks to embed[/yellow]")
        return
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Embedding and uploading...", total=len(chunks))
        
        for i in range(0, len(chunks), 10):  # Batch size 10
            batch = chunks[i:i+10]
            
            # Convert chunks to embedding vectors
            texts = [doc.page_content for doc in batch]
            embeddings = list(embedding_model.embed(texts))
            
            # Prepare the batch for Qdrant
            ids = list(range(i, i + len(batch)))
            payloads = [
                {
                    "page_content": doc.page_content,  # Include full content
                    "metadata": doc.metadata
                }
                for doc in batch
            ]
            
            # Upload to Qdrant
            client.upsert(
                collection_name=collection_name,
                points=qmodels.Batch(
                    ids=ids,
                    vectors=embeddings,
                    payloads=payloads
                )
            )
            
            progress.update(task, advance=len(batch))
    
    rprint(f"[green]✅ Embedded and uploaded {len(chunks)} chunks to Qdrant[/green]")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Ingest documents into the knowledge base")
    parser.add_argument("--path", required=True, help="Path to document file or directory")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the collection")
    parser.add_argument("--collection", default=COLLECTION, help=f"Collection name (default: {COLLECTION})")
    args = parser.parse_args()
    
    try:
        # Initialize Qdrant client
        # Try Docker connection first, fall back to embedded if needed
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Test the connection
            client.get_collections()
            rprint("[green]✅ Connected to Docker Qdrant[/green]")
        except Exception as docker_e:
            rprint(f"[yellow]⚠️ Could not connect to Docker Qdrant: {docker_e}[/yellow]")
            
            # Try embedded Qdrant as fallback
            try:
                rprint("[cyan]🔄 Trying embedded Qdrant as fallback...[/cyan]")
                client = QdrantClient(path="./qdrant_data")
                client.get_collections()
                rprint("[green]✅ Connected to embedded Qdrant[/green]")
            except Exception as e:
                rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e}[/red]")
                rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant Docker[/yellow]")
                raise RuntimeError("Could not connect to any Qdrant instance")
        
        # Setup collection
        if args.rebuild:
            rebuild_collection(client, args.collection)
        else:
            get_or_create_collection(client, args.collection)
        
        # Load and process documents
        documents = load_documents(args.path)
        chunks = create_chunks(documents)
        embed_and_upload(client, chunks, args.collection)
        
        rprint("[green bold]🎉 Ingestion complete![/green bold]")
        
    except Exception as e:
        rprint(f"[red bold]❌ Error: {e}[/red bold]")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())