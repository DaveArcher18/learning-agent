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
# import json # No longer used directly
# import yaml # No longer used directly
import os
from pathlib import Path
from typing import List, Dict, Any, Optional # Dict, Any might not be strictly needed now

# QdrantClient is now imported in qdrant_utils
# from qdrant_client import QdrantClient
from qdrant_client import models as qmodels # Keep this for qmodels usage
from qdrant_client.http.exceptions import UnexpectedResponse
from fastembed import TextEmbedding
from qdrant_utils import connect_to_qdrant # Import the new utility
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from rich import print as rprint
from rich.progress import Progress
from config_utils import ConfigManager # Import the new ConfigManager

# Initialize ConfigManager
config_manager = ConfigManager()

# Configuration values accessed via ConfigManager
# These are global for convenience within this script's functions.
# Default values are specified in ConfigManager.DEFAULT_CONFIG.
COLLECTION_NAME: str = config_manager.get("collection")
EMBED_MODEL_NAME: str = config_manager.get("embedding_model")
CHUNK_SIZE: int = config_manager.get("chunk_size")
CHUNK_OVERLAP: int = config_manager.get("chunk_overlap")

# Initialize embedding model for vector creation (global for efficiency)
embedding_model = TextEmbedding(model_name=EMBED_MODEL_NAME) 
# Determine vector size dynamically from the embedding model
try:
    VECTOR_SIZE: int = len(next(embedding_model.embed(["Sample text"])))
except Exception as e:
    rprint(f"[red]❌ Failed to determine vector size from embedding model: {e}[/red]")
    rprint("[yellow]⚠️ Defaulting VECTOR_SIZE to 384. This might be incorrect for the chosen model.[/yellow]")
    VECTOR_SIZE = 384 # Fallback, common for BAAI/bge-small-en-v1.5 but should be dynamic

def load_documents(path_str: str) -> List[Document]:
    """
    Loads documents from the specified file or directory path.
    Supports various file types (.pdf, .txt, .md, etc.).
    Combines documents from the same source before chunking.

    Args:
        path_str (str): The path to a single file or a directory.

    Returns:
        List[Document]: A list of LangChain Document objects.
        
    Raises:
        FileNotFoundError: If the provided path does not exist.
    """
    path_obj = Path(path_str)
    
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
    """
    Combines multiple Document objects that originate from the same source file
    into a single Document. This is useful for ensuring that text splitting
    can create chunks that span across what were originally separate pages (e.g., in a PDF).

    Args:
        documents (List[Document]): A list of Document objects, potentially from various sources.

    Returns:
        List[Document]: A new list of Document objects, where documents from the
                        same source are merged.
    """
    # Group documents by source
    source_docs: Dict[str, List[Document]] = {}
    
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
    """
    Loads a single file into a list of LangChain Document objects.
    Adds 'title' and 'file_type' metadata. For PDFs, 'page' metadata is preserved.

    Args:
        file_path (Path): The Path object pointing to the file.

    Returns:
        List[Document]: A list of Document objects, or an empty list if the file type
                        is unsupported or an error occurs.
    """
    file_suffix = file_path.suffix.lower()
    
    if file_suffix == '.pdf':
        loader = PyPDFLoader(str(file_path))
        try:
            documents = loader.load()
            for doc in documents: # Add common metadata
                doc.metadata["title"] = file_path.stem
                doc.metadata["file_type"] = "pdf"
                # page number is usually included by PyPDFLoader
            return documents
        except Exception as e:
            rprint(f"[red]❌ Error loading PDF {file_path}: {e}[/red]")
            return []
            
    elif file_suffix in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml']:
        loader = TextLoader(str(file_path), encoding='utf-8') # Specify encoding
        try:
            documents = loader.load()
            for doc in documents: # Add common metadata
                doc.metadata["title"] = file_path.stem
                doc.metadata["file_type"] = file_suffix[1:] # Remove the dot
            return documents
        except Exception as e:
            rprint(f"[red]❌ Error loading text file {file_path}: {e}[/red]")
            return []
    else:
        rprint(f"[yellow]⚠️ Unsupported file type skipped: {file_path.name}[/yellow]")
        return []

def _is_supported_file(file_path: Path) -> bool:
    """Checks if the file extension is in the list of supported types."""
    supported_extensions = ['.txt', '.md', '.pdf', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml']
    return file_path.suffix.lower() in supported_extensions

def create_chunks(documents: List[Document]) -> List[Document]:
    """
    Splits a list of Documents into smaller chunks suitable for embedding.
    Uses TokenTextSplitter with CHUNK_SIZE and CHUNK_OVERLAP from config.
    Adds 'chunk_index' and 'total_chunks' metadata to each chunk.

    Args:
        documents (List[Document]): The list of Document objects to split.

    Returns:
        List[Document]: A list of Document objects representing the chunks.
                       Returns an empty list if input documents is empty.
    """
    if not documents:
        rprint("[yellow]⚠️ No documents provided to create_chunks.[/yellow]")
        return []
    
    splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE,  # From global config
        chunk_overlap=CHUNK_OVERLAP # From global config
    )
    
    chunks = splitter.split_documents(documents)
    
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks) # Add total_chunks for context
    
    rprint(f"[green]✅ Created {len(chunks)} chunks (size: {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP}).[/green]")
    return chunks

