"""
learning_agent.py
-----------------
Interactive CLI RAG assistant using:

  • Qwen-3 4B via Ollama (32k context)
  • FastEmbed + FlagEmbedding (BAAI/bge-small-en)
  • Qdrant (local, embedded) for vector search (Hybrid)
  • Exa Search MCP as web-fallback

Run:
    python learning_agent.py           # start chat
    python learning_agent.py --no-web  # disable Exa
"""

import argparse
import os
import yaml
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

# ---- LangChain core ----
try:
    from langchain_ollama import Ollama
except ImportError:
    from langchain.llms import Ollama

# Memory imports - try new path first, then fall back to old path
try:
    from langchain_core.memory import ConversationBufferMemory
except ImportError:
    from langchain.memory import ConversationBufferMemory

# Prompts imports
try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate

# Runnable imports
try:
    from langchain_core.runnables import RunnablePassthrough, RunnableParallel
except ImportError:
    from langchain.schema.runnable import RunnablePassthrough, RunnableParallel

# Chains imports
from langchain.chains import LLMChain

# ---- Vector & embeddings ----
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

from qdrant_client import QdrantClient
try:
    from langchain_qdrant import QdrantVectorStore, RetrievalMode
except ImportError:
    from langchain.vectorstores import QdrantVectorStore
    RetrievalMode = None  # Might not be available in older versions

# Multi-query retriever
try:
    from langchain_community.retrievers.multi_query import MultiQueryRetriever
except ImportError:
    from langchain.retrievers.multi_query import MultiQueryRetriever

# ---- Exa search ----
from exa_py import Exa  # Exa's official SDK


# --------------------------------------------------------------------------- #
#                               Configuration                                 #
# --------------------------------------------------------------------------- #
CONFIG_PATH = "config.yaml"


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not os.path.exists(CONFIG_PATH):
        rprint(
            f"[yellow]⚠️ Config file {CONFIG_PATH} not found, using defaults.[/yellow]"
        )
        return {
            "model": "qwen3:4b",
            "temperature": 0.3,
            "use_memory": True,
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "top_k": 5,
            "similarity_threshold": 0.5,
            "chunk_size": 2000,
            "chunk_overlap": 200,
            "use_web_fallback": True,
            "web_results": 3,
            "collection": "kb",
        }

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
COLLECTION = CONFIG.get("collection", "kb")
EMBED_MODEL_NAME = CONFIG.get("embedding_model", "BAAI/bge-small-en-v1.5")
CHUNK_SIZE = CONFIG.get("chunk_size", 2000)
CHUNK_OVERLAP = CONFIG.get("chunk_overlap", 200)
DEFAULT_TOP_K = CONFIG.get("top_k", 5)

load_dotenv()
EXA_KEY = os.getenv("EXA_API_KEY")
if not EXA_KEY and CONFIG.get("use_web_fallback", True):
    rprint("[yellow]⚠️ EXA_API_KEY not set; you can still run with --no-web[/yellow]")


# --------------------------------------------------------------------------- #
#                               Helper funcs                                  #
# --------------------------------------------------------------------------- #
def init_llm(model: str = None, temperature: float = None):
    """Return an Ollama LLM wrapped for LangChain."""
    model = model or CONFIG.get("model", "qwen3:4b")
    temperature = temperature or CONFIG.get("temperature", 0.3)
    return Ollama(model=model, temperature=temperature, timeout=120)


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
            rprint(
                "[yellow]  - Run 'make start_qdrant' to start Qdrant Docker[/yellow]"
            )
            rprint(
                "[yellow]  - Or make sure ./qdrant_data directory exists and is writable[/yellow]"
            )
            raise RuntimeError("Could not connect to any Qdrant instance")


def init_vector_store(embedder: Embedder):
    """Initialize vector store with the right Qdrant connection."""
    client = connect_to_qdrant()

    # Create a proper wrapper for embeddings
    from langchain_core.embeddings import Embeddings

    class EmbeddingWrapper(Embeddings):
        """Wrapper for embeddings that works with both old and new APIs."""

        def __init__(self, embedder):
            self.embedder = embedder

        def embed_documents(self, texts):
            results = []
            for text in texts:
                try:
                    # Try new API
                    vector = self.embedder.embed(text)
                    # Check if it's an iterator
                    if hasattr(vector, "__next__"):
                        vector = next(vector)
                    results.append(vector)
                except Exception:
                    # Fall back to old API as a batch
                    vector = self.embedder.embed([text])[0]
                    results.append(vector)
            return results

        def embed_query(self, text):
            try:
                # Try new API
                vector = self.embedder.embed(text)
                # Check if it's an iterator
                if hasattr(vector, "__next__"):
                    vector = next(vector)
                return vector
            except Exception:
                # Fall back to old API
                return self.embedder.embed([text])[0]

    # Return QdrantVectorStore with the proper parameters
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION,
        embedding=EmbeddingWrapper(embedder),
    )


