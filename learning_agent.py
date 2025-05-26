"""
learning_agent.py
-----------------
A simplified RAG chat assistant with memory and retrieval capabilities.
Refactored with a class-based architecture for better maintainability.
"""

import os
# import yaml # No longer used directly in this file
import warnings
# import logging # No longer used directly in this file
# from pathlib import Path # No longer used directly in this file
from typing import List, Dict, Any, Optional, Union, Callable # Path was removed from here too
from abc import ABC, abstractmethod
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console
from dotenv import load_dotenv

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*was deprecated.*")
warnings.filterwarnings("ignore", message=".*TOKENIZERS_PARALLELISM.*")

# Set environment variable to avoid HuggingFace tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# LangChain imports
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.language_models import BaseChatModel

# Vector store and embeddings
import fastembed
# QdrantClient is now imported in qdrant_utils
# from qdrant_client import QdrantClient
from qdrant_client import models as qmodels
from langchain_qdrant import QdrantVectorStore
from qdrant_utils import connect_to_qdrant # Import the new utility
from langchain_community.embeddings import FastEmbedEmbeddings

# Exa search for web fallback
from exa_py import Exa

# Import ConfigManager from the new utility file
from config_utils import ConfigManager

# --------------------------------------------------------------------------- #
#                                LLM Factory                                  #
# --------------------------------------------------------------------------- #
class LLMFactory:
    """
    Factory for creating Language Model (LLM) instances.
    Provides robust error handling and fallback mechanisms for LLM initialization.
    """
    
    @staticmethod
    def check_ollama_service() -> bool:
        """Check if Ollama service is running and available."""
        import socket
        
        # Check if Ollama is running on default port 11434
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Short timeout for quick check
        result = sock.connect_ex(('localhost', 11434))
        sock.close()
        
        return result == 0  # True if port is open
    
    @staticmethod
    def create_llm(config: ConfigManager) -> BaseChatModel:
        """
        Creates an LLM instance based on the provider specified in the configuration.
        Handles initialization for 'openrouter' and 'ollama' providers,
        including API key checks for OpenRouter and service availability checks for Ollama.
        Implements fallback logic between providers if one fails.

        Args:
            config (ConfigManager): The configuration manager instance.

        Returns:
            BaseChatModel: An instance of the configured language model.
        
        Raises:
            ValueError: If an API key is missing for OpenRouter or if all LLM providers fail to initialize.
        """
        model_provider = config.get("model_provider", "ollama")
        model = config.get("model", "qwen3:4b")
        temperature = config.get("temperature", 0.3)
        
        # Try OpenRouter if configured
        if model_provider == "openrouter":
            try:
                # Use OpenRouter through the OpenAI interface
                openrouter_model = config.get("openrouter_model", "deepseek/deepseek-prover-v2:free")
                
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    rprint("[red]❌ Missing OPENAI_API_KEY in .env for OpenRouter[/red]")
                    rprint("[yellow]💡 Add OPENAI_API_KEY=your_openrouter_key to .env[/yellow]")
                    raise ValueError("OpenRouter API key not found in environment")
                
                rprint(f"[green]🔄 Using OpenRouter model: {openrouter_model}[/green]")
                
                return ChatOpenAI(
                    model=openrouter_model,
                    temperature=temperature,
                    api_key=api_key,
                    base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
                )
            except Exception as e:
                rprint(f"[red]❌ Failed to initialize OpenRouter: {e}[/red]")
                # If OpenRouter fails and Ollama is available, try Ollama as fallback
                if LLMFactory.check_ollama_service():
                    rprint("[yellow]💡 Falling back to Ollama...[/yellow]")
                    try:
                        return ChatOllama(model=model, temperature=temperature)
                    except Exception as ollama_e:
                        rprint(f"[red]❌ Ollama fallback also failed: {ollama_e}[/red]")
                # If both fail, re-raise the original error
                raise
        
        # Default to Ollama with better error handling
        if not LLMFactory.check_ollama_service():
            rprint("[yellow]⚠️ Ollama service not detected on port 11434[/yellow]")
            rprint("[yellow]💡 To start Ollama, open a new terminal and run: ollama serve[/yellow]")
            
            # Check if OpenRouter is configured as fallback
            if os.getenv("OPENAI_API_KEY"):
                rprint("[yellow]💡 Trying OpenRouter as fallback...[/yellow]")
                try:
                    openrouter_model = config.get("openrouter_model", "deepseek/deepseek-prover-v2:free")
                    return ChatOpenAI(
                        model=openrouter_model,
                        temperature=temperature,
                        api_key=os.getenv("OPENAI_API_KEY"),
                        base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
                    )
                except Exception as or_e:
                    rprint(f"[red]❌ OpenRouter fallback failed: {or_e}[/red]")
            
            # If we get here, we'll try Ollama anyway, but it will likely fail
            rprint("[yellow]⚠️ Attempting to connect to Ollama anyway...[/yellow]")
        
        try:
            rprint(f"[green]🔄 Using Ollama model: {model}[/green]")
            return ChatOllama(model=model, temperature=temperature)
        except Exception as e:
            rprint(f"[red]❌ Failed to initialize Ollama: {e}[/red]")
            
            # Try OpenRouter as fallback if API key exists
            if os.getenv("OPENAI_API_KEY"):
                rprint("[yellow]💡 Trying OpenRouter as fallback...[/yellow]")
                try:
                    openrouter_model = config.get("openrouter_model", "deepseek/deepseek-prover-v2:free")
                    return ChatOpenAI(
                        model=openrouter_model,
                        temperature=temperature,
                        api_key=os.getenv("OPENAI_API_KEY"),
                        base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
                    )
                except Exception:
                    pass  # Both failed, will raise original error
            
            # If we get here, both providers failed
            raise ValueError(f"Failed to initialize any LLM provider: {str(e)}")

# We're now using LangChain's built-in FastEmbedEmbeddings class instead of a custom implementation