def get_or_create_collection(client: 'QdrantClient', collection_name: str) -> None:
    """
    Ensures a Qdrant collection with the specified name and vector configuration exists.
    If the collection does not exist, it is created.

    Args:
        client ('QdrantClient'): The Qdrant client instance.
        collection_name (str): The name of the collection to get or create.
    """
    try:
        collection_info = client.get_collection(collection_name=collection_name) # type: ignore
        rprint(f"[green]✅ Collection '{collection_name}' already exists with {collection_info.points_count} points.[/green]") # type: ignore
    except (UnexpectedResponse, Exception) as e: # More specific exception handling if possible
        if isinstance(e, UnexpectedResponse) and e.status_code == 404: # Collection not found
            rprint(f"[cyan]Collection '{collection_name}' not found. Creating new collection...[/cyan]")
        else: # Other unexpected error during get_collection
            rprint(f"[yellow]⚠️ Could not retrieve collection info for '{collection_name}' (may not exist): {e}. Attempting to create.[/yellow]")
        
        try:
            client.create_collection( # type: ignore
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams( # type: ignore
                    size=VECTOR_SIZE, # Global VECTOR_SIZE
                    distance=qmodels.Distance.COSINE # type: ignore
                ),
                optimizers_config=qmodels.OptimizersConfigDiff(indexing_threshold=0) # type: ignore
            )
            rprint(f"[green]✅ Created new collection '{collection_name}' with VECTOR_SIZE={VECTOR_SIZE}.[/green]")
        except Exception as create_e:
            rprint(f"[red]❌ Failed to create collection '{collection_name}': {create_e}[/red]")
            raise # Re-raise after logging if creation fails

def rebuild_collection(client: 'QdrantClient', collection_name: str) -> None:
    """
    Deletes the specified collection if it exists, then creates it anew.
    This is a destructive operation.

    Args:
        client ('QdrantClient'): The Qdrant client instance.
        collection_name (str): The name of the collection to rebuild.
    """
    try:
        client.delete_collection(collection_name=collection_name) # type: ignore
        rprint(f"[yellow]⚠️ Deleted existing collection '{collection_name}'.[/yellow]")
    except (UnexpectedResponse, Exception) as e:
        if isinstance(e, UnexpectedResponse) and e.status_code == 404:
             rprint(f"[cyan]Collection '{collection_name}' did not exist. No need to delete.[/cyan]")
        else:
            rprint(f"[yellow]⚠️ Error trying to delete collection '{collection_name}' (it may not exist): {e}[/yellow]")
            # Continue to creation attempt even if delete had minor issue but wasn't "not found"
    
    # Create the new collection
    try:
        client.create_collection( # type: ignore
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams( # type: ignore
                size=VECTOR_SIZE, # Global VECTOR_SIZE
                distance=qmodels.Distance.COSINE # type: ignore
            ),
            optimizers_config=qmodels.OptimizersConfigDiff(indexing_threshold=0) # type: ignore
        )
        rprint(f"[green]✅ Recreated collection '{collection_name}' with VECTOR_SIZE={VECTOR_SIZE}.[/green]")
    except Exception as create_e:
        rprint(f"[red]❌ Failed to create collection '{collection_name}' during rebuild: {create_e}[/red]")
        raise # Re-raise if creation fails

def embed_and_upload(client: 'QdrantClient', chunks: List[Document], collection_name: str) -> None:
    """
    Embeds document chunks using the globally defined embedding model and uploads
    them to the specified Qdrant collection. Uploads are done in batches.

    Args:
        client ('QdrantClient'): The Qdrant client instance.
        chunks (List[Document]): The list of Document chunks to embed and upload.
        collection_name (str): The name of the Qdrant collection to upload to.
    """
    if not chunks:
        rprint("[yellow]⚠️ No chunks provided to embed_and_upload.[/yellow]")
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
            client.upsert( # type: ignore
                collection_name=collection_name, # type: ignore
                points=qmodels.Batch( # type: ignore
                    ids=ids, # type: ignore
                    vectors=embeddings, # type: ignore
                    payloads=payloads # type: ignore
                ) # type: ignore
            )
            
            progress.update(task, advance=len(batch)) # type: ignore
    
    rprint(f"[green]✅ Embedded and uploaded {len(chunks)} chunks to Qdrant[/green]")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Ingest documents into the knowledge base")
    parser.add_argument("--path", required=True, help="Path to document file or directory")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the collection")
    parser.add_argument("--collection", default=COLLECTION, help=f"Collection name (default: {COLLECTION})")
    args = parser.parse_args()
    
    try:
        # Initialize Qdrant client using the new utility function
        client = connect_to_qdrant()
        
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