def build_retriever(vector_store, llm, top_k: int):
    """Hybrid + MultiQuery expansion."""
    base = vector_store.as_retriever(search_kwargs={"k": top_k})
    return MultiQueryRetriever.from_llm(retriever=base, llm=llm)


def embed_with_fallback(embedder, text):
    """Try to embed text with fallback to handle API changes."""
    try:
        # Try new API
        vector = embedder.embed(text)
        # Check if it's an iterator
        if hasattr(vector, "__next__"):
            vector = next(vector)
    except Exception:
        # Fall back to old API
        vector = embedder.embed(text)
    return vector


def web_fallback(query: str, n_results: int = 3) -> str:
    """Call Exa MCP to fetch web content."""
    if not EXA_KEY:
        rprint(
            "[yellow]⚠️ No Exa API key found. Set EXA_API_KEY env variable for web search.[/yellow]"
        )
        return ""

    try:
        exa = Exa(api_key=EXA_KEY)
        results = exa.search_and_contents(
            query,
            num_results=n_results,
            use_autoprompt=True,
            text=True,
        )

        # Store web results in vector DB for future reference
        web_texts = [res["content"] for res in results[:n_results]]
        if web_texts:
            try:
                from langchain_core.documents import Document
                from langchain_text_splitters.text_splitter import TokenTextSplitter

                # Process web results like other documents
                docs = [
                    Document(page_content=text, metadata={"source": "web"})
                    for text in web_texts
                ]

                # Split into chunks
                splitter = TokenTextSplitter(
                    chunk_size=CHUNK_SIZE,
                    chunk_overlap=CHUNK_OVERLAP,
                    model_name="gpt-3.5-turbo",
                )
                chunks = splitter.split_documents(docs)

                # Get embedder and client
                embedder = Embedder(EMBED_MODEL_NAME)
                client = QdrantClient(path="./qdrant_data")

                # Create batch of embeddings and payloads
                batch_vectors = []
                payloads = []
                for doc in chunks:
                    batch_vectors.append(
                        embed_with_fallback(embedder, doc.page_content)
                    )
                    payloads.append({"source": "web", "query": query})

                # Use a timestamp-based ID to avoid collisions
                import time

                start_id = int(time.time() * 1000)

                # Upsert to Qdrant
                from qdrant_client import models as qmodels

                client.upsert(
                    collection_name=COLLECTION,
                    points=[
                        qmodels.PointStruct(
                            id=start_id + i, vector=v, payload=payloads[i]
                        )
                        for i, v in enumerate(batch_vectors)
                    ],
                )
                rprint(
                    f"[green]✅ Stored {len(batch_vectors)} web result chunks in vector DB[/green]"
                )
            except Exception as e:
                rprint(f"[yellow]⚠️ Could not store web results: {e}[/yellow]")

        return "\n\n".join(web_texts)
    except Exception as e:
        rprint(f"[red]❌ Error during web search: {e}[/red]")
        return ""


def process_command(cmd: str, args: str, state: Dict[str, Any]) -> bool:
    """Process CLI commands. Returns True if normal input, False to exit."""
    if cmd == ":exit":
        return False

    if cmd == ":ingest":
        if not args:
            rprint("[red]⚠️ Path required: :ingest PATH[/red]")
            return True

        path = args.strip()
        rprint(f"[cyan]📚 Ingesting documents from {path}...[/cyan]")
        # Import here to avoid circular imports
        from ingest import load_files, split_documents

        try:
            raw_docs = load_files(Path(path))
            chunks = split_documents(raw_docs)
            embedder = state.get("embedder")

            # Create batch of embeddings and payloads
            batch_vectors = []
            payloads = []
            for doc in chunks:
                batch_vectors.append(embed_with_fallback(embedder, doc.page_content))
                payloads.append({"source": doc.metadata.get("source", "local")})

            # Upsert to Qdrant
            client = QdrantClient(path="./qdrant_data")
            from qdrant_client import models as qmodels

            client.upsert(
                collection_name=COLLECTION,
                points=[
                    qmodels.PointStruct(id=i + 10000, vector=v, payload=payloads[i])
                    for i, v in enumerate(batch_vectors)
                ],
            )
            rprint(f"[green]✅ Added {len(batch_vectors)} chunks from {path}[/green]")
        except Exception as e:
            rprint(f"[red]❌ Error ingesting documents: {e}[/red]")
        return True

    if cmd == ":config":
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        for key, value in CONFIG.items():
            table.add_row(key, str(value))

        # Add runtime settings
        table.add_row("memory_enabled", str(state.get("memory_enabled", False)))
        table.add_row("web_fallback_enabled", str(state.get("web_fallback", False)))

        rprint(table)
        return True

    if cmd == ":memory":
        if args.lower() in ("off", "false", "0"):
            state["memory_enabled"] = False
            state["memory"] = None
            rprint("[cyan]🧠 Memory disabled[/cyan]")
        elif args.lower() in ("on", "true", "1"):
            state["memory_enabled"] = True
            state["memory"] = ConversationBufferMemory(return_messages=True)
            rprint("[cyan]🧠 Memory enabled[/cyan]")
        else:
            rprint(
                f"[cyan]🧠 Memory is currently {'enabled' if state.get('memory_enabled') else 'disabled'}[/cyan]"
            )
        return True

    # If not a command, treat as normal input
    return True