# --------------------------------------------------------------------------- #
#                              Vector Database                                #
# --------------------------------------------------------------------------- #
class VectorDatabase:
    """
    Manages connections and operations with the Qdrant vector database.
    Uses a centralized utility for Qdrant connection and initializes
    the vector store with appropriate embeddings.
    """
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.collection_name = config.get("collection", "kb")
        self.embedding_model_name = config.get("embedding_model", "BAAI/bge-small-en-v1.5")
        # Use LangChain's built-in FastEmbedEmbeddings
        self.embeddings = FastEmbedEmbeddings(model_name=self.embedding_model_name)
        self.client = self._connect_to_qdrant()
        self.vector_store = self._initialize_vector_store()
    
    def _connect_to_qdrant(self) -> QdrantClient: # Keep QdrantClient type hint for clarity
        """Connect to Qdrant using the centralized utility function."""
        # The utility function already handles printing messages and raising errors.
        return connect_to_qdrant()
    
    def _initialize_vector_store(self) -> Optional[QdrantVectorStore]:
        """Initialize the vector store for retrieval."""
        try:
            # Check if collection exists
            collections = [c.name for c in self.client.get_collections().collections]
            if self.collection_name not in collections:
                rprint(f"[yellow]⚠️ Collection '{self.collection_name}' not found. Creating empty collection.[/yellow]")
                # Create an empty collection
                vector_size = len(self.embeddings.embed_query("test"))
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=vector_size,
                        distance=qmodels.Distance.COSINE
                    )
                )
            
            return QdrantVectorStore(
                client=self.client, 
                collection_name=self.collection_name,
                embedding=self.embeddings
            )
        except Exception as e:
            rprint(f"[red]❌ Failed to initialize vector store: {e}[/red]")
            return None
    
    def has_documents(self) -> bool:
        """Check if the collection has any documents."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count > 0
        except Exception:
            return False

# --------------------------------------------------------------------------- #
#                              Retrieval Service                              #
# --------------------------------------------------------------------------- #
class RetrievalService:
    """
    Service for retrieving relevant documents from the vector database
    and generating answers using the LLM, with robust error handling and fallbacks.
    """
    
    def __init__(self, vector_db: VectorDatabase, llm: BaseChatModel, config: ConfigManager):
        self.vector_db = vector_db
        self.llm = llm
        self.config = config
        self.top_k = config.get("top_k", 5)
        self.similarity_threshold = config.get("similarity_threshold", 0.5)
        self.retrieval_chain = self._create_retrieval_chain() if vector_db.vector_store else None
        # Track service health
        self.vector_store_healthy = True if vector_db.vector_store else False
    
    def _create_retrieval_chain(self):
        """Create a retrieval chain for answering questions with context."""
        try:
            # Create a retriever with error handling
            retriever = self.vector_db.vector_store.as_retriever(
                search_kwargs={"k": self.top_k, "score_threshold": self.similarity_threshold}
            )
            
            # Define the prompt template with context
            template = self.config.get("prompt_template")
            # Create a properly formatted prompt template without empty variables
            # This fixes the "Input to ChatPromptTemplate is missing variables {''}" error
            prompt = ChatPromptTemplate.from_template(template.replace("{}", ""))
            
            # Create a retrieval chain
            retrieval_chain = (
                {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            return retrieval_chain
        except Exception as e:
            rprint(f"[red]❌ Failed to create retrieval chain: {e}[/red]")
            self.vector_store_healthy = False
            return None
    
    def _format_docs(self, docs):
        """Format retrieved documents into a context string."""
        if not docs:
            return "No relevant documents found in the knowledge base."
            
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown")
            context_parts.append(f"[Document {i}] {doc.page_content}\nSource: {source}")
        
        return "\n\n".join(context_parts)
    
    def retrieve_and_answer(self, query: str, messages: List[BaseMessage]) -> str:
        """
        Retrieves relevant documents based on the query and generates an answer.
        
        First attempts to use the RAG (Retrieval Augmented Generation) chain if the
        vector store is healthy and contains documents. If RAG fails or is unavailable,
        it falls back to a direct LLM response.

        Args:
            query (str): The user's query.
            messages (List[BaseMessage]): The history of messages for context.

        Returns:
            str: The generated answer.
            
        Raises:
            Exception: If the direct LLM response also fails.
        """
        # Check if vector store is healthy and has documents
        has_docs = False
        try:
            has_docs = self.vector_db.has_documents() if self.vector_store_healthy else False
        except Exception as e:
            rprint(f"[yellow]⚠️ Error checking for documents: {e}[/yellow]")
            self.vector_store_healthy = False
            has_docs = False
        
        # First try: Use retrieval chain if available and healthy
        if self.retrieval_chain and has_docs and self.vector_store_healthy:
            try:
                rprint("[cyan]🔍 Using RAG to answer query...[/cyan]")
                return self.retrieval_chain.invoke(query)
            except Exception as e:
                # Check if it's a connection error
                if "Connection refused" in str(e) or "Max retries exceeded" in str(e):
                    rprint(f"[yellow]⚠️ Vector store connection error: {e}[/yellow]")
                    self.vector_store_healthy = False
                else:
                    rprint(f"[yellow]⚠️ Retrieval error: {e}[/yellow]")
                # Continue to fallback
        
        # Second try: Fall back to direct LLM response
        try:
            rprint("[cyan]🔍 Using direct LLM response...[/cyan]")
            return self.llm.invoke(messages).content
        except Exception as e:
            rprint(f"[red]❌ LLM response error: {e}[/red]")
            # Let the caller handle this error
            raise e

# --------------------------------------------------------------------------- #
#                                Web Search                                   #
# --------------------------------------------------------------------------- #
class WebSearchService:
    """
    Service for performing web searches as a fallback or direct command.
    Uses the Exa API for search functionality.
    """
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.api_key = os.getenv("EXA_API_KEY")
        self.enabled = config.get("use_web_fallback", True) and self.api_key is not None
        self.n_results = config.get("web_results", 3)
    
    def search(self, query: str) -> str:
        """Search the web for information."""
        if not self.enabled:
            return "Web search is not configured. Add EXA_API_KEY to your .env file."
        
        try:
            exa_client = Exa(api_key=self.api_key)
            results = exa_client.search(query, num_results=self.n_results, use_autoprompt=True)
            
            content = []
            for i, result in enumerate(results.results, 1):
                title = result.title
                url = result.url
                content_snippet = result.text
                content.append(f"[{i}] {title}\n{url}\n{content_snippet}\n")
            
            return "\n\n".join(content)
        except Exception as e:
            return f"Error during web search: {str(e)}"

# --------------------------------------------------------------------------- #
#                               Memory Service                                #
# --------------------------------------------------------------------------- #
class ChatMemory:
    """
    Manages the conversation history (memory) for the chat agent.
    Allows adding messages, retrieving history, clearing memory, and enabling/disabling memory.
    """
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.messages: List[BaseMessage] = []
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the history if memory is enabled."""
        if self.enabled:
            self.messages.append(message)
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages in the history."""
        return self.messages if self.enabled else []
    
    def clear(self) -> None:
        """Clear the message history."""
        self.messages = []
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable memory."""
        self.enabled = enabled

