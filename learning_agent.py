"""
learning_agent.py
-----------------
A simplified RAG chat assistant with memory and retrieval capabilities.
Refactored with a class-based architecture for better maintainability.
"""

import os
import yaml
import warnings
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Callable
from abc import ABC, abstractmethod
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console
from dotenv import load_dotenv

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*was deprecated.*")
warnings.filterwarnings("ignore", message=".*TOKENIZERS_PARALLELISM.*")

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
from qdrant_client import QdrantClient
from qdrant_client import models as qmodels
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings

# Exa search for web fallback
from exa_py import Exa

# --------------------------------------------------------------------------- #
#                            Configuration Manager                            #
# --------------------------------------------------------------------------- #
class ConfigManager:
    """Manages configuration loading and access."""
    
    CONFIG_PATH = "config.yaml"
    DEFAULT_CONFIG = {
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
        "prompt_template": "Answer the question based on the following context. \nIf you don't know the answer, just say you don't know; don't make up information.\n\nContext:\n{context}\n\nQuestion: {question}\n"
    }
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not os.path.exists(self.CONFIG_PATH):
            rprint(f"[yellow]⚠️ Config file {self.CONFIG_PATH} not found, using defaults.[/yellow]")
            return self.DEFAULT_CONFIG

        try:
            with open(self.CONFIG_PATH, "r") as f:
                config = yaml.safe_load(f)
                # Merge with defaults for any missing keys
                return {**self.DEFAULT_CONFIG, **config}
        except Exception as e:
            rprint(f"[red]❌ Error loading config: {e}[/red]")
            return self.DEFAULT_CONFIG
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def update(self, key: str, value: Any) -> None:
        """Update a configuration value in memory."""
        self.config[key] = value

# --------------------------------------------------------------------------- #
#                                LLM Factory                                  #
# --------------------------------------------------------------------------- #
class LLMFactory:
    """Factory for creating LLM instances with robust error handling."""
    
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
        """Create an LLM instance based on the configured provider with fallback handling."""
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
    """Manages connections and operations with the vector database."""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.collection_name = config.get("collection", "kb")
        self.embedding_model_name = config.get("embedding_model", "BAAI/bge-small-en-v1.5")
        # Use LangChain's built-in FastEmbedEmbeddings
        self.embeddings = FastEmbedEmbeddings(model_name=self.embedding_model_name)
        self.client = self._connect_to_qdrant()
        self.vector_store = self._initialize_vector_store()
    
    def _connect_to_qdrant(self) -> QdrantClient:
        """Connect to Qdrant, prioritizing Docker over embedded."""
        # Try Docker connection first
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Test the connection
            client.get_collections()
            rprint("[green]✅ Connected to Docker Qdrant[/green]")
            return client
        except Exception as docker_e:
            rprint(f"[yellow]⚠️ Could not connect to Docker Qdrant: {docker_e}[/yellow]")
            
            # Try embedded Qdrant as fallback
            try:
                rprint("[cyan]🔄 Trying embedded Qdrant as fallback...[/cyan]")
                client = QdrantClient(path="./qdrant_data")
                client.get_collections()
                rprint("[green]✅ Connected to embedded Qdrant[/green]")
                return client
            except Exception as e:
                rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e}[/red]")
                rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant Docker[/yellow]")
                raise RuntimeError("Could not connect to any Qdrant instance")
    
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
    """Service for retrieving relevant documents with robust error handling."""
    
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
            prompt = ChatPromptTemplate.from_template(template)
            
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
        """Retrieve relevant documents and answer the query with fallback mechanisms."""
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
    """Service for web search fallback."""
    
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
    """Manages conversation history."""
    
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
    """Base command interface."""
    
    @abstractmethod
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """Execute the command."""
        pass

class ExitCommand(Command):
    """Command to exit the application."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        return False

class MemoryCommand(Command):
    """Command to manage memory settings."""
    
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
    """Command to search the web."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        if not args:
            rprint("[yellow]⚠️ Please provide a search query[/yellow]")
            return True
        
        rprint(f"[cyan]🔍 Web search for: {args}[/cyan]")
        results = agent.web_search.search(args)
        
        rprint(Panel(results, title="Web Search Results", expand=False))
        return True

class ProviderCommand(Command):
    """Command to switch LLM provider."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        parts = args.split()
        if not parts:
            rprint(f"[cyan]Current provider: {agent.config.get('model_provider')}, "
                   f"model: {agent.config.get('model')}[/cyan]")
            return True
        
        provider = parts[0].lower()
        if provider not in ["ollama", "openrouter"]:
            rprint("[yellow]⚠️ Invalid provider. Use 'ollama' or 'openrouter'[/yellow]")
            return True
        
        agent.config.update("model_provider", provider)
        
        if len(parts) > 1:
            agent.config.update("model", parts[1])
        
        # Update the LLM
        try:
            agent.llm = LLMFactory.create_llm(agent.config)
            # Recreate retrieval service with new LLM
            agent.retrieval = RetrievalService(agent.vector_db, agent.llm, agent.config)
            rprint(f"[green]✅ Switched to {provider} with model: {agent.config.get('model')}[/green]")
        except Exception as e:
            rprint(f"[red]❌ Failed to switch provider: {e}[/red]")
        
        return True

class ConfigCommand(Command):
    """Command to show current configuration."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        rprint("\n[bold]Current Configuration:[/bold]")
        for key, value in agent.config.config.items():
            # Skip complex objects and templates
            if key != "prompt_template":
                rprint(f"  {key}: {value}")
        return True

class HelpCommand(Command):
    """Command to show help information."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        rprint("""
Available commands:
  :exit, :quit       - Exit the chat
  :memory on/off     - Turn memory on or off
  :search <query>    - Search the web for information
  :provider <name>   - Switch between 'ollama' and 'openrouter'
  :config            - Show current configuration
  :help              - Show this help message
        """)
        return True

# --------------------------------------------------------------------------- #
#                              Learning Agent                                 #
# --------------------------------------------------------------------------- #
class LearningAgent:
    """Main agent class that coordinates all components."""
    
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
        
        # Register commands
        self.commands = {
            "exit": ExitCommand(),
            "quit": ExitCommand(),
            "memory": MemoryCommand(),
            "search": SearchCommand(),
            "provider": ProviderCommand(),
            "config": ConfigCommand(),
            "help": HelpCommand()
        }
    
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
        """Run the chat loop."""
        print("\n✨ Initializing LearningAgent...\n")
        rprint("\n[bold cyan]💬 LearningAgent ready! Type a question or use ':help' for commands.[/bold cyan]\n")
        
        while True:
            try:
                user_input = input("> ")
            except (KeyboardInterrupt, EOFError):
                rprint("\n[bold]Goodbye! 👋[/bold]")
                break
            
            if not user_input.strip():
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
            
            # Display the response
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
