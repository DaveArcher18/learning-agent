#!/usr/bin/env python
"""
fix_retrieval.py
--------------
A script to fix retrieval issues in the LearningAgent.

This script implements the recommended fixes from the debug report:
1. Adds timeout handling for Ollama connections
2. Improves error handling in the retrieval service
3. Implements a more robust fallback chain

Usage:
  python fix_retrieval.py
"""

import os
import sys
import signal
import yaml
from contextlib import contextmanager
from rich import print as rprint
from rich.panel import Panel

# Define timeout context manager for preventing hanging connections
@contextmanager
def timeout(seconds):
    """Context manager for timing out operations."""
    def signal_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")
    
    # Set the timeout handler
    original_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Restore original handler and disable the alarm
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


def patch_learning_agent():
    """Patch the learning_agent.py file with improved error handling."""
    try:
        # Check if learning_agent.py exists
        if not os.path.exists("learning_agent.py"):
            rprint("[red]❌ learning_agent.py not found[/red]")
            return False
        
        # Read the file content
        with open("learning_agent.py", "r") as f:
            content = f.read()
        
        # Check if the file has already been patched
        if "timeout_seconds" in content:
            rprint("[yellow]⚠️ learning_agent.py already appears to be patched[/yellow]")
            return True
        
        # Create backup
        with open("learning_agent.py.bak", "w") as f:
            f.write(content)
        rprint("[green]✅ Created backup at learning_agent.py.bak[/green]")
        
        # Add timeout context manager
        timeout_manager = """
# --------------------------------------------------------------------------- #
#                              Timeout Utilities                              #
# --------------------------------------------------------------------------- #
@contextmanager
def timeout(seconds):
    """Context manager for timing out operations."""
    def signal_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")
    
    # Set the timeout handler
    original_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Restore original handler and disable the alarm
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)
"""
        
        # Add import for contextlib and signal
        if "from contextlib import contextmanager" not in content:
            content = content.replace("import warnings\n", "import warnings\nimport signal\nfrom contextlib import contextmanager\n")
        
        # Add timeout manager after the imports section
        content = content.replace("# Exa search for web fallback\nfrom exa_py import Exa", "# Exa search for web fallback\nfrom exa_py import Exa\n" + timeout_manager)
        
        # Update RetrievalService.__init__ to include timeout settings
        retrieval_init_patch = """
    def __init__(self, vector_db: VectorDatabase, llm: BaseChatModel, config: ConfigManager):
        self.vector_db = vector_db
        self.llm = llm
        self.config = config
        self.top_k = config.get("top_k", 5)
        self.similarity_threshold = config.get("similarity_threshold", 0.5)
        self.timeout_seconds = config.get("retrieval_timeout", 30)  # Default 30 second timeout
        self.retrieval_chain = self._create_retrieval_chain() if vector_db.vector_store else None
        # Track service health
        self.vector_store_healthy = True if vector_db.vector_store else False
        self.web_search_enabled = config.get("use_web_fallback", True) and os.getenv("EXA_API_KEY") is not None"""
        
        content = content.replace("    def __init__(self, vector_db: VectorDatabase, llm: BaseChatModel, config: ConfigManager):\n        self.vector_db = vector_db\n        self.llm = llm\n        self.config = config\n        self.top_k = config.get(\"top_k\", 5)\n        self.similarity_threshold = config.get(\"similarity_threshold\", 0.5)\n        self.retrieval_chain = self._create_retrieval_chain() if vector_db.vector_store else None\n        # Track service health\n        self.vector_store_healthy = True if vector_db.vector_store else False", retrieval_init_patch)
        
        # Update retrieve_and_answer method with timeout handling
        retrieve_and_answer_patch = """
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
                # Add timeout handling for retrieval operations
                rprint("[cyan]🔍 Using RAG to answer query...[/cyan]")
                try:
                    with timeout(self.timeout_seconds):
                        return self.retrieval_chain.invoke(query)
                except TimeoutError:
                    rprint(f"[yellow]⚠️ Retrieval timed out after {self.timeout_seconds} seconds, falling back to alternatives[/yellow]")
                    # Continue to fallbacks
            except Exception as e:
                # Check if it's a connection error
                if "Connection refused" in str(e) or "Max retries exceeded" in str(e):
                    rprint(f"[yellow]⚠️ Vector store connection error: {e}[/yellow]")
                    self.vector_store_healthy = False
                else:
                    rprint(f"[yellow]⚠️ Retrieval error: {e}[/yellow]")
                # Continue to fallback
        
        # Second try: Try web search if enabled
        if self.web_search_enabled:
            try:
                rprint("[cyan]🔍 Trying web search fallback...[/cyan]")
                from exa_py import Exa
                exa_client = Exa(api_key=os.getenv("EXA_API_KEY"))
                results = exa_client.search(query, num_results=self.config.get("web_results", 3), use_autoprompt=True)
                
                if results and results.results:
                    # Format web results as context
                    web_context = []
                    for i, result in enumerate(results.results, 1):
                        title = result.title
                        url = result.url
                        content_snippet = result.text
                        web_context.append(f"[{i}] {title}\n{url}\n{content_snippet}\n")
                    
                    web_context_str = "\n\n".join(web_context)
                    
                    # Create a prompt with web context
                    template = self.config.get("prompt_template")
                    prompt = ChatPromptTemplate.from_template(template)
                    
                    # Generate response using web context
                    rprint("[cyan]🔍 Generating response from web results...[/cyan]")
                    try:
                        with timeout(self.timeout_seconds):
                            response = prompt.format(context=web_context_str, question=query)
                            return self.llm.invoke(response).content
                    except TimeoutError:
                        rprint(f"[yellow]⚠️ Web response generation timed out after {self.timeout_seconds} seconds[/yellow]")
                        # Fall through to direct LLM response
            except Exception as web_e:
                rprint(f"[yellow]⚠️ Web search fallback failed: {web_e}[/yellow]")
        
        # Third try: Direct LLM response without retrieval
        try:
            rprint("[cyan]🔍 Using direct LLM response...[/cyan]")
            return self.llm.invoke(messages).content
        except Exception as e:
            rprint(f"[red]❌ LLM response error: {e}[/red]")
            # Let the caller handle this error
            raise e"""
        
        content = content.replace("    def retrieve_and_answer(self, query: str, messages: List[BaseMessage]) -> str:\n        \"\"\"Retrieve relevant documents and answer the query with fallback mechanisms.\"\"\"\n        # Check if vector store is healthy and has documents\n        has_docs = False\n        try:\n            has_docs = self.vector_db.has_documents() if self.vector_store_healthy else False\n        except Exception as e:\n            rprint(f\"[yellow]⚠️ Error checking for documents: {e}[/yellow]\")\n            self.vector_store_healthy = False\n            has_docs = False\n        \n        # First try: Use retrieval chain if available and healthy\n        if self.retrieval_chain and has_docs and self.vector_store_healthy:\n            try:\n                rprint(\"[cyan]🔍 Using RAG to answer query...[/cyan]\")\n                return self.retrieval_chain.invoke(query)\n            except Exception as e:\n                # Check if it's a connection error\n                if \"Connection refused\" in str(e) or \"Max retries exceeded\" in str(e):\n                    rprint(f\"[yellow]⚠️ Vector store connection error: {e}[/yellow]\")\n                    self.vector_store_healthy = False\n                else:\n                    rprint(f\"[yellow]⚠️ Retrieval error: {e}[/yellow]\")\n                # Continue to fallback\n        \n        # Second try: Fall back to direct LLM response\n        try:\n            rprint(\"[cyan]🔍 Using direct LLM response...[/cyan]\")\n            return self.llm.invoke(messages).content\n        except Exception as e:\n            rprint(f\"[red]❌ LLM response error: {e}[/red]\")\n            # Let the caller handle this error\n            raise e", retrieve_and_answer_patch)
        
        # Update ConfigManager.DEFAULT_CONFIG to include retrieval_timeout
        default_config_patch = """    DEFAULT_CONFIG = {
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
        "retrieval_timeout": 30,  # Timeout in seconds for retrieval operations
        "prompt_template": "Answer the question based on the following context. \nIf you don't know the answer, just say you don't know; don't make up information.\n\nContext:\n{context}\n\nQuestion: {question}\n"
    }"""
        
        content = content.replace("    DEFAULT_CONFIG = {\n        \"model\": \"qwen3:4b\",\n        \"model_provider\": \"ollama\",\n        \"openrouter_model\": \"deepseek/deepseek-prover-v2:free\",\n        \"temperature\": 0.3,\n        \"use_memory\": True,\n        \"embedding_model\": \"BAAI/bge-small-en-v1.5\",\n        \"top_k\": 5,\n        \"similarity_threshold\": 0.5,\n        \"chunk_size\": 2000,\n        \"chunk_overlap\": 200,\n        \"use_web_fallback\": True,\n        \"web_results\": 3,\n        \"collection\": \"kb\",\n        \"prompt_template\": \"Answer the question based on the following context. \\nIf you don't know the answer, just say you don't know; don't make up information.\\n\\nContext:\\n{context}\\n\\nQuestion: {question}\\n\"\n    }", default_config_patch)
        
        # Write the updated content back to the file
        with open("learning_agent.py", "w") as f:
            f.write(content)
        
        rprint("[green]✅ Successfully patched learning_agent.py with improved error handling[/green]")
        return True
    
    except Exception as e:
        rprint(f"[red]❌ Error patching learning_agent.py: {e}[/red]")
        import traceback
        rprint(traceback.format_exc())
        return False