# --------------------------------------------------------------------------- #
#                               Command Pattern                               #
# --------------------------------------------------------------------------- #
class Command(ABC):
    """Abstract base class for defining agent commands."""
    
    @abstractmethod
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Executes the command.

        Args:
            args (str): Arguments for the command.
            agent (LearningAgent): The instance of the LearningAgent.

        Returns:
            bool: True if the agent should continue running, False to exit.
        """
        pass

class ExitCommand(Command):
    """Command to exit the chat application."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        rprint("\n[bold]Goodbye! 👋[/bold]") # Moved message here from agent.run()
        return False

class MemoryCommand(Command):
    """Command to manage chat memory settings (on/off)."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        if args.lower() in ["on", "true", "yes", "1"]:
            agent.memory.set_enabled(True)
            rprint("[green]✅ Memory turned ON[/green]")
        elif args.lower() in ["off", "false", "no", "0"]:
            agent.memory.set_enabled(False)
            rprint("[green]✅ Memory turned OFF[/green]")
        else:
            rprint(f"[yellow]Memory is currently: {'ON' if agent.memory.enabled else 'OFF'}[/yellow]")
        return True

class SearchCommand(Command):
    """Command to perform a web search using the WebSearchService."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        if not args:
            rprint("[yellow]⚠️ Please provide a search query[/yellow]")
            return True
        
        rprint(f"[cyan]🔍 Web search for: {args}[/cyan]")
        results = agent.web_search.search(args)
        
        rprint(Panel(results, title="Web Search Results", expand=False))
        return True

class ProviderCommand(Command):
    """Command to switch the LLM provider (e.g., ollama, openrouter) and optionally the model."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        parts = args.split()
        if not parts:
            current_provider = agent.config.get('model_provider')
            current_model = agent.config.get('model')
            
            rprint(f"\n[bold cyan]🤖 Current Model Configuration:[/bold cyan]")
            rprint(f"  Provider: [green]{current_provider}[/green]")
            
            if current_provider == "ollama":
                rprint(f"  Model: [green]{current_model}[/green]")
                # Check if Ollama is running
                if LLMFactory.check_ollama_service():
                    rprint("  Status: [green]Ollama service is running[/green]")
                else:
                    rprint("  Status: [yellow]⚠️ Ollama service not detected[/yellow]")
                    rprint("  [yellow]💡 Start Ollama with 'ollama serve' in a separate terminal[/yellow]")
            else:  # openrouter
                openrouter_model = agent.config.get('openrouter_model')
                rprint(f"  Model: [green]{openrouter_model}[/green]")
                if os.getenv("OPENAI_API_KEY"):
                    rprint("  Status: [green]OpenRouter API key detected[/green]")
                else:
                    rprint("  Status: [yellow]⚠️ OpenRouter API key not found[/yellow]")
                    rprint("  [yellow]💡 Add OPENAI_API_KEY to your .env file[/yellow]")
            
            rprint("\n[dim]Use :provider ollama or :provider openrouter to switch[/dim]")
            return True
        
        provider = parts[0].lower()
        if provider not in ["ollama", "openrouter"]:
            rprint("[yellow]⚠️ Invalid provider. Use 'ollama' or 'openrouter'[/yellow]")
            rprint("[yellow]💡 Try :help provider for more information[/yellow]")
            return True
        
        # Store old provider for comparison
        old_provider = agent.config.get('model_provider')
        old_model = agent.config.get('model') if provider == "ollama" else agent.config.get('openrouter_model')
        
        # Update provider
        agent.config.update("model_provider", provider)
        
        # Update model if specified
        if len(parts) > 1:
            model_name = parts[1]
            if provider == "ollama":
                agent.config.update("model", model_name)
            else:  # openrouter
                agent.config.update("openrouter_model", model_name)
        
        # Get the new model name for display
        new_model = agent.config.get('model') if provider == "ollama" else agent.config.get('openrouter_model')
        
        # Check prerequisites before switching
        if provider == "ollama" and not LLMFactory.check_ollama_service():
            rprint("[yellow]⚠️ Ollama service not detected on port 11434[/yellow]")
            rprint("[yellow]💡 To start Ollama, open a new terminal and run: ollama serve[/yellow]")
        
        if provider == "openrouter" and not os.getenv("OPENAI_API_KEY"):
            rprint("[yellow]⚠️ OpenRouter requires an API key[/yellow]")
            rprint("[yellow]💡 Add OPENAI_API_KEY=your_openrouter_key to .env file[/yellow]")
        
        # Only recreate LLM if provider or model changed
        if old_provider != provider or old_model != new_model:
            try:
                rprint(f"[cyan]🔄 Switching to {provider} with model: {new_model}...[/cyan]")
                agent.llm = LLMFactory.create_llm(agent.config)
                # Recreate retrieval service with new LLM
                agent.retrieval = RetrievalService(agent.vector_db, agent.llm, agent.config)
                rprint(f"[green]✅ Successfully switched to {provider} with model: {new_model}[/green]")
            except Exception as e:
                rprint(f"[red]❌ Failed to switch provider: {e}[/red]")
                if provider == "ollama":
                    rprint("[yellow]💡 Make sure Ollama is running and the model is downloaded[/yellow]")
                    rprint("[yellow]💡 Try 'ollama list' to see available models[/yellow]")
                else:  # openrouter
                    rprint("[yellow]💡 Check your OpenRouter API key and internet connection[/yellow]")
        else:
            rprint(f"[cyan]ℹ️ Already using {provider} with model: {new_model}[/cyan]")
        
        return True

class ConfigCommand(Command):
    """Command to display the current agent configuration (excluding sensitive or complex fields)."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        rprint("\n[bold]Current Configuration:[/bold]")
        for key, value in agent.config.config.items():
            # Skip complex objects and templates
            if key != "prompt_template":
                rprint(f"  {key}: {value}")
        return True

