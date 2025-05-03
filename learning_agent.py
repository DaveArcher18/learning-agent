"""
learning_agent.py
-----------------
Interactive CLI RAG assistant using:

  • Qwen-3 4B via Ollama (32k context)
  • OpenRouter supported models (optional)
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
import warnings
import re
import numpy as np
from pathlib import Path
from typing import List, Dict, Any

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*was deprecated.*")
warnings.filterwarnings("ignore", message=".*TOKENIZERS_PARALLELISM.*")

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

# ---- LangChain core ----
# Ollama import is handled in get_llm() function now

# Memory imports - try new path first, then fall back to old path
try:
    from langchain.memory import ConversationBufferMemory
except ImportError:
    try:
        from langchain_core.memory import ConversationBufferMemory
    except ImportError:
        from langchain_community.memory import ConversationBufferMemory

# Prompts imports
try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain_community.prompts import PromptTemplate

# Runnable imports
try:
    from langchain_core.runnables import RunnablePassthrough, RunnableParallel
except ImportError:
    from langchain_community.schema.runnable import RunnablePassthrough, RunnableParallel

# Chains imports
try:
    from langchain.chains import LLMChain
except ImportError:
    from langchain_core.chains import LLMChain

# ---- Vector & embeddings ----
try:
    # Import fastembed directly - new API
    import fastembed
    Embedder = fastembed.TextEmbedding
except ImportError:
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
    from langchain_community.vectorstores import QdrantVectorStore
    RetrievalMode = None  # Might not be available in older versions

# Multi-query retriever
try:
    from langchain.retrievers.multi_query import MultiQueryRetriever
except ImportError:
    try:
        from langchain_community.retrievers.multi_query import MultiQueryRetriever
    except ImportError:
        from langchain.retrievers import MultiQueryRetriever

# ---- Exa search ----
from exa_py import Exa  # Exa's official SDK

# ---- Text splitters ----
try:
    from langchain_text_splitters import TokenTextSplitter, CharacterTextSplitter
except ImportError:
    # Fall back to community package if needed
    from langchain_community.text_splitters import TokenTextSplitter, CharacterTextSplitter


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
            "model_provider": "ollama",
            "openrouter_model": "deepseek/deepseek-prover-v2:free",
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Actually OpenRouter API key
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")

if not EXA_KEY and CONFIG.get("use_web_fallback", True):
    rprint("[yellow]⚠️ EXA_API_KEY not set; you can still run with --no-web[/yellow]")

# Print more detailed OpenRouter API key information for debugging
if CONFIG.get("model_provider") == "openrouter":
    if not OPENAI_API_KEY:
        rprint("[red]⚠️ OPENAI_API_KEY not set in .env; needed for OpenRouter models[/red]")
        rprint("[yellow]💡 Create a .env file with OPENAI_API_KEY=your_openrouter_key[/yellow]")
        rprint("[yellow]💡 Make sure to run 'source .env' or restart your terminal after creating .env[/yellow]")
    else:
        rprint(f"[green]✅ Found OPENAI_API_KEY (length: {len(OPENAI_API_KEY)})[/green]")


# --------------------------------------------------------------------------- #
#                               Helper funcs                                  #
# --------------------------------------------------------------------------- #
def get_llm(model=None, temperature=None):
    """Create an LLM instance based on the configured provider."""
    model_provider = CONFIG.get("model_provider", "ollama")
    model = model or CONFIG.get("model", "qwen3:4b")
    temperature = temperature or CONFIG.get("temperature", 0.3)
    
    if model_provider == "openrouter":
        # Use OpenRouter through the OpenAI interface
        openrouter_model = CONFIG.get("openrouter_model", "deepseek/deepseek-prover-v2:free")
        
        if not OPENAI_API_KEY:
            rprint("[red]❌ Missing OPENAI_API_KEY in .env for OpenRouter[/red]")
            rprint("[yellow]💡 Add OPENAI_API_KEY=your_openrouter_key to .env[/yellow]")
            rprint("[yellow]💡 Then either:                                    [/yellow]")
            rprint("[yellow]   - Run 'source .env' in your terminal            [/yellow]")
            rprint("[yellow]   - Close and reopen your terminal                [/yellow]")
            rprint("[yellow]   - Export directly: export OPENAI_API_KEY=value  [/yellow]")
            raise ValueError("OpenRouter API key not found in environment")
        
        try:
            # Import OpenAI integration from LangChain
            try:
                from langchain_openai import ChatOpenAI
            except ImportError:
                from langchain_community.chat_models import ChatOpenAI
            
            rprint(f"[green]🔄 Using OpenRouter model: {openrouter_model}[/green]")
            
            # Get headers from environment variables or use defaults
            http_referer = os.getenv("HTTP_REFERER", "LearningAgent")
            x_title = os.getenv("X_TITLE", "LearningAgent")
            
            # Test the API key first with a simple validation request
            try:
                import openai
                from openai import OpenAI
                
                # Set up a minimal client to test authentication
                test_client = OpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url=OPENAI_API_BASE
                )
                
                # Get models list as a simple authentication test
                try:
                    test_client.models.list(limit=1)
                    rprint("[green]✅ OpenRouter authentication successful[/green]")
                except Exception as auth_e:
                    # If models list fails, try a more basic authentication test
                    test_client.with_options(timeout=5.0).chat.completions.create(
                        model=openrouter_model,
                        messages=[{"role": "system", "content": "test"}],
                        max_tokens=1
                    )
                    rprint("[green]✅ OpenRouter authentication successful[/green]")
            except Exception as test_e:
                rprint(f"[red]❌ OpenRouter authentication failed: {test_e}[/red]")
                rprint(f"[yellow]💡 Make sure your API key is correct and properly exported[/yellow]")
                raise ValueError(f"OpenRouter authentication failed: {test_e}")
            
            return ChatOpenAI(
                model=openrouter_model,
                temperature=temperature,
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_API_BASE,
                timeout=120,
                max_retries=3,
                model_kwargs={
                    "extra_headers": {
                        "HTTP-Referer": http_referer,
                        "X-Title": x_title
                    }
                }
            )
        except Exception as e:
            rprint(f"[red]❌ Error initializing OpenRouter: {e}[/red]")
            rprint("[yellow]💡 Falling back to Ollama...[/yellow]")
            model_provider = "ollama"  # Fallback to Ollama
    
    # Use Ollama (either as primary choice or fallback)
    if model_provider == "ollama":
        # Try to use OllamaLLM (the new recommended class)
        try:
            from langchain_ollama import OllamaLLM
            return OllamaLLM(model=model, temperature=temperature, timeout=120)
        except ImportError:
            # Fall back to Ollama if OllamaLLM isn't available
            try:
                from langchain_ollama import Ollama
                return Ollama(model=model, temperature=temperature, timeout=120)
            except ImportError:
                # Last resort fallback
                from langchain_community.llms import Ollama
                return Ollama(model=model, temperature=temperature, timeout=120)


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
        rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant in Docker[/yellow]")
        
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
    """Hybrid + MultiQuery expansion with similarity threshold."""
    similarity_threshold = CONFIG.get("similarity_threshold", 0.5)
    # Base retriever with similarity threshold filter
    if hasattr(vector_store, "as_retriever") and hasattr(vector_store.as_retriever, "__call__"):
        base = vector_store.as_retriever(
            search_kwargs={
                "k": top_k,
                "score_threshold": similarity_threshold
            }
        )
        
        # Add debug wrapper to the base retriever if needed
        class DebugRetriever:
            """Wrapper to debug retriever calls"""
            def __init__(self, retriever):
                self.retriever = retriever
                
            def invoke(self, query):
                rprint(f"[cyan]🔍 Base retriever search: {query}[/cyan]")
                docs = self.retriever.invoke(query)
                rprint(f"[cyan]📝 Retrieved {len(docs)} documents[/cyan]")
                return docs
        
        # Use MultiQueryRetriever for better recall
        try:
            # Create the multi-query retriever with callbacks for debugging
            from langchain.callbacks.manager import CallbackManager
            from langchain.callbacks import StdOutCallbackHandler
            
            # Only use verbose callbacks in debug mode
            if CONFIG.get("debug", False):
                callbacks = [StdOutCallbackHandler()]
                cb_manager = CallbackManager(callbacks)
                retriever = MultiQueryRetriever.from_llm(
                    retriever=base,
                    llm=llm,
                    callbacks=cb_manager
                )
                rprint("[green]✅ Using MultiQueryRetriever with debug output[/green]")
            else:
                retriever = MultiQueryRetriever.from_llm(
                    retriever=base, 
                    llm=llm
                )
                rprint("[green]✅ Using MultiQueryRetriever[/green]")
            
            return retriever
            
        except Exception as e:
            rprint(f"[yellow]⚠️ MultiQueryRetriever error: {e}. Falling back to base retriever.[/yellow]")
            return base
    else:
        # Fallback for older versions
        rprint("[yellow]⚠️ Using basic retriever (similarity threshold not supported)[/yellow]")
        return vector_store.as_retriever(search_kwargs={"k": top_k})


def embed_with_fallback(embedder, text):
    """Try to embed text with fallback to handle API changes."""
    try:
        # Try new API (v0.6.x+)
        if hasattr(embedder, "embed_documents"):
            # fastembed 0.6.x+ API style
            vectors = embedder.embed_documents([text])
            return vectors[0]
        # Try new API (v0.3.x - v0.5.x)
        vector = embedder.embed(text)
        # Check if it's an iterator or generator
        if hasattr(vector, "__iter__") and not isinstance(vector, (list, np.ndarray)):
            vector = next(vector)
        return vector
    except Exception as e:
        try:
            # Fall back to old API as a batch
            vector = embedder.embed([text])[0]
            return vector
        except Exception as e2:
            raise ValueError(f"Failed to embed text: {str(e)} | {str(e2)}")


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
        web_texts = []
        # Handle different response formats in different exa-py versions
        if isinstance(results, list) and len(results) > 0:
            # Handle list format (newer versions)
            for res in results[:n_results]:
                if 'content' in res:
                    web_texts.append(res['content'])
                elif 'text' in res:
                    web_texts.append(res['text'])
        elif hasattr(results, 'results') and hasattr(results.results, '__iter__'):
            # Handle object format (older versions)
            for res in results.results[:n_results]:
                if hasattr(res, 'content'):
                    web_texts.append(res.content)
                elif hasattr(res, 'text'):
                    web_texts.append(res.text)
                
        if web_texts:
            try:
                from langchain_core.documents import Document
                # Use the text splitter already imported
                splitter = TokenTextSplitter(
                    chunk_size=CHUNK_SIZE,
                    chunk_overlap=CHUNK_OVERLAP,
                    model_name="gpt-3.5-turbo",
                )
                # Process web results like other documents
                docs = [
                    Document(page_content=text, metadata={"source": "web"})
                    for text in web_texts
                ]

                # Split into chunks
                chunks = splitter.split_documents(docs)

                # Get embedder and client
                embedder = Embedder(EMBED_MODEL_NAME)
                client = connect_to_qdrant()

                # Create batch of embeddings and payloads
                batch_vectors = []
                payloads = []
                for doc in chunks:
                    batch_vectors.append(
                        embed_with_fallback(embedder, doc.page_content)
                    )
                    # Include page_content in the payload to match ingest.py
                    payloads.append({
                        "source": "web", 
                        "query": query,
                        "page_content": doc.page_content
                    })

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

            # Use the same client that's already connected in the main application
            # instead of creating a new one
            client = connect_to_qdrant()
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
            # Provide a hint about Docker if embedded Qdrant fails
            if "already accessed by another instance" in str(e):
                rprint("[yellow]💡 Try using Docker-based Qdrant instead:[/yellow]")
                rprint("[yellow]   1. Stop this chat (Ctrl+C)[/yellow]")
                rprint("[yellow]   2. Run 'make start_qdrant' if not already running[/yellow]")
                rprint("[yellow]   3. Use 'python ingest.py --path {path}' directly[/yellow]")
        return True

    if cmd == ":search_kb":
        if not args:
            rprint("[red]⚠️ Search term required: :search_kb TERM[/red]")
            return True
            
        search_term = args.strip()
        rprint(f"[cyan]🔍 Direct knowledge base search for: {search_term}[/cyan]")
        
        # Debug output
        if state.get("debug"):
            rprint("[cyan]⚙️ Debug mode enabled for KB search[/cyan]")
            
        try:
            # Use direct embedding for search
            embedder = state.get("embedder")
            query_vec = embed_with_fallback(embedder, search_term)
            client = connect_to_qdrant()
            
            limit = CONFIG.get("top_k", 5)
            results = client.search(
                collection_name=COLLECTION,
                query_vector=query_vec,
                limit=limit,
                with_payload=True,
            )
            
            if not results:
                rprint("[yellow]⚠️ No results found[/yellow]")
                return True
                
            for i, res in enumerate(results):
                score = res.score
                source = res.payload.get("source", "unknown")
                
                # In debug mode, show all metadata
                if state.get("debug"):
                    rprint(f"[bold cyan]Result {i+1} (score: {score:.4f}):[/bold cyan]")
                    for k, v in res.payload.items():
                        rprint(f"  [green]{k}:[/green] {v}")
                else:
                    rprint(f"[green]Result {i+1}:[/green] {source} (score: {score:.4f})")
                    
            rprint(f"[green]✅ Found {len(results)} results[/green]")
        except Exception as e:
            import traceback
            rprint(f"[red]❌ Error searching knowledge base: {e}[/red]")
            if state.get("debug"):
                rprint(traceback.format_exc())
        
        return True
            
    if cmd == ":search":
        if not args:
            rprint("[red]⚠️ Search term required: :search TERM[/red]")
            return True

        search_term = args.strip()
        rprint(f"[cyan]🔍 Web search for: {search_term}[/cyan]")
        context = web_fallback(search_term, n_results=5)
        
        if not context:
            rprint("[red]❌ No web search results found.[/red]")
            return True
            
        # Do a QA with the search results
        qa_prompt = PromptTemplate.from_template(
            "You are a helpful assistant. Use the following web search results to answer the question.\n"
            "Clearly cite sources from the results.\n\n"
            "Web search results:\n{context}\n\n"
            "Question: {question}\nAnswer:"
        )
        
        # Create a temporary chain for the search operation
        # This is separate from the main qa_chain because it uses a different prompt
        search_chain = qa_prompt | state["llm"]
        
        # Generate answer
        answer = search_chain.invoke({"context": context, "question": search_term})
        
        # Format and display
        rprint(Panel.fit(answer, title="Web Search Results", border_style="green"))
        return True

    if cmd == ":debug":
        if args.lower() in ("on", "true", "1"):
            state["debug"] = True
            rprint("[bold green]🔍 Debug mode ON - Detailed information will be shown[/bold green]")
            # Set debug in CONFIG too for other components
            CONFIG["debug"] = True
        elif args.lower() in ("off", "false", "0"):
            state["debug"] = False
            rprint("[bold yellow]🔍 Debug mode OFF[/bold yellow]")
            CONFIG["debug"] = False
        else:
            current = state.get("debug", False)
            rprint(f"[cyan]🔍 Debug mode is currently {'ON' if current else 'OFF'}[/cyan]")
            rprint("[cyan]Use ':debug on' or ':debug off' to change[/cyan]")
        return True

    if cmd == ":config":
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        # Add provider-specific information
        model_provider = CONFIG.get("model_provider", "ollama")
        table.add_row("model_provider", model_provider)
        
        if model_provider == "ollama":
            table.add_row("model (ollama)", CONFIG.get("model", "qwen3:4b"))
        elif model_provider == "openrouter":
            table.add_row("openrouter_model", CONFIG.get("openrouter_model", "deepseek/deepseek-prover-v2:free"))
            table.add_row("openrouter_api_base", OPENAI_API_BASE)
        
        # Add other configuration settings
        for key, value in CONFIG.items():
            # Skip model settings already displayed
            if key not in ["model_provider", "model", "openrouter_model"]:
                table.add_row(key, str(value))

        # Add runtime settings
        table.add_row("memory_enabled", str(state.get("memory_enabled", False)))
        table.add_row("web_fallback_enabled", str(state.get("web_fallback", False)))
        table.add_row("debug_mode", str(state.get("debug", False)))

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

    # Add provider command
    if cmd == ":provider":
        if not args:
            current_provider = CONFIG.get("model_provider", "ollama")
            rprint(f"[cyan]🔍 Current provider is: {current_provider}[/cyan]")
            rprint("[cyan]Use ':provider ollama' or ':provider openrouter' to change[/cyan]")
            if current_provider == "openrouter":
                rprint(f"[cyan]Current OpenRouter model: {CONFIG.get('openrouter_model', 'deepseek/deepseek-prover-v2:free')}[/cyan]")
                rprint("[cyan]Use ':provider openrouter MODEL_NAME' to change the OpenRouter model[/cyan]")
            return True
            
        parts = args.split(maxsplit=1)
        provider = parts[0].lower()
        
        if provider not in ["ollama", "openrouter"]:
            rprint(f"[red]⚠️ Unknown provider: {provider}. Use 'ollama' or 'openrouter'[/red]")
            return True
            
        # If changing to the same provider but with a different model
        if provider == CONFIG.get("model_provider"):
            if provider == "openrouter" and len(parts) > 1:
                model_name = parts[1].strip()
                CONFIG["openrouter_model"] = model_name
                rprint(f"[green]✅ Changed OpenRouter model to: {model_name}[/green]")
                
                # Recreate the LLM with the new model
                state["llm"] = get_llm()
            else:
                rprint(f"[cyan]ℹ️ Already using {provider} provider[/cyan]")
            return True
            
        # Change provider
        CONFIG["model_provider"] = provider
        rprint(f"[green]✅ Changed provider to: {provider}[/green]")
        
        # If switching to OpenRouter with a specific model
        if provider == "openrouter" and len(parts) > 1:
            model_name = parts[1].strip()
            CONFIG["openrouter_model"] = model_name
            rprint(f"[green]✅ Using OpenRouter model: {model_name}[/green]")
        
        # Recreate the LLM with the new provider
        try:
            state["llm"] = get_llm()
            
            # Update the QA chain to use the new LLM
            qa_prompt = PromptTemplate.from_template(
                "You are a helpful assistant. Use the following context to answer the question.\n"
                "If the context doesn't contain relevant information to answer the question, clearly state that no relevant information is available.\n"
                "If the context has SOME information on the topic but not enough to fully answer, use what's available and acknowledge the limitations.\n"
                "Always cite sources from the context when using specific information.\n\n"
                "Context:\n{context}\n\n"
                "{history}\n\n"
                "Question: {question}\n\n"
                "Approach this in steps:\n"
                "1. Analyze whether the context contains information related to the question\n"
                "2. Extract relevant details from the context\n"
                "3. Formulate a clear answer that synthesizes the information and cites sources\n\n"
                "Answer:"
            )
            
            state["qa_chain"] = qa_prompt | state["llm"]
            
        except Exception as e:
            rprint(f"[red]❌ Error changing provider: {e}[/red]")
            # Revert to the previous provider
            CONFIG["model_provider"] = "ollama" if provider == "openrouter" else "openrouter"
            rprint(f"[yellow]⚠️ Reverted to {CONFIG['model_provider']} provider[/yellow]")
        
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
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode with detailed output"
    )
    parser.add_argument(
        "--provider", type=str, choices=["ollama", "openrouter"], 
        help="Model provider to use (overrides config.yaml)"
    )
    parser.add_argument(
        "--openrouter-model", type=str,
        help="OpenRouter model to use (overrides config.yaml)"
    )
    args = parser.parse_args()

    # Override configuration based on command line arguments
    if args.provider:
        CONFIG["model_provider"] = args.provider
        rprint(f"[cyan]🔄 Overriding model provider from command line: {args.provider}[/cyan]")
    
    if args.openrouter_model and CONFIG["model_provider"] == "openrouter":
        CONFIG["openrouter_model"] = args.openrouter_model
        rprint(f"[cyan]🔄 Overriding OpenRouter model from command line: {args.openrouter_model}[/cyan]")
    
    # Display credentials check information for clarity
    rprint("[cyan]🔐 Checking credentials...[/cyan]")
    if CONFIG["model_provider"] == "openrouter":
        if not OPENAI_API_KEY:
            rprint("[red]❌ OPENAI_API_KEY not found in environment[/red]")
            rprint("[yellow]💡 Please set this in .env file or export it directly:[/yellow]")
            rprint("[yellow]  export OPENAI_API_KEY=your_openrouter_key[/yellow]")
        else:
            masked_key = OPENAI_API_KEY[:4] + "..." + OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 8 else "***" 
            rprint(f"[green]✅ OPENAI_API_KEY found: {masked_key}[/green]")
            rprint(f"[green]✅ Using base URL: {OPENAI_API_BASE}[/green]")
    
    if CONFIG.get("use_web_fallback", True) and not args.no_web:
        if not EXA_KEY:
            rprint("[yellow]⚠️ EXA_API_KEY not found - web search will be disabled[/yellow]")
        else:
            masked_key = EXA_KEY[:4] + "..." + EXA_KEY[-4:] if len(EXA_KEY) > 8 else "***"
            rprint(f"[green]✅ EXA_API_KEY found: {masked_key}[/green]")

    rprint(
        Panel(
            "🚀 [bold cyan]LearningAgent Ready[/bold cyan]\n\n"
            "📚 [bold]Commands:[/bold]\n"
            "  - Type your questions to chat with the agent\n"
            "  - [yellow]:search[/yellow] [italic]<topic>[/italic] → run web search on a topic\n"
            "  - [yellow]:search_kb[/yellow] [italic]<term>[/italic] → direct search in knowledge base\n"
            "  - [yellow]:ingest[/yellow] [italic]<path>[/italic] → add documents to knowledge base\n"
            "  - [yellow]:provider[/yellow] [italic]<ollama|openrouter> [model_name][/italic] → change LLM provider\n"
            "  - [yellow]:memory[/yellow] [italic]on/off[/italic] → toggle conversation memory\n"
            "  - [yellow]:debug[/yellow] [italic]on/off[/italic] → toggle detailed debug info\n"
            "  - [yellow]:config[/yellow] → show current settings\n"
            "  - [yellow]:exit[/yellow] → quit the application",
            border_style="cyan",
            title="Welcome",
        )
    )

    # LLM & retriever
    try:
        llm = get_llm()
        embedder = Embedder(EMBED_MODEL_NAME)
        vector_store = init_vector_store(embedder)
        retriever = build_retriever(vector_store, llm, args.top_k)
    except ValueError as e:
        if "OpenRouter authentication failed" in str(e) or "OpenRouter API key not found" in str(e):
            rprint("[red]❌ OpenRouter authentication failed. Please check your API key.[/red]")
            rprint("[yellow]💡 Quick fix: try these commands in sequence:[/yellow]")
            rprint("[yellow]  make export_env[/yellow]")
            rprint("[yellow]  source ./export_env.sh[/yellow]")
            rprint("[yellow]  make run_openrouter[/yellow]")
            rprint("[yellow]💡 More details in README.md troubleshooting section[/yellow]")
            return
        else:
            raise

    # Enhanced QA prompt that asks to cite sources
    qa_prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the question.\n"
        "If the context doesn't contain relevant information to answer the question, clearly state that no relevant information is available.\n"
        "If the context has SOME information on the topic but not enough to fully answer, use what's available and acknowledge the limitations.\n"
        "Always cite sources from the context when using specific information.\n\n"
        "Context:\n{context}\n\n"
        "{history}\n\n"
        "Question: {question}\n\n"
        "Approach this in steps:\n"
        "1. Analyze whether the context contains information related to the question\n"
        "2. Extract relevant details from the context\n"
        "3. Formulate a clear answer that synthesizes the information and cites sources\n\n"
        "Answer:"
    )
    
    # Use RunnableSequence instead of LLMChain
    qa_chain = qa_prompt | llm

    # State dictionary to hold runtime config
    state = {
        "memory_enabled": not args.no_memory and CONFIG.get("use_memory", True),
        "web_fallback": not args.no_web and CONFIG.get("use_web_fallback", True),
        "top_k": args.top_k,
        "embedder": embedder,
        "llm": llm,
        "qa_chain": qa_chain,  # Store the qa_chain in state
        "debug": args.debug,
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
        rprint("[cyan]🔍 Searching knowledge base...[/cyan]")
        docs = retriever.invoke(user_input)
        
        # Debug: show document sources and scores if available
        if isinstance(docs, list):
            context_texts = []
            sources = []
            
            # Create formatted context with source info
            for i, doc in enumerate(docs):
                content = doc.page_content
                metadata = doc.metadata
                source = metadata.get("source", "unknown")
                page = metadata.get("page", "")
                score = metadata.get("score", None)
                
                # Format source info
                source_info = f"[Source: {source}"
                if page:
                    source_info += f", page {page}"
                if score is not None:
                    source_info += f", relevance: {score:.2f}"
                source_info += "]"
                
                # Add to context with source information
                context_texts.append(f"{content}\n\n{source_info}")
                sources.append(source)
                
                # Enhanced debug logging
                if state.get("debug"):
                    rprint(f"[cyan]Document {i+1}:[/cyan]")
                    rprint(f"[green]  Source: {source} {page if page else ''}[/green]")
                    if score is not None:
                        rprint(f"[yellow]  Score: {score:.4f}[/yellow]")
                    rprint(f"[blue]  Length: {len(content)} chars[/blue]")
                    
                    # Show content preview in debug mode
                    if content:
                        preview = content[:min(200, len(content))]
                        if len(content) > 200:
                            preview += "..."
                        rprint(f"[dim]  Preview: {preview}[/dim]")
                    else:
                        rprint("[red]  Warning: Empty content![/red]")
                    rprint("")  # Add spacing between documents
            
            # Display retrieval info
            rprint(f"[green]✅ Found {len(docs)} relevant documents[/green]")
            if len(set(sources)) > 1:
                rprint(f"[green]  Sources: {', '.join(set(sources))[:80]}{'...' if len(', '.join(set(sources))) > 80 else ''}[/green]")
        else:
            context_texts = []
            rprint("[yellow]⚠️ No relevant documents found[/yellow]")

        # Web fallback if no results
        if not context_texts and state["web_fallback"]:
            rprint("[yellow]🔍 No local results – falling back to web search...[/yellow]")
            web_ctx = web_fallback(user_input, n_results=CONFIG.get("web_results", 3))
            if web_ctx:
                context_texts = [f"{web_ctx}\n\n[Source: web search results]"]
                rprint("[green]✅ Retrieved information from the web[/green]")

        if not context_texts:
            rprint(
                "[red]😕 I couldn't find relevant information. Try ingesting more docs or enabling web search.[/red]"
            )
            continue

        # Join context texts and ensure there's content
        context = "\n\n---\n\n".join(context_texts)
        
        # Extra debug for context verification
        if state.get("debug"):
            rprint(f"[cyan]Total context length: {len(context)} chars[/cyan]")
            rprint("[cyan]Context sample (first 500 chars):[/cyan]")
            rprint(f"[dim]{context[:min(500, len(context))]}{'...' if len(context) > 500 else ''}[/dim]")
            
            # Offer to save debug info to file
            rprint("[yellow]Would you like to save debug info to a file? (y/n)[/yellow]")
            save_debug = input().strip().lower()
            if save_debug in ["y", "yes"]:
                debug_file = f"debug_query_{int(time.time())}.txt"
                with open(debug_file, "w") as f:
                    f.write(f"QUERY: {user_input}\n\n")
                    f.write(f"DOCUMENTS RETRIEVED: {len(docs)}\n\n")
                    for i, doc in enumerate(docs):
                        f.write(f"--- DOCUMENT {i+1} ---\n")
                        f.write(f"Source: {doc.metadata.get('source', 'unknown')}\n")
                        if 'page' in doc.metadata:
                            f.write(f"Page: {doc.metadata['page']}\n")
                        if 'score' in doc.metadata:
                            f.write(f"Score: {doc.metadata['score']}\n")
                        f.write(f"Content length: {len(doc.page_content)} chars\n")
                        f.write("\nCONTENT:\n")
                        f.write(doc.page_content)
                        f.write("\n\n")
                    f.write("--- FULL CONTEXT SENT TO LLM ---\n")
                    f.write(context)
                rprint(f"[green]Debug info saved to {debug_file}[/green]")

        # Get conversation history if memory is enabled
        history = ""
        if state.get("memory"):
            memory_buffer = state["memory"].buffer
            if memory_buffer:
                history = "Previous conversation:\n" + memory_buffer

        # ===== LLM phase =====
        if state.get("debug"):
            rprint("[cyan]⚙️ Generating answer...[/cyan]")
            
        answer = state["qa_chain"].invoke({"context": context, "question": user_input, "history": history})
        
        # Clean up the answer to remove <think> sections and any other assistant markup
        clean_answer = answer
        
        # Ensure answer is a string before applying regex
        if not isinstance(clean_answer, str):
            # Convert to string if it's not already
            clean_answer = str(clean_answer)
        
        # Extract just the content from OpenRouter response if it's in that format    
        if "content=" in clean_answer and "additional_kwargs=" in clean_answer:
            try:
                # Extract the content part from OpenRouter format
                content_match = re.search(r"content='(.*?)' additional_kwargs=", clean_answer, re.DOTALL)
                if content_match:
                    clean_answer = content_match.group(1)
                    # Unescape any escaped quotes and handle newlines
                    clean_answer = clean_answer.replace("\\'", "'").replace("\\n", "\n")
            except Exception as e:
                # If parsing fails, continue with the original string
                rprint(f"[yellow]⚠️ Could not parse OpenRouter response format: {e}[/yellow]")
            
        # Remove <think>...</think> blocks
        clean_answer = re.sub(r'<think>.*?</think>', '', clean_answer, flags=re.DOTALL)
        # Remove any remaining XML-like tags
        clean_answer = re.sub(r'<[^>]+>', '', clean_answer)
        # Remove any lines with only dashes or empty lines at the beginning/end
        clean_answer = re.sub(r'^[\s\-]+', '', clean_answer)
        clean_answer = re.sub(r'[\s\-]+$', '', clean_answer)
        # Trim whitespace
        clean_answer = clean_answer.strip()
        
        rprint(Panel.fit(clean_answer, title="Assistant", border_style="green"))

        if state.get("memory"):
            state["memory"].save_context({"input": user_input}, {"output": clean_answer})

            # Store conversation in vector DB for future reference
            try:
                from langchain_core.documents import Document

                # Create document from conversation turn
                conv_doc = Document(
                    page_content=f"Q: {user_input}\nA: {clean_answer}",
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
