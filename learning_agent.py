#!/usr/bin/env python3
"""
Learning Agent - Simple RAG Assistant with Memory

A streamlined entry point that uses config.yaml as the single source of truth
for all configuration settings.
"""

import sys
import signal
from pathlib import Path
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.config import get_config_manager
from src.core.agent import LearningAgent

console = Console()

def signal_handler(signum: int, frame) -> None:
    """Handle shutdown signals gracefully."""
    rprint("\n[yellow]👋 Shutting down gracefully...[/yellow]")
    sys.exit(0)

def check_requirements(config_manager) -> bool:
    """Check if basic requirements are met."""
    
    # Validate configuration  
    if not config_manager.validate_config():
        return False
    
    # Check if API key is available for the configured provider
    provider = config_manager.config.llm.model_provider.value
    
    if provider != 'ollama':  # Ollama doesn't need API key
        provider_config = getattr(config_manager.config.llm.providers, provider, None)
        if not provider_config or not provider_config.api_key:
            rprint(f"[yellow]⚠️ No API key found for {provider}[/yellow]")
            rprint(f"[blue]💡 Add {provider.upper()}_API_KEY to your .env file[/blue]")
            return False
    
    return True

def main() -> None:
    """Main entry point for the Learning Agent."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Display startup banner
        console.print(Panel.fit(
            "[bold blue]Learning Agent[/bold blue]\n"
            "[dim]Simple RAG Assistant with Memory[/dim]\n\n"
            "[green]Configuration:[/green] config.yaml\n"
            "[green]Environment:[/green] .env",
            border_style="blue"
        ))
        
        # Load and validate configuration
        config_manager = get_config_manager()
        
        if not check_requirements(config_manager):
            rprint("\n[red]❌ Setup incomplete. Please check your configuration.[/red]")
            sys.exit(1)
        
        # Display configuration summary
        provider = config_manager.config.llm.model_provider.value
        model = config_manager.config.llm.model
        memory = config_manager.config.use_memory
        
        rprint(f"\n[green]✅ Ready![/green]")
        rprint(f"[dim]Provider:[/dim] {provider}")
        rprint(f"[dim]Model:[/dim] {model}")
        rprint(f"[dim]Memory:[/dim] {'enabled' if memory else 'disabled'}")
        rprint(f"[dim]Document chunking:[/dim] {config_manager.get('documents.chunk_size', 4000)} tokens with {config_manager.get('documents.chunk_overlap', 500)} overlap")
        rprint()
        
        # Create and run the agent
        agent = LearningAgent(config_manager)
        agent.run()
        
    except KeyboardInterrupt:
        rprint("\n[yellow]👋 Goodbye![/yellow]")
    except FileNotFoundError as e:
        rprint(f"[red]❌ Configuration error: {e}[/red]")
        rprint("[blue]💡 Make sure config.yaml exists in the project root[/blue]")
        sys.exit(1)
    except Exception as e:
        rprint(f"[red]❌ Fatal error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 