class DbCommand(Command):
    """
    Command to manage and audit the vector database.
    Supports sub-commands like status, audit, search, and search-view.
    """
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        parts = args.split()
        action = parts[0].lower() if parts else "status"
        
        if action == "status" or action == "info":
            self._show_db_status(agent)
        elif action == "audit":
            # Parse additional arguments for audit
            audit_args = []
            if len(parts) > 1:
                audit_args = parts[1:]
            self._run_audit(audit_args)
        elif action == "search":
            self._search_db(agent, " ".join(parts[1:]) if len(parts) > 1 else "")
        elif action == "search-view" and len(parts) > 1:
            try:
                doc_num = int(parts[1])
                self._view_search_result(agent, doc_num)
            except ValueError:
                rprint("[yellow]⚠️ Please provide a valid document number[/yellow]")
                rprint("[yellow]💡 Usage: :db search-view <number>[/yellow]")
        else:
            rprint("[yellow]⚠️ Unknown database command. Try :db status, :db audit, or :db search <query>[/yellow]")
            rprint("[yellow]💡 Use :help db for more information[/yellow]")
        
        return True
    
    def _show_db_status(self, agent):
        """Show basic database status."""
        if not agent.vector_db or not agent.vector_db.client:
            rprint("[yellow]⚠️ Vector database is not connected[/yellow]")
            return
        
        try:
            # Use the audit_qdrant.py script with --summary flag for consistent output
            import subprocess
            import sys
            
            rprint("[cyan]🔍 Checking database status...[/cyan]")
            
            cmd = [sys.executable, "audit_qdrant.py", "--summary"]
            subprocess.run(cmd)
            
            # Add additional agent-specific information
            rprint(f"\n[bold cyan]🤖 Agent Database Connection:[/bold cyan]")
            rprint(f"  RAG Status: [green]{'Active' if agent.retrieval and agent.retrieval.vector_store_healthy else 'Inactive'}[/green]")
            
            if agent.retrieval and not agent.retrieval.vector_store_healthy:
                rprint("[yellow]⚠️ Vector store connection issues detected[/yellow]")
            
            rprint("\n[dim]For detailed information, run :db audit or python audit_qdrant.py[/dim]")
        except Exception as e:
            rprint(f"[red]❌ Error checking database status: {e}[/red]")
            rprint("[yellow]💡 Make sure audit_qdrant.py exists in the current directory[/yellow]")
    
    def _search_db(self, agent: 'LearningAgent', query: str):
        """Search the database and show raw results."""
        if not query.strip():
            rprint("[yellow]⚠️ Please provide a search query[/yellow]")
            rprint("[yellow]💡 Usage: :db search <your query>[/yellow]")
            return
            
        try:
            rprint(f"[bold cyan]🔍 Database Search Results for: \"{query}\"[/bold cyan]")
            
            # Check if vector database is initialized
            if not agent.vector_db or not agent.vector_db.vector_store:
                rprint("[red]❌ Vector database not initialized or unavailable[/red]")
                return
                
            # Get search parameters from config
            top_k = agent.config.get("top_k", 5)
            similarity_threshold = agent.config.get("similarity_threshold", 0.5)
            db_search_limit = agent.config.get("db_search_limit", 20)
            
            # Create a retriever with the same parameters as the agent uses
            retriever = agent.vector_db.vector_store.as_retriever(
                search_kwargs={"k": min(top_k, db_search_limit), "score_threshold": similarity_threshold}
            )
            
            # Perform the search
            docs = retriever.get_relevant_documents(query)
            
            if not docs:
                rprint("[yellow]⚠️ No matching documents found[/yellow]")
                return
                
            # Store the search results for later viewing
            self.last_search_results = docs
            
            # Display results with similarity scores
            rprint(f"[green]✅ Found {len(docs)} relevant documents[/green]")
            rprint(f"[dim]Using top_k={top_k}, similarity_threshold={similarity_threshold}[/dim]\n")
            
            from rich.table import Table
            table = Table(title="Search Results")
            table.add_column("#", style="cyan", justify="right")
            table.add_column("Score", style="green", justify="right")
            table.add_column("Source", style="yellow")
            table.add_column("Content Preview", style="white")
            
            for i, doc in enumerate(docs, 1):
                # Get metadata
                source = doc.metadata.get("source", "unknown")
                score = doc.metadata.get("score", "N/A")
                
                # Truncate content for preview
                content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                
                # Add to table
                table.add_row(str(i), f"{score:.4f}" if isinstance(score, float) else str(score), 
                             source, content_preview)
            
            from rich.console import Console
            console = Console()
            console.print(table)
            
            # Show the exact context that would be sent to the LLM
            if agent.retrieval:
                rprint("\n[bold cyan]🔄 Context that would be sent to the LLM:[/bold cyan]")
                formatted_context = agent.retrieval._format_docs(docs)
                
                # Try to render as markdown if enabled
                if agent.config.get("use_markdown_rendering", True):
                    try:
                        from rich.markdown import Markdown
                        from rich.panel import Panel
                        md = Markdown(formatted_context)
                        console.print(Panel(md, title="Context for LLM", expand=False))
                    except Exception:
                        # Fall back to plain text
                        console.print(Panel(formatted_context, title="Context for LLM", expand=False))
                else:
                    console.print(Panel(formatted_context, title="Context for LLM", expand=False))
            
            # Ask if user wants to see full content of any document
            rprint("\n[dim]To view full content of a document, use :db search-view <number>[/dim]")
            
        except Exception as e:
            rprint(f"[red]❌ Error searching database: {e}[/red]")
    
    def _view_search_result(self, agent: 'LearningAgent', doc_num: int):
        """View the full content of a specific search result."""
        if not hasattr(self, 'last_search_results') or not self.last_search_results:
            rprint("[yellow]⚠️ No search results available. Run :db search <query> first.[/yellow]")
            return
        
        if doc_num < 1 or doc_num > len(self.last_search_results):
            rprint(f"[yellow]⚠️ Invalid document number. Please choose between 1 and {len(self.last_search_results)}[/yellow]")
            return
        
        # Get the requested document (1-indexed for user, 0-indexed for list)
        doc = self.last_search_results[doc_num - 1]
        source = doc.metadata.get("source", "unknown")
        score = doc.metadata.get("score", "N/A")
        
        # Display the full document content
        from rich.panel import Panel
        from rich.markdown import Markdown
        from rich.console import Console
        
        console = Console()
        
        # Create header with metadata
        header = f"Document {doc_num} | Source: {source} | Score: {score:.4f if isinstance(score, float) else score}"
        
        # Display the full content
        if agent.config.get("use_markdown_rendering", True):
            # Try to render as markdown
            try:
                md = Markdown(doc.page_content)
                console.print(Panel(md, title=header, expand=False))
            except Exception:
                # Fall back to plain text if markdown rendering fails
                console.print(Panel(doc.page_content, title=header, expand=False))
        else:
            # Use plain text panel
            console.print(Panel(doc.page_content, title=header, expand=False))
    
    def _run_audit(self, args):
        """Run the audit_qdrant.py script with arguments."""
        import subprocess
        import sys
        
        cmd = [sys.executable, "audit_qdrant.py"]
        for arg in args:
            cmd.append(arg)
        
        rprint(f"[cyan]🔍 Running database audit: {' '.join(cmd)}[/cyan]")
        
        try:
            subprocess.run(cmd)
        except Exception as e:
            rprint(f"[red]❌ Error running audit: {e}[/red]")
            rprint("[yellow]💡 Make sure audit_qdrant.py exists in the current directory[/yellow]")


