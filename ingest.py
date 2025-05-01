"""
ingest.py
--------- 
One‑shot (or repeatable) document ingestion for LearningAgent.

Usage:
    python ingest.py --path ./docs               # ingest all supported files under ./docs
    python ingest.py --path ./docs/my.pdf        # ingest a single file
    python ingest.py --path ./docs --rebuild     # wipe & rebuild the collection
    python ingest.py -h                          # help

This script:
1. Loads PDFs, markdown, plaintext, JSON.
2. Splits into 2000‑token chunks (200‑token overlap) using TokenTextSplitter.
3. Generates embeddings with FastEmbed + FlagEmbedding (CPU efficient).
4. Stores vectors in a local Qdrant collection called ``kb``.
"""

import argparse
import json
from pathlib import Path
from typing import List

from qdrant_client import QdrantClient, models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse
try:
    # Use newer TextEmbedding (recommended)
    from fastembed import TextEmbedding as Embedder
except ImportError:
    try:
        # Try legacy FlagEmbedding
        from fastembed import FlagEmbedding as Embedder
    except ImportError:
        # Try the oldest location
        from fastembed.embedding import FlagEmbedding as Embedder

# Newer langchain has moved loaders to community package
try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
except ImportError:
    # Fall back to old import path
    from langchain.document_loaders import PyPDFLoader, TextLoader

# Documents import
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.docstore.document import Document

# Text splitter import
try:
    from langchain_text_splitters.text_splitter import TokenTextSplitter
except ImportError:
    from langchain.text_splitter import TokenTextSplitter

from rich import print as rprint


# ---------- Constants ---------------------------------------------------------
COLLECTION = "kb"
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200

# ---------- Helpers -----------------------------------------------------------
def load_files(path: Path) -> List[Document]:
    """Recursively load supported files into LangChain Document objects."""
    docs: List[Document] = []
    for file in path.rglob("*"):
        if file.is_dir():
            continue
        suffix = file.suffix.lower()
        try:
            if suffix == ".pdf":
                docs.extend(PyPDFLoader(str(file)).load())
            elif suffix in {".md", ".txt"}:
                docs.extend(TextLoader(str(file), encoding="utf-8").load())
            elif suffix == ".json":
                # load entire json as a string; user can customise
                with open(file, encoding="utf-8") as f:
                    docs.append(
                        Document(page_content=json.dumps(json.load(f), indent=2))
                    )
        except Exception as err:  # noqa: BLE001
            rprint(f"[yellow]⚠️  Skipped {file}: {err}[/yellow]")
    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        model_name="gpt-3.5-turbo",  # Use a well-known model as tokenizer
    )
    return splitter.split_documents(docs)


def ensure_collection(client: QdrantClient, size: int, rebuild: bool = False) -> None:
    if rebuild:
        try:
            client.delete_collection(collection_name=COLLECTION)
            rprint(f"[cyan]🗑️  Deleted existing collection '{COLLECTION}'.[/cyan]")
        except UnexpectedResponse:
            pass  # not existing = fine

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=qmodels.VectorParams(
                size=size, distance=qmodels.Distance.COSINE
            ),
        )
        rprint(f"[green]✅ Created collection '{COLLECTION}'.[/green]")


def connect_to_qdrant():
    """Try to connect to Qdrant, first embedded then Docker."""
    # Try embedded Qdrant first
    try:
        client = QdrantClient(path="./qdrant_data")
        # Quick test to make sure it works
        client.get_collections()
        rprint("[green]✅ Connected to embedded Qdrant[/green]")
        return client
    except Exception as e:
        rprint(f"[yellow]⚠️ Could not connect to embedded Qdrant: {e}[/yellow]")
        rprint("[cyan]🔄 Trying Docker Qdrant connection...[/cyan]")
        
        # Try Docker connection
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Simple health check
            client.get_collections()
            rprint("[green]✅ Connected to Docker Qdrant[/green]")
            return client
        except Exception as docker_e:
            rprint(f"[red]❌ Failed to connect to Docker Qdrant: {docker_e}[/red]")
            rprint("[yellow]💡 Tips:[/yellow]")
            rprint("[yellow]  - Run 'make start_qdrant' to start Qdrant Docker[/yellow]")
            rprint("[yellow]  - Or make sure ./qdrant_data directory exists and is writable[/yellow]")
            raise RuntimeError("Could not connect to any Qdrant instance")


# ---------- Main --------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into Qdrant.")
    parser.add_argument(
        "--path",
        required=True,
        help="File or directory with documents to ingest.",
    )
    parser.add_argument(
        "--rebuild", action="store_true", help="Drop and recreate the collection."
    )
    args = parser.parse_args()

    root = Path(args.path).expanduser()
    if not root.exists():
        # Create directory if it doesn't exist
        if args.path == "./docs" or args.path == "docs":
            rprint(f"[yellow]⚠️ Path {root} does not exist, creating it[/yellow]")
            root.mkdir(parents=True, exist_ok=True)
        else:
            raise SystemExit(f"Path {root} does not exist")

    if not list(root.glob('*')) and (args.path == "./docs" or args.path == "docs"):
        rprint("[yellow]⚠️ No files found in docs directory. Add some files and try again.[/yellow]")
        rprint("[green]✅ Directory exists and is ready for documents.[/green]")
        return

    rprint(f"[cyan]🔍 Loading documents from {root}...[/cyan]")
    raw_docs = load_files(root)
    
    if not raw_docs:
        rprint("[yellow]⚠️ No documents were loaded. Check file types and permissions.[/yellow]")
        return
        
    rprint(f"[cyan]   Loaded {len(raw_docs)} document objects.[/cyan]")

    rprint("[cyan]🔪 Splitting into token chunks...[/cyan]")
    docs = split_documents(raw_docs)
    rprint(f"[cyan]   Produced {len(docs)} chunks.[/cyan]")

    rprint("[cyan]⚙️  Initialising embedder...[/cyan]")
    embedder = Embedder(EMBED_MODEL_NAME)
    
    # Get dimension size
    try:
        # New API
        dim = embedder.dimensions
    except AttributeError:
        try:
            # Older API
            dim = embedder.embedding_size
        except AttributeError:
            # Determine by embedding a test string
            test_vec = embedder.embed("test")
            if hasattr(test_vec, "__len__"):
                dim = len(test_vec)
            else:
                # It's probably an iterator
                dim = len(next(test_vec))
    
    rprint(f"[cyan]   Using {dim}-dimensional embeddings.[/cyan]")

    rprint("[cyan]🗄️  Connecting to Qdrant...[/cyan]")
    client = connect_to_qdrant()
    ensure_collection(client, size=dim, rebuild=args.rebuild)

    rprint("[cyan]🔢 Generating embeddings & upserting...[/cyan]")
    batch_vectors = []
    payloads = []
    
    # Handle both old and new API for embedding
    for doc in docs:
        try:
            # Try new API
            vector = embedder.embed(doc.page_content)
            # Check if it's an iterator
            if hasattr(vector, "__next__"):
                vector = next(vector)
        except Exception:
            # Fall back to old API
            vector = embedder.embed(doc.page_content)
            
        batch_vectors.append(vector)
        payloads.append({"source": doc.metadata.get("source", "local")})

    client.upsert(
        collection_name=COLLECTION,
        points=[
            qmodels.PointStruct(id=i, vector=v, payload=payloads[i])
            for i, v in enumerate(batch_vectors)
        ],
    )
    rprint(f"[green]✅ Ingestion complete. Inserted {len(batch_vectors)} vectors.[/green]")


if __name__ == "__main__":
    main()