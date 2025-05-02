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
def get_llm(model=None, temperature=None):
    """Create an LLM instance."""
    model = model or CONFIG.get("model", "qwen3:4b")
    temperature = temperature or CONFIG.get("temperature", 0.3)
    
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
        # Use MultiQueryRetriever for better recall
        return MultiQueryRetriever.from_llm(
            retriever=base, 
            llm=llm
        )
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
        
        try:
            # Get components from state
            embedder = state.get("embedder")
            if not embedder:
                embedder = Embedder(EMBED_MODEL_NAME)
                
            # Connect to Qdrant
            client = connect_to_qdrant()
            
            # Create embedding for search term
            query_vector = embed_with_fallback(embedder, search_term)
            
            # Perform raw search with high limit and no threshold
            from qdrant_client.models import Filter
            
            search_results = client.search(
                collection_name=COLLECTION,
                query_vector=query_vector,
                limit=20,  # Higher limit for debug search
                with_payload=True,
            )
            
            if not search_results:
                rprint("[yellow]⚠️ No results found in knowledge base[/yellow]")
                return True
                
            # Display results in a table
            from rich.table import Table
            
            table = Table(title=f"Search Results for '{search_term}'")
            table.add_column("Score", style="cyan", justify="right")
            table.add_column("Source", style="green")
            table.add_column("Content Preview", style="yellow")
            
            for i, result in enumerate(search_results, 1):
                score = result.score
                source = result.payload.get("source", "unknown")
                
                # Get content preview by searching in vectors
                point = client.retrieve(
                    collection_name=COLLECTION,
                    ids=[result.id],
                    with_vectors=False,
                    with_payload=True,
                )
                
                content = "Content not available"
                if point and point[0].payload:
                    # Try different ways to get content
                    if "page_content" in point[0].payload:
                        content = point[0].payload["page_content"]
                    elif "text" in point[0].payload:
                        content = point[0].payload["text"]
                    else:
                        # For direct search results, try to get content from a separate lookup
                        try:
                            from langchain_community.vectorstores import QdrantVectorStore
                            raw_results = QdrantVectorStore(
                                client=client,
                                collection_name=COLLECTION,
                                embedding=EmbeddingWrapper(embedder),
                            ).similarity_search_with_score(search_term, k=1, filter=Filter(must=[{"has_id": [result.id]}]))
                            if raw_results:
                                content = raw_results[0][0].page_content
                        except:
                            content = "Content preview not available"
                
                # Truncate long content
                if len(content) > 100:
                    content = content[:97] + "..."
                
                table.add_row(
                    f"{score:.4f}",
                    source,
                    content
                )
                
                # For the top 3 most similar documents, show more details
                if i <= 3:
                    rprint(f"[bold]Document {i} (Score: {score:.4f})[/bold]")
                    rprint(f"Source: {source}")
                    if len(content) > 100:
                        rprint(f"Preview: {content[:100]}...")
                    else:
                        rprint(f"Content: {content}")
                    rprint("")
            
            rprint(table)
            
            # Show collection stats
            collection_info = client.get_collection(COLLECTION)
            vector_count = collection_info.points_count
            rprint(f"[dim]Knowledge base contains {vector_count} total vectors[/dim]")
            
        except Exception as e:
            import traceback
            rprint(f"[red]❌ Error searching knowledge base: {e}[/red]")
            if state.get("debug"):
                rprint(traceback.format_exc())
        
        return True
            
    if cmd == ":search":
        if not args:
            rprint("[red]⚠️ Topic required: :search TOPIC[/red]")
            return True
            
        if not EXA_KEY:
            rprint("[red]❌ No Exa API key found. Set EXA_API_KEY in .env file.[/red]")
            return True
            
        topic = args.strip()
        rprint(f"[cyan]🔍 Researching topic: {topic}...[/cyan]")
        
        # Create chain to generate research questions
        question_prompt = PromptTemplate.from_template(
            "Given the research topic: {topic}, generate 5 detailed research questions "
            "to explore this topic thoroughly. Output as a numbered list, one per line."
        )
        
        llm = state.get("llm")
        if not llm:
            llm = get_llm()
            
        # Generate questions
        try:
            q_result = llm.invoke(question_prompt.format(topic=topic))
            if hasattr(q_result, 'content'):
                q_text = q_result.content
            else:
                q_text = str(q_result)
                
            # Extract questions from numbered list
            questions = [
                line.lstrip("0123456789. ").strip()
                for line in q_text.splitlines() if line.strip()
            ]
            
            # Filter out non-question lines
            questions = [q for q in questions if q and len(q) > 10]
            
            if not questions:
                rprint("[yellow]⚠️ Could not generate research questions. Using topic directly.[/yellow]")
                questions = [topic]
            else:
                rprint(f"[green]✅ Generated {len(questions)} research questions:[/green]")
                for i, q in enumerate(questions, 1):
                    rprint(f"   {i}. {q}")
                    
            # Perform searches for each question
            rprint("[cyan]🌐 Searching web for information...[/cyan]")
            exa = Exa(api_key=EXA_KEY)
            enriched = []
            total_results = 0
            
            for q in questions:
                try:
                    resp = exa.search_and_contents(
                        q,
                        use_autoprompt=True,
                        num_results=3,  # Limit to 3 results per question
                        text=True,
                        highlights=True
                    )
                    # Process results
                    if hasattr(resp, 'results'):
                        results = resp.results
                    else:
                        results = resp
                        
                    snippets = []
                    for item in results:
                        snippet = ""
                        if hasattr(item, "text"):
                            snippet = item.text
                        elif isinstance(item, dict) and "text" in item:
                            snippet = item["text"]
                            
                        url = ""
                        if hasattr(item, "url"):
                            url = item.url
                        elif isinstance(item, dict) and "url" in item:
                            url = item["url"]
                            
                        if snippet and url:
                            snippets.append(f"[{url}] {snippet}")
                            
                    if snippets:
                        enriched.append(f"## {q}\n" + "\n\n".join(snippets))
                        total_results += len(snippets)
                except Exception as e:
                    rprint(f"[yellow]⚠️ Search failed for question: {q} - {e}[/yellow]")
                    
            if not enriched:
                rprint("[red]❌ No search results found. Try a different topic.[/red]")
                return True
                
            # Combine all research
            all_research = "\n\n".join(enriched)
            
            # Store in vector DB
            from langchain_core.documents import Document
            # Use the text splitter already imported
            
            # Process web results
            docs = [
                Document(page_content=text, metadata={"source": "web", "topic": topic})
                for text in enriched
            ]
            
            # Split into chunks if needed
            splitter = TokenTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                model_name="gpt-3.5-turbo",
            )
            chunks = splitter.split_documents(docs)
            
            # Get embedder and client
            embedder = state.get("embedder")
            client = connect_to_qdrant()
            
            # Create batch of embeddings and payloads
            batch_vectors = []
            payloads = []
            for doc in chunks:
                vector = embed_with_fallback(embedder, doc.page_content)
                batch_vectors.append(vector)
                payloads.append({"source": "web", "topic": topic})
                
            # Use a timestamp-based ID to avoid collisions
            import time
            start_id = int(time.time() * 1000)
            
            # Upsert to Qdrant
            from qdrant_client import models as qmodels
            client.upsert(
                collection_name=COLLECTION,
                points=[
                    qmodels.PointStruct(id=start_id + i, vector=v, payload=payloads[i])
                    for i, v in enumerate(batch_vectors)
                ],
            )
            
            # Get vector count
            collection_info = client.get_collection(COLLECTION)
            vector_count = collection_info.points_count
            
            rprint(
                Panel.fit(
                    f"🔖 Stored research for topic: [bold]{topic}[/bold]\n"
                    f"📊 Found [bold]{total_results}[/bold] web results for [bold]{len(questions)}[/bold] questions\n"
                    f"💾 Collection now contains [bold green]{vector_count}[/bold green] vectors.",
                    title="Research Complete",
                    border_style="blue",
                )
            )
            
        except Exception as e:
            import traceback
            rprint(f"[red]❌ Error during web research: {e}[/red]")
            rprint(traceback.format_exc())
            
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
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode with detailed output"
    )
    args = parser.parse_args()

    rprint(
        Panel(
            "🚀 [bold cyan]LearningAgent Ready[/bold cyan]\n\n"
            "📚 [bold]Commands:[/bold]\n"
            "  - Type your questions to chat with the agent\n"
            "  - [yellow]:search[/yellow] [italic]<topic>[/italic] → run web search on a topic\n"
            "  - [yellow]:search_kb[/yellow] [italic]<term>[/italic] → direct search in knowledge base\n"
            "  - [yellow]:ingest[/yellow] [italic]<path>[/italic] → add documents to knowledge base\n"
            "  - [yellow]:memory[/yellow] [italic]on/off[/italic] → toggle conversation memory\n"
            "  - [yellow]:config[/yellow] → show current settings\n"
            "  - [yellow]:exit[/yellow] → quit the application",
            border_style="cyan",
            title="Welcome",
        )
    )

    # LLM & retriever
    llm = get_llm()
    embedder = Embedder(EMBED_MODEL_NAME)
    vector_store = init_vector_store(embedder)
    retriever = build_retriever(vector_store, llm, args.top_k)

    # Enhanced QA prompt that asks to cite sources
    qa_prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the question.\n"
        "If the context doesn't contain relevant information, say so.\n"
        "If you use information from the context, cite the source when possible.\n\n"
        "Context:\n{context}\n\n"
        "{history}\n\n"
        "Question: {question}\nAnswer:"
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
                
                context_texts.append(f"{content}\n\n{source_info}")
                sources.append(source)
                
                # Debug logging
                if state.get("debug"):
                    rprint(f"[dim]Document {i+1}:[/dim]")
                    rprint(f"[dim]  Source: {source} {page if page else ''}[/dim]")
                    if score is not None:
                        rprint(f"[dim]  Score: {score:.2f}[/dim]")
                    rprint(f"[dim]  Length: {len(content)} chars[/dim]")
            
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

        context = "\n\n---\n\n".join(context_texts)

        # Get conversation history if memory is enabled
        history = ""
        if state.get("memory"):
            memory_buffer = state["memory"].buffer
            if memory_buffer:
                history = "Previous conversation:\n" + memory_buffer

        # ===== LLM phase =====
        if state.get("debug"):
            rprint("[cyan]⚙️ Generating answer...[/cyan]")
            
        answer = qa_chain.invoke({"context": context, "question": user_input, "history": history})
        
        # Clean up the answer to remove <think> sections and any other assistant markup
        clean_answer = answer
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