class HelpCommand(Command):
    """Command to display help information for general commands, database, or provider settings."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        if args.lower() == "db" or args.lower() == "database":
            self._show_db_help()
        elif args.lower() == "provider" or args.lower() == "model":
            self._show_provider_help()
        else:
            self._show_general_help()
        return True
    
    def _show_general_help(self):
        rprint("""
[bold cyan]📚 LearningAgent Help[/bold cyan]

Available commands:
  :exit, :quit       - Exit the chat
  :memory on/off     - Turn memory on or off
  :search <query>    - Search the web for information
  :provider <name>   - Switch between 'ollama' and 'openrouter'
  :config            - Show current configuration
  :db                - Manage and audit the vector database
  :db status         - Show database connection status
  :db audit          - Run detailed database audit
  :db search <query> - Search the database and see raw results
  :help              - Show this help message
  :help db           - Show database management help
  :help provider     - Show model provider help
        """)
    
    def _show_db_help(self):
        rprint("""
[bold cyan]🗄️ Database Management Help[/bold cyan]

Managing your vector database:

[bold]Database commands:[/bold]
  • [green]:db status[/green]: Show database connection status
  • [green]:db audit[/green]: Run detailed database audit
  • [green]:db search <query>[/green]: Search the database and see raw results

[bold]Auditing the database:[/bold]
  Run [green]python audit_qdrant.py[/green] or [green]make audit[/green] to:
  • View collection statistics
  • See sample documents
  • Check vector counts and configuration

[bold]Command options:[/bold]
  • [green]--count N[/green]: Show N sample documents (default: 5)
  • [green]--full[/green]: Show complete document contents
  • [green]--export FILE[/green]: Save audit results to a file
  • [green]--points N[/green]: Show specific number of points

[bold]Other database operations:[/bold]
  • [green]make start_qdrant[/green]: Start the Qdrant Docker container
  • [green]make stop_qdrant[/green]: Stop and remove the container
  • [green]make clean[/green]: Delete all vector data (CAUTION!)
  • [green]make ingest[/green]: Add documents from ./docs directory
        """)
    
    def _show_provider_help(self):
        rprint("""
[bold cyan]🔄 Model Provider Help[/bold cyan]

Switching between model providers:

[bold]Current providers:[/bold]
  • [green]ollama[/green]: Local models via Ollama (default)
  • [green]openrouter[/green]: Cloud models via OpenRouter API

[bold]Switching providers:[/bold]
  • [green]:provider ollama[/green]: Switch to local Ollama
  • [green]:provider openrouter[/green]: Switch to OpenRouter

[bold]Specifying models:[/bold]
  • [green]:provider ollama qwen3:4b[/green]: Use specific Ollama model
  • [green]:provider openrouter deepseek/deepseek-prover-v2:free[/green]: Use specific OpenRouter model

[bold]Requirements:[/bold]
  • Ollama: Must be running locally (start with [green]ollama serve[/green])
  • OpenRouter: Requires API key in .env file as OPENAI_API_KEY

