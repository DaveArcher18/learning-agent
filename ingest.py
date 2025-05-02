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
import os

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
    files_to_process = [path] if path.is_file() else list(path.rglob("*"))
    
    for file in files_to_process:
        if file.is_dir():
            continue
        suffix = file.suffix.lower()
        try:
            if suffix == ".pdf":
                rprint(f"[cyan]📄 Loading PDF: {file}[/cyan]")
                try:
                    # Direct PyPDF reader approach (most reliable)
                    from pypdf import PdfReader
                    reader = PdfReader(str(file))
                    rprint(f"[green]✅ PDF has {len(reader.pages)} pages[/green]")
                    
                    for i, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if text and text.strip():  # Only add non-empty pages
                            docs.append(Document(
                                page_content=text.strip(),
                                metadata={"source": str(file), "page": i+1}
                            ))
                            rprint(f"[green]✅ Extracted page {i+1}: {len(text)} chars[/green]")
                        else:
                            rprint(f"[yellow]⚠️ Page {i+1} has no extractable text[/yellow]")
                except Exception as pdf_err:
                    rprint(f"[red]❌ Failed to read PDF: {pdf_err}[/red]")
                    # Try using LangChain loaders as fallback
                    try:
                        rprint("[yellow]⚠️ Trying PyPDFLoader as fallback...[/yellow]")
                        docs.extend(PyPDFLoader(str(file)).load())
                    except Exception as lc_err:
                        rprint(f"[red]❌ PyPDFLoader also failed: {lc_err}[/red]")
                        raise
            elif suffix in {".md", ".txt"}:
                rprint(f"[cyan]📄 Loading text file: {file}[/cyan]")
                docs.extend(TextLoader(str(file), encoding="utf-8").load())
            elif suffix == ".json":
                rprint(f"[cyan]📄 Loading JSON file: {file}[/cyan]")
                # load entire json as a string; user can customise
                with open(file, encoding="utf-8") as f:
                    docs.append(
                        Document(page_content=json.dumps(json.load(f), indent=2))
                    )
            elif suffix in {".docx", ".doc"}:
                rprint(f"[cyan]📄 Loading Word document: {file}[/cyan]")
                try:
                    from langchain_community.document_loaders import Docx2txtLoader
                    docs.extend(Docx2txtLoader(str(file)).load())
                    rprint(f"[green]✅ Successfully loaded Word document: {file}[/green]")
                except Exception as docx_err:
                    rprint(f"[red]❌ Failed to load Word document: {docx_err}[/red]")
                    # Try alternative docx loader
                    try:
                        from langchain_community.document_loaders import UnstructuredWordDocumentLoader
                        docs.extend(UnstructuredWordDocumentLoader(str(file)).load())
                        rprint(f"[green]✅ Successfully loaded Word document with UnstructuredLoader: {file}[/green]")
                    except Exception as unstr_err:
                        rprint(f"[red]❌ All Word document loaders failed: {unstr_err}[/red]")
                        raise
            elif suffix in {".pptx", ".ppt"}:
                rprint(f"[cyan]📄 Loading PowerPoint presentation: {file}[/cyan]")
                try:
                    from langchain_community.document_loaders import UnstructuredPowerPointLoader
                    docs.extend(UnstructuredPowerPointLoader(str(file)).load())
                    rprint(f"[green]✅ Successfully loaded PowerPoint: {file}[/green]")
                except Exception as ppt_err:
                    rprint(f"[red]❌ Failed to load PowerPoint: {ppt_err}[/red]")
                    raise
            elif suffix in {".html", ".htm"}:
                rprint(f"[cyan]📄 Loading HTML file: {file}[/cyan]")
                try:
                    from langchain_community.document_loaders import BSHTMLLoader
                    docs.extend(BSHTMLLoader(str(file)).load())
                    rprint(f"[green]✅ Successfully loaded HTML: {file}[/green]")
                except Exception as html_err:
                    rprint(f"[red]❌ Failed to load HTML: {html_err}[/red]")
                    raise
            else:
                rprint(f"[yellow]⚠️ Unsupported file type: {suffix}[/yellow]")
        except Exception as err:  # noqa: BLE001
            rprint(f"[red]❌ Failed to process {file}: {err}[/red]")
    
    rprint(f"[green]✅ Successfully loaded {len(docs)} documents[/green]")
    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        model_name="gpt-3.5-turbo", #This is correct! Do not change it.
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
    """Connect to Qdrant, prioritizing Docker over embedded."""
    # Try Docker connection first (preferred for reliability)
    try:
        client = QdrantClient(host="localhost", port=6333)
        # Quick test to make sure it works
        client.get_collections()
        rprint("[green]✅ Connected to Docker Qdrant[/green]")
        return client
    except Exception as docker_e:
        rprint(f"[yellow]⚠️ Could not connect to Docker Qdrant: {docker_e}[/yellow]")
        rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant Docker[/yellow]")
        
        # Try embedded Qdrant as fallback
        try:
            rprint("[cyan]🔄 Trying embedded Qdrant as fallback...[/cyan]")
            client = QdrantClient(path="./qdrant_data")
            # Quick test to make sure it works
            client.get_collections()
            rprint("[green]✅ Connected to embedded Qdrant[/green]")
            return client
        except Exception as e:
            rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e}[/red]")
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
            
    # For individual files, verify it exists and is readable
    if root.is_file():
        if not os.access(root, os.R_OK):
            raise SystemExit(f"File {root} exists but is not readable")
        rprint(f"[green]✅ Found file {root} ({root.stat().st_size} bytes)[/green]")

    if not list(root.glob('*')) and not root.is_file() and (args.path == "./docs" or args.path == "docs"):
        rprint("[yellow]⚠️ No files found in docs directory. Add some files and try again.[/yellow]")
        rprint("[green]✅ Directory exists and is ready for documents.[/green]")
        return

    rprint(f"[cyan]🔍 Loading documents from {root}...[/cyan]")
    
    try:
        raw_docs = load_files(root)
    except Exception as e:
        import traceback
        rprint(f"[red]❌ Error during document loading: {e}[/red]")
        rprint(f"[red]{traceback.format_exc()}[/red]")
        return
    
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
        # Store both metadata and content in the payload
        payload = {
            "source": doc.metadata.get("source", "local"),
            "page_content": doc.page_content
        }
        # Add any additional metadata fields
        for key, value in doc.metadata.items():
            if key != "source":
                payload[key] = value
                
        payloads.append(payload)

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