# --------------------------------------------------------------------------- #
#                               Main chat loop                                #
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description="LearningAgent CLI")
    parser.add_argument("--no-web", action="store_true", help="Disable Exa web search")
    parser.add_argument(
        "--no-memory", action="store_true", help="Disable conversation memory"
    )
    parser.add_argument(
        "--top-k", type=int, default=DEFAULT_TOP_K, help="Top-k retrieval"
    )
    args = parser.parse_args()

    rprint(
        Panel(
            "🚀 [bold cyan]LearningAgent Ready[/bold cyan]\nType ':exit' to quit, ':config' to show settings.",
            border_style="cyan",
        )
    )

    # LLM & retriever
    llm = init_llm()
    embedder = Embedder(EMBED_MODEL_NAME)
    vector_store = init_vector_store(embedder)
    retriever = build_retriever(vector_store, llm, args.top_k)

    # Simple QA prompt
    qa_prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the question.\n"
        "If you don't know, say so.\n\n"
        "Context:\n{context}\n\n"
        "{history}\n\n"
        "Question: {question}\nAnswer:"
    )
    qa_chain = LLMChain(llm=llm, prompt=qa_prompt)

    # State dictionary to hold runtime config
    state = {
        "memory_enabled": not args.no_memory and CONFIG.get("use_memory", True),
        "web_fallback": not args.no_web and CONFIG.get("use_web_fallback", True),
        "top_k": args.top_k,
        "embedder": embedder,
    }

    # Setup memory if enabled
    if state["memory_enabled"]:
        state["memory"] = ConversationBufferMemory(return_messages=True)
        # Memory is enabled by default in config.yaml
        rprint("[cyan]🧠 Memory enabled and will be stored in vector DB[/cyan]")
    else:
        state["memory"] = None

    # CLI loop
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        # Check if this is a command
        if user_input.startswith(":"):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            if not process_command(cmd, args, state):
                break
            continue

        # ===== Retrieval phase =====
        docs = retriever.invoke(user_input)
        if isinstance(docs, list):
            context_texts = [d.page_content for d in docs]
        else:
            context_texts = []

        if not context_texts and state["web_fallback"]:
            rprint(
                "[yellow]🔍 No local results – falling back to web search...[/yellow]"
            )
            web_ctx = web_fallback(user_input, n_results=CONFIG.get("web_results", 3))
            context_texts = [web_ctx] if web_ctx else []

        if not context_texts:
            rprint(
                "[red]😕 I couldn't find relevant information. Try ingesting more docs or enabling web search.[/red]"
            )
            continue

        context = "\n\n---\n\n".join(context_texts)

        # Get conversation history if memory is enabled
        history = ""
        if state.get("memory"):
            memory_buffer = state["memory"].buffer
            if memory_buffer:
                history = "Previous conversation:\n" + memory_buffer

        # ===== LLM phase =====
        answer = qa_chain.run(
            {"context": context, "question": user_input, "history": history}
        )
        rprint(Panel.fit(answer, title="Assistant", border_style="green"))

        if state.get("memory"):
            state["memory"].save_context({"input": user_input}, {"output": answer})

            # Store conversation in vector DB for future reference
            try:
                from langchain_core.documents import Document

                # Create document from conversation turn
                conv_doc = Document(
                    page_content=f"Q: {user_input}\nA: {answer}",
                    metadata={"source": "conversation", "type": "memory"},
                )

                # Get embedder and client
                embedder = state["embedder"]
                client = connect_to_qdrant()

                # Create embedding
                vector = embed_with_fallback(embedder, conv_doc.page_content)

                # Use a timestamp-based ID to avoid collisions
                import time

                doc_id = int(time.time() * 1000)

                # Upsert to Qdrant
                from qdrant_client import models as qmodels

                client.upsert(
                    collection_name=COLLECTION,
                    points=[
                        qmodels.PointStruct(
                            id=doc_id, vector=vector, payload=conv_doc.metadata
                        )
                    ],
                )
            except Exception as e:
                rprint(f"[yellow]⚠️ Could not store conversation: {e}[/yellow]")


if __name__ == "__main__":
    main()