[bold]Configuration:[/bold]
  • Default models are set in config.yaml
  • Use [green]:config[/green] to view current settings
        """)


# --------------------------------------------------------------------------- #
#                              Learning Agent                                 #
# --------------------------------------------------------------------------- #
class LearningAgent:
    """
    The main class for the Learning Agent.
    It initializes and coordinates all components including configuration,
    LLM, vector database, retrieval services, web search, memory, and commands.
    It also contains the main chat loop.
    """
    
    def __init__(self):
        # Load configuration
        self.config = ConfigManager()
        
        # Initialize components
        self.memory = ChatMemory(enabled=self.config.get("use_memory", True))
        
        # Initialize LLM with better fallback handling
        self.llm = self._initialize_llm()
        
        # Initialize vector database with better error handling
        self.vector_db = self._initialize_vector_db()
        
        # Initialize retrieval service if vector DB is available
        if self.vector_db:
            self.retrieval = self._initialize_retrieval_service()
        else:
            self.retrieval = None
        
        # Initialize web search
        self.web_search = WebSearchService(self.config)
        
        # Define message prefixes for output formatting
        self.ASSISTANT_PREFIX = "🤖"
        self.SYSTEM_PREFIX = "🔧"
        self.USER_PREFIX = "💬"
        
        # Register commands
        self.commands = {
            "exit": ExitCommand(),
            "quit": ExitCommand(),
            "memory": MemoryCommand(),
            "search": SearchCommand(),
            "provider": ProviderCommand(),
            "config": ConfigCommand(),
            "db": DbCommand(),
            "help": HelpCommand()
        }
    
    def _initialize_llm(self):
        """Initialize LLM with improved fallback mechanisms."""
        # Try to create the LLM using the factory, which now has built-in fallback logic
        try:
            return LLMFactory.create_llm(self.config)
        except Exception as e:
            rprint(f"[red]❌ All LLM initialization attempts failed: {e}[/red]")
            
            # Create a dummy LLM that returns helpful error messages
            rprint("[yellow]⚠️ Using emergency fallback mode - limited functionality[/yellow]")
            return self._create_emergency_llm()
    
    def _create_emergency_llm(self):
        """Create an emergency LLM that returns helpful error messages."""
        # This is a simple class that mimics the BaseChatModel interface
        # but returns helpful error messages with troubleshooting steps
        class EmergencyLLM(BaseChatModel):
            def _generate(self, messages, stop=None, run_manager=None, **kwargs):
                from langchain_core.messages import AIMessage
                from langchain_core.outputs import ChatGeneration, ChatResult
                
                # Create a helpful error message with troubleshooting steps
                response = "I'm currently running in emergency mode with limited functionality. "
                
                if self.config.get("model_provider") == "ollama":
                    response += "\n\nTroubleshooting Ollama connection issues:\n"
                    response += "1. Make sure Ollama is running with 'ollama serve' in a separate terminal\n"
                    response += "2. Check if the model is downloaded with 'ollama list'\n"
                    response += "3. Try switching to OpenRouter with ':provider openrouter' if you have an API key configured\n"
                    response += "4. Restart the application after starting Ollama"
                else:  # OpenRouter
                    response += "\n\nTroubleshooting OpenRouter connection issues:\n"
                    response += "1. Check your OPENAI_API_KEY in the .env file\n"
                    response += "2. Verify your internet connection\n"
                    response += "3. Try switching to Ollama with ':provider ollama' if you have it installed\n"
                    response += "4. Check the OpenRouter status page for service disruptions"
                
                message = AIMessage(content=response)
                generation = ChatGeneration(message=message)
                return ChatResult(generations=[generation])
            
            def __init__(self, config=None):
                super().__init__()
                self.config = config
            
            @property
            def _llm_type(self):
                return "emergency_llm"
        
        return EmergencyLLM(config=self.config)
    
    def _initialize_vector_db(self):
        """Initialize vector database with better error handling."""
        try:
            return VectorDatabase(self.config)
        except Exception as e:
            rprint(f"[yellow]⚠️ Vector database initialization failed: {e}[/yellow]")
            rprint("[yellow]💡 RAG functionality will be unavailable[/yellow]")
            return None
    
    def _initialize_retrieval_service(self):
        """Initialize retrieval service with error handling."""
        try:
            return RetrievalService(self.vector_db, self.llm, self.config)
        except Exception as e:
            rprint(f"[yellow]⚠️ Retrieval service initialization failed: {e}[/yellow]")
            return None
        
        # Commands are now initialized in __init__
    
    def process_command(self, cmd: str, args: str) -> bool:
        """Process command inputs starting with ':'."""
        cmd = cmd.lower()
        
        if cmd in self.commands:
            return self.commands[cmd].execute(args, self)
        else:
            rprint(f"[yellow]⚠️ Unknown command: {cmd}[/yellow]")
            return True
    
    def generate_response(self, user_input: str) -> str:
        """Generate a response to user input with robust error handling."""
        # Create user message
        user_message = HumanMessage(content=user_input)
        
        # Prepare messages for the model
        messages_for_model = []
        messages_for_model.extend(self.memory.get_messages())
        messages_for_model.append(user_message)
        
        # Add user message to memory
        self.memory.add_message(user_message)
        
        # Try web search fallback if enabled
        web_results = None
        if self.config.get("use_web_fallback", True):
            try:
                web_results = self.web_search.search(user_input)
            except Exception as web_e:
                rprint(f"[yellow]⚠️ Web search fallback failed: {web_e}[/yellow]")
        
        try:
            # First try: Generate response using retrieval if available
            if self.retrieval:
                try:
                    response = self.retrieval.retrieve_and_answer(user_input, messages_for_model)
                    # Add AI message to memory
                    self.memory.add_message(AIMessage(content=response))
                    return response
                except Exception as retrieval_e:
                    rprint(f"[yellow]⚠️ Retrieval failed, falling back to direct LLM: {retrieval_e}[/yellow]")
                    # Fall through to direct LLM response
            
            # Second try: Direct LLM response without retrieval
            try:
                response = self.llm.invoke(messages_for_model).content
                # Add AI message to memory
                self.memory.add_message(AIMessage(content=response))
                return response
            except Exception as llm_e:
                # If we have web results, use them in the error message
                if web_results and not web_results.startswith("Error"):
                    rprint(f"[yellow]⚠️ LLM response failed, using web results: {llm_e}[/yellow]")
                    web_response = f"I couldn't access my knowledge base, but I found this on the web:\n\n{web_results}"
                    self.memory.add_message(AIMessage(content=web_response))
                    return web_response
                else:
                    # Re-raise to be caught by the outer exception handler
                    raise llm_e
        except Exception as e:
            # Format error message based on the type of error
            if "Connection refused" in str(e) or "Max retries exceeded" in str(e):
                error_msg = "I couldn't connect to the language model service (Ollama). "
                error_msg += "\n\nTroubleshooting steps:\n"
                error_msg += "1. Make sure Ollama is running with 'ollama serve' in a separate terminal\n"
                error_msg += "2. Check if the model is downloaded with 'ollama list'\n"
                error_msg += "3. Try switching to OpenRouter with ':provider openrouter' if you have an API key configured\n"
                error_msg += "4. Restart the application after starting Ollama"
            elif "API key" in str(e):
                error_msg = "There was an issue with the API key. "
                error_msg += "\n\nTroubleshooting steps:\n"
                error_msg += "1. Check your .env file and ensure you have the correct API keys configured\n"
                error_msg += "2. For OpenRouter, make sure OPENAI_API_KEY is set to your OpenRouter API key\n"
                error_msg += "3. Try switching to Ollama with ':provider ollama' if you have it installed"
            else:
                error_msg = f"Error generating response: {e}\n\n"
                error_msg += "Try using ':help' to see available commands or ':provider' to switch providers."
            
            rprint(f"[red]❌ {error_msg}[/red]")
            return f"I encountered an error: {error_msg}"
    
    def run(self):
        """Runs the main chat loop for the Learning Agent."""
        # Initial greeting messages
        # Using rprint for consistency with other console outputs
        rprint("\n[bold green]✨ Initializing LearningAgent...[/bold green]") 
        rprint("\n[bold cyan]💬 LearningAgent ready! Type a question or use ':help' for commands.[/bold cyan]\n")
        
        while True:
            try:
                user_input = input("> ").strip() # Added strip() here for consistency
            except (KeyboardInterrupt, EOFError):
                # User initiated exit (Ctrl+C or Ctrl+D)
                # The ExitCommand now handles printing the goodbye message.
                # Simply break the loop.
                break 
            
            if not user_input: # Check if input is empty after strip
                continue
            
            # Process commands (starting with :)
            if user_input.startswith(":"):
                parts = user_input[1:].strip().split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                should_continue = self.process_command(cmd, args)
                if not should_continue:
                    break
                continue
            
            # Generate a response
            rprint("[cyan]🔍 Thinking...[/cyan]")
            response = self.generate_response(user_input)
            
            # Display the response with markdown and LaTeX rendering if enabled
            if self.config.get("use_markdown_rendering", True):
                try:
                    from rich.markdown import Markdown # Moved import here, only needed if rendering
                    from rich.console import Console # Moved import here
                    from rich.panel import Panel # Moved import here
                    
                    # LaTeX processing block
                    if self.config.get("enable_latex_processing", True):
                        import re # Moved import here, only needed for LaTeX
                        
                        if self.config.get("use_advanced_latex_rendering", True):
                            # This block contains numerous regex substitutions for LaTeX to text/markup.
                            # Order of substitutions is crucial for correctness.
                            
                            # 1. Complex Block Environments (e.g., matrices) & Display Style
                            response = re.sub(r'\\begin\{(matrix|pmatrix|bmatrix|vmatrix|Vmatrix|array)\}[\s\S]*?\end\{\1\}', r'[matrix representation]', response, flags=re.DOTALL) # Clarified placeholder
                            response = re.sub(r'\\displaystyle', '', response) # Remove display style command

                            # 2. Fractions, Binomials
                            response = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', response) # Simpler fraction
                            response = re.sub(r'\\binom\{([^}]+)\}\{([^}]+)\}', r'C(\1, \2)', response) # Binomial coefficient

                            # 3. Radicals
                            response = re.sub(r'\\sqrt\[([^]]+)\]\{([^}]+)\}', r'\1th_root(\2)', response) # nth root
                            response = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\2)', response) # Square root - corrected group index

                            # 4. Accents
                            response = re.sub(r'\\hat\{([a-zA-Z0-9])\}', r'\1'+'\u0302', response)  # Combining circumflex
                            response = re.sub(r'\\bar\{([a-zA-Z0-9])\}', r'\1'+'\u0304', response)  # Combining macron
                            response = re.sub(r'\\tilde\{([a-zA-Z0-9])\}', r'\1'+'\u0303', response) # Combining tilde
                            response = re.sub(r'\\vec\{([a-zA-Z0-9])\}', r'\1'+'\u20D7', response) # Combining right arrow above
                            response = re.sub(r'\\dot\{([a-zA-Z0-9])\}', r'\1'+'\u0307', response)  # Combining dot above
                            response = re.sub(r'\\ddot\{([a-zA-Z0-9])\}', r'\1'+'\u0308', response) # Combining diaeresis

                            # 5. Subscripts & Superscripts (using Rich tags for better rendering)
                            # Process multi-character sub/sup first
                            response = re.sub(r'_\{([^}]+)\}', r'[sub]\1[/sub]', response) 
                            response = re.sub(r'\^\{([^}]+)\}', r'[sup]\1[/sup]', response)
                            # Process single character sub/sup (avoiding interference with escaped chars or other commands)
                            response = re.sub(r'(?<![a-zA-Z0-9\\])_([a-zA-Z0-9])', r'[sub]\1[/sub]', response)
                            response = re.sub(r'(?<![a-zA-Z0-9\\])\^([a-zA-Z0-9])', r'[sup]\1[/sup]', response)
                            
                            # 6. Font Styles (textual representation)
                            response = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', response) # Roman
                            response = re.sub(r'\\mathbf\{([^}]+)\}', r'[b]\1[/b]', response) # Bold
                            response = re.sub(r'\\textit\{([^}]+)\}', r'[i]\1[/i]', response) # Italic
                            response = re.sub(r'\\texttt\{([^}]+)\}', r'[code]\1[/code]', response) # Monospace/code

                            # 7. Set Notation (mathbb) - Common Unicode symbols
                            response = re.sub(r'\\mathbb\{R\}', 'ℝ', response) # Real numbers
                            response = re.sub(r'\\mathbb\{Z\}', 'ℤ', response) # Integers
                            response = re.sub(r'\\mathbb\{N\}', 'ℕ', response) # Natural numbers
                            response = re.sub(r'\\mathbb\{Q\}', 'ℚ', response) # Rational numbers
                            response = re.sub(r'\\mathbb\{C\}', 'ℂ', response) # Complex numbers
                            response = re.sub(r'\\mathbb\{([a-zA-Z])\}', r'\1', response) # Fallback for other mathbb (plain char)

                            # 8. Calligraphic Notation (mathcal) - Textual representation
                            response = re.sub(r'\\mathcal\{([A-Z])\}', r'\1', response) # Uppercasemathcal to plain char for simplicity

                            # 9. Common Functions (remove backslash, ensure word boundary)
                            funcs = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'sinh', 'cosh', 'tanh',
                                     'log', 'ln', 'lim', 'liminf', 'limsup', 'exp', 'det', 'dim', 
                                     'min', 'max', 'sup', 'inf', 'arg', 'deg', 'gcd', 'lcm', 'ker', 'mod']
                            for func_name in funcs:
                                response = re.sub(r'\\' + func_name + r'(?!\w)', func_name, response)

                            # 10. Greek Letters & Common Math Symbols (Unicode)
                            response = response.replace('\\infty', '∞')
                            response = response.replace('\\pi', 'π')
                            response = response.replace('\\theta', 'θ') # Lowercase theta
                            response = response.replace('\\Theta', 'Θ') # Uppercase Theta
                            response = response.replace('\\alpha', 'α')
                            response = response.replace('\\beta', 'β')
                            response = response.replace('\\gamma', 'γ')
                            response = response.replace('\\Gamma', 'Γ') # Uppercase Gamma
                            response = response.replace('\\delta', 'δ')
                            response = response.replace('\\Delta', 'Δ') # Uppercase Delta
                            response = response.replace('\\epsilon', 'ε')
                            response = response.replace('\\varepsilon', 'ɛ')
                            response = response.replace('\\zeta', 'ζ')
                            response = response.replace('\\eta', 'η')
                            response = response.replace('\\iota', 'ι')
                            response = response.replace('\\kappa', 'κ')
                            response = response.replace('\\lambda', 'λ')
                            response = response.replace('\\Lambda', 'Λ') # Uppercase Lambda
                            response = response.replace('\\mu', 'μ')
                            response = response.replace('\\nu', 'ν')
                            response = response.replace('\\xi', 'ξ')
                            response = response.replace('\\Xi', 'Ξ') # Uppercase Xi
                            response = response.replace('\\rho', 'ρ')
                            response = response.replace('\\sigma', 'σ')
                            response = response.replace('\\Sigma', 'Σ') # Uppercase Sigma
                            response = response.replace('\\tau', 'τ')
                            response = response.replace('\\upsilon', 'υ')
                            response = response.replace('\\Upsilon', 'Υ') # Uppercase Upsilon
                            response = response.replace('\\phi', 'φ')
                            response = response.replace('\\Phi', 'Φ') # Uppercase Phi
                            response = response.replace('\\varphi', 'ϕ')
                            response = response.replace('\\chi', 'χ')
                            response = response.replace('\\psi', 'ψ')
                            response = response.replace('\\Psi', 'Ψ') # Uppercase Psi
                            response = response.replace('\\omega', 'ω')
                            response = response.replace('\\Omega', 'Ω') # Uppercase Omega
                            
                            response = response.replace('\\sum', '∑')
                            response = response.replace('\\prod', '∏')
                            response = response.replace('\\int', '∫')
                            response = response.replace('\\partial', '∂')
                            response = response.replace('\\nabla', '∇')
                            response = response.replace('\\pm', '±')
                            response = response.replace('\\times', '×')
                            response = response.replace('\\cdot', '·')
                            response = response.replace('\\approx', '≈')
                            response = response.replace('\\neq', '≠')
                            response = response.replace('\\leq', '≤')
                            response = response.replace('\\geq', '≥')
                            response = response.replace('\\ll', '≪')
                            response = response.replace('\\gg', '≫')
                            response = response.replace('\\subset', '⊂')
                            response = response.replace('\\supset', '⊃')
                            response = response.replace('\\subseteq', '⊆')
                            response = response.replace('\\supseteq', '⊇')
                            response = response.replace('\\in', '∈')
                            response = response.replace('\\notin', '∉')
                            response = response.replace('\\ni', '∋')
                            response = response.replace('\\leftarrow', '←')
                            response = response.replace('\\rightarrow', '→')
                            response = response.replace('\\leftrightarrow', '↔')
                            response = response.replace('\\Leftarrow', '⇐')
                            response = response.replace('\\Rightarrow', '⇒')
                            response = response.replace('\\Leftrightarrow', '⇔')
                            response = response.replace('\\uparrow', '↑')
                            response = response.replace('\\downarrow', '↓')
                            response = response.replace('\\updownarrow', '↕')
                            response = response.replace('\\forall', '∀')
                            response = response.replace('\\exists', '∃')
                            response = response.replace('\\emptyset', '∅')
                            response = response.replace('\\ldots', '...')
                            response = response.replace('\\cdots', '⋯')
                            response = response.replace('\\vdots', '⋮')
                            response = response.replace('\\ddots', '⋱')
                            response = response.replace('\\angle', '∠')
                            response = response.replace('\\hbar', 'ħ')
                            response = response.replace('\\degree', '°')
                            response = response.replace('\\prime', '′')
                            response = response.replace('\\{', '{') # Unescape escaped braces
                            response = response.replace('\\}', '}')
                            response = response.replace('\\%', '%')
                            response = response.replace('\\&', '&')
                            response = response.replace('\\#', '#')
                            response = response.replace('\\_', '_')

                        # 10. Inline Math Delimiters \(...\) and Display Math \[...\] (Rich Markdown emphasis)
                        # These should be applied after other LaTeX commands are processed.
                        response = re.sub(r'\\\((.+?)\\\)', r'[i] \1 [/i]', response) # Italic and math symbol for inline
                        response = re.sub(r'\\\[(.+?)\\\]', r'\n\n[b]\[ \1 \]\[/b]\n\n', response) # Bold for display math

                    # Create a console for rich output
                    console = Console()
                    
                    # Render the message as markdown in a panel
                    md = Markdown(response)
                    console.print(Panel(md, title="🤖 Agent", expand=False))
                except ImportError:
                    # Fall back to plain panel if rich markdown is not available
                    rprint(Panel(response, title="🤖 Agent", expand=False))
            else:
                # Use standard panel without markdown rendering
                rprint(Panel(response, title="🤖 Agent", expand=False))

def main():
    """Main entrypoint for the learning agent."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Create and run the agent
        # Note: LLMFactory now handles Ollama service checks internally
        agent = LearningAgent()
        agent.run()
    except Exception as e:
        rprint(f"[red]❌ Fatal error: {e}[/red]")
        import traceback
        rprint(traceback.format_exc())

if __name__ == "__main__":
    main()