def update_config():
    """Update config.yaml to include retrieval_timeout setting."""
    try:
        config_path = "config.yaml"
        
        # Create default config if it doesn't exist
        if not os.path.exists(config_path):
            default_config = {
                "model": "qwen3:4b",
                "model_provider": "ollama",
                "temperature": 0.3,
                "use_memory": True,
                "embedding_model": "BAAI/bge-small-en-v1.5",
                "top_k": 5,
                "similarity_threshold": 0.5,
                "use_web_fallback": True,
                "web_results": 3,
                "collection": "kb",
                "retrieval_timeout": 30,  # Add timeout setting
            }
            
            with open(config_path, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            rprint(f"[green]✅ Created new config.yaml with retrieval_timeout setting[/green]")
            return True
        
        # Update existing config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
        
        # Add retrieval_timeout if not present
        if "retrieval_timeout" not in config:
            config["retrieval_timeout"] = 30  # Default 30 seconds
            
            # Write updated config
            with open(config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False)
            
            rprint(f"[green]✅ Updated config.yaml with retrieval_timeout setting[/green]")
        else:
            rprint(f"[yellow]⚠️ retrieval_timeout already exists in config.yaml[/yellow]")
        
        return True
    
    except Exception as e:
        rprint(f"[red]❌ Error updating config.yaml: {e}[/red]")
        return False


def update_dependencies():
    """Update dependencies to use the latest LangChain components."""
    try:
        rprint("[cyan]🔄 Checking for langchain-ollama package...[/cyan]")
        
        # Check if langchain-ollama is installed
        try:
            import langchain_ollama
            rprint("[green]✅ langchain-ollama is already installed[/green]")
        except ImportError:
            rprint("[yellow]⚠️ langchain-ollama not found, installing...[/yellow]")
            
            # Install langchain-ollama
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "langchain-ollama"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                rprint("[green]✅ Successfully installed langchain-ollama[/green]")
            else:
                rprint(f"[red]❌ Failed to install langchain-ollama: {result.stderr}[/red]")
                rprint("[yellow]⚠️ Please manually run: pip install -U langchain-ollama[/yellow]")
        
        # Update import in learning_agent.py
        with open("learning_agent.py", "r") as f:
            content = f.read()
        
        if "from langchain_community.chat_models import ChatOllama" in content:
            content = content.replace(
                "from langchain_community.chat_models import ChatOllama",
                "# Updated import for ChatOllama\nfrom langchain_ollama import ChatOllama"
            )
            
            # Write the updated content back to the file
            with open("learning_agent.py", "w") as f:
                f.write(content)
            
            rprint("[green]✅ Updated ChatOllama import in learning_agent.py[/green]")
        else:
            rprint("[yellow]⚠️ ChatOllama import not found or already updated[/yellow]")
        
        return True
    
    except Exception as e:
        rprint(f"[red]❌ Error updating dependencies: {e}[/red]")
        return False


def main():
    """Main function."""
    rprint(Panel.fit(
        "[bold cyan]LearningAgent Retrieval Fix[/bold cyan]\n\n"
        "This script will fix retrieval issues in the LearningAgent by:\n"
        "1. Adding timeout handling for Ollama connections\n"
        "2. Improving error handling in the retrieval service\n"
        "3. Implementing a more robust fallback chain\n"
        "4. Updating dependencies to use the latest LangChain components",
        title="🛠️ Fix Retrieval",
        border_style="cyan"
    ))
    
    # Patch learning_agent.py
    if patch_learning_agent():
        rprint("[green]✓[/green] Successfully patched learning_agent.py")
    else:
        rprint("[red]✗[/red] Failed to patch learning_agent.py")
    
    # Update config.yaml
    if update_config():
        rprint("[green]✓[/green] Successfully updated config.yaml")
    else:
        rprint("[red]✗[/red] Failed to update config.yaml")
    
    # Update dependencies
    if update_dependencies():
        rprint("[green]✓[/green] Successfully updated dependencies")
    else:
        rprint("[red]✗[/red] Failed to update dependencies")
    
    rprint("\n[bold green]✅ Retrieval fix complete![/bold green]")
    rprint("\n[cyan]To test the fix, run:[/cyan]")
    rprint("  python learning_agent.py")
    rprint("\n[cyan]Then try querying about Morava K-theory again.[/cyan]")


if __name__ == "__main__":
    main()