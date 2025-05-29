"""
Provider commands for LLM provider management.

This module contains commands for switching between different
LLM providers and managing provider-specific settings.
"""

from typing import TYPE_CHECKING, List, Dict, Any
from rich import print as rprint
from rich.table import Table
from rich.panel import Panel

from .base import Command, command_decorator
from ...observability.logger import get_logger

if TYPE_CHECKING:
    from ...core.agent import LearningAgent

logger = get_logger(__name__)


@command_decorator(
    name="provider",
    description="Switch LLM provider or show provider status",
    aliases=["prov"]
)
class ProviderCommand(Command):
    """Switch LLM provider or show provider status."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the provider command.
        
        Args:
            args: Provider arguments (provider_name, status, list)
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            self._show_provider_status(agent)
        else:
            parts = args.strip().split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "status":
                self._show_provider_status(agent)
            elif action == "list":
                self._list_providers(agent)
            elif action == "test":
                provider_name = parts[1] if len(parts) > 1 else None
                self._test_provider(provider_name, agent)
            elif action in self._get_supported_providers():
                self._switch_provider(action, agent)
            else:
                rprint(f"[yellow]⚠️ Unknown provider or action: {action}[/yellow]")
                self._show_provider_help()
        
        return True
    
    def _show_provider_status(self, agent: 'LearningAgent') -> None:
        """
        Show current provider status.
        
        Args:
            agent: Learning agent instance
        """
        llm_service = agent.get_llm_service()
        config = agent.get_config()
        
        # Create status table
        table = Table(title="🔧 LLM Provider Status", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Status", style="green")
        
        # Current provider info
        current_provider = config.get("model_provider", "unknown")
        current_model = config.get("model", "unknown")
        temperature = config.get("temperature", 0.3)
        
        # Check provider health
        provider_status = "🟢 Healthy" if llm_service.is_healthy() else "🔴 Unhealthy"
        
        table.add_row("Current Provider", current_provider, provider_status)
        table.add_row("Current Model", current_model, "")
        table.add_row("Temperature", str(temperature), "")
        table.add_row("Response Time", f"{llm_service.get_avg_response_time():.2f}s", "")
        table.add_row("Total Requests", str(llm_service.get_request_count()), "")
        table.add_row("Error Rate", f"{llm_service.get_error_rate():.1%}", "")
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _list_providers(self, agent: 'LearningAgent') -> None:
        """
        List all supported providers.
        
        Args:
            agent: Learning agent instance
        """
        providers = self._get_provider_info()
        
        # Create providers table
        table = Table(title="🌐 Supported LLM Providers", show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Requirements", style="yellow")
        table.add_column("Models", style="green")
        
        for provider, info in providers.items():
            table.add_row(
                provider,
                info["description"],
                info["requirements"],
                info["models"]
            )
        
        rprint("\n")
        rprint(table)
        
        # Show usage examples
        usage_panel = Panel(
            "[bold]Usage Examples:[/bold]\n\n"
            "• Switch to OpenAI: [cyan]:provider openai[/cyan]\n"
            "• Switch to DeepSeek: [cyan]:provider deepseek[/cyan]\n"
            "• Switch to Ollama: [cyan]:provider ollama[/cyan]\n"
            "• Test provider: [cyan]:provider test openai[/cyan]\n"
            "• Show status: [cyan]:provider status[/cyan]",
            title="💡 Provider Commands",
            border_style="blue"
        )
        rprint(usage_panel)
        rprint()
    
    def _switch_provider(self, provider_name: str, agent: 'LearningAgent') -> None:
        """
        Switch to a different LLM provider.
        
        Args:
            provider_name: Name of the provider to switch to
            agent: Learning agent instance
        """
        llm_service = agent.get_llm_service()
        config = agent.get_config()
        
        try:
            rprint(f"[cyan]🔄 Switching to {provider_name}...[/cyan]")
            
            # Update configuration
            config.set("model_provider", provider_name)
            
            # Set default model for provider
            default_models = self._get_default_models()
            if provider_name in default_models:
                config.set("model", default_models[provider_name])
            
            # Reinitialize LLM service
            llm_service.switch_provider(provider_name)
            
            # Test the new provider
            if llm_service.is_healthy():
                rprint(f"[green]✅ Successfully switched to {provider_name}[/green]")
                logger.info(f"Provider switched to: {provider_name}")
            else:
                rprint(f"[yellow]⚠️ Switched to {provider_name} but health check failed[/yellow]")
                logger.warning(f"Provider {provider_name} health check failed after switch")
            
        except Exception as e:
            rprint(f"[red]❌ Failed to switch to {provider_name}: {e}[/red]")
            logger.error(f"Provider switch failed: {e}")
    
    def _test_provider(self, provider_name: str, agent: 'LearningAgent') -> None:
        """
        Test a specific provider.
        
        Args:
            provider_name: Name of the provider to test
            agent: Learning agent instance
        """
        if not provider_name:
            provider_name = agent.get_config().get("model_provider", "current")
        
        llm_service = agent.get_llm_service()
        
        rprint(f"[cyan]🧪 Testing {provider_name} provider...[/cyan]")
        
        try:
            # Perform health check
            is_healthy = llm_service.test_provider(provider_name)
            
            if is_healthy:
                rprint(f"[green]✅ {provider_name} provider is working correctly[/green]")
            else:
                rprint(f"[red]❌ {provider_name} provider test failed[/red]")
                
        except Exception as e:
            rprint(f"[red]❌ Provider test error: {e}[/red]")
            logger.error(f"Provider test failed: {e}")
    
    def _show_provider_help(self) -> None:
        """Show provider command help."""
        help_panel = Panel(
            "[bold]Provider Command Usage:[/bold]\n\n"
            "• [cyan]:provider[/cyan] - Show current provider status\n"
            "• [cyan]:provider list[/cyan] - List all supported providers\n"
            "• [cyan]:provider <name>[/cyan] - Switch to provider\n"
            "• [cyan]:provider test [name][/cyan] - Test provider\n"
            "• [cyan]:provider status[/cyan] - Show detailed status\n\n"
            "[bold]Supported Providers:[/bold]\n"
            "• openai, deepseek, anthropic, ollama, groq",
            title="❓ Provider Help",
            border_style="yellow"
        )
        rprint(help_panel)
    
    def _get_supported_providers(self) -> List[str]:
        """Get list of supported provider names."""
        return ["openai", "deepseek", "anthropic", "ollama", "groq"]
    
    def _get_default_models(self) -> Dict[str, str]:
        """Get default models for each provider."""
        return {
            "openai": "gpt-4o-mini",
            "deepseek": "deepseek-chat",
            "anthropic": "claude-3-haiku-20240307",
            "ollama": "qwen2.5:7b",
            "groq": "llama-3.1-8b-instant"
        }
    
    def _get_provider_info(self) -> Dict[str, Dict[str, str]]:
        """Get detailed information about each provider."""
        return {
            "openai": {
                "description": "OpenAI GPT models",
                "requirements": "OPENAI_API_KEY",
                "models": "gpt-4o, gpt-4o-mini, gpt-3.5-turbo"
            },
            "deepseek": {
                "description": "DeepSeek reasoning models",
                "requirements": "DEEPSEEK_API_KEY",
                "models": "deepseek-chat, deepseek-coder"
            },
            "anthropic": {
                "description": "Anthropic Claude models",
                "requirements": "ANTHROPIC_API_KEY",
                "models": "claude-3-opus, claude-3-sonnet, claude-3-haiku"
            },
            "ollama": {
                "description": "Local Ollama models",
                "requirements": "Ollama service running",
                "models": "qwen2.5, llama3.1, mistral, codellama"
            },
            "groq": {
                "description": "Groq fast inference",
                "requirements": "GROQ_API_KEY",
                "models": "llama-3.1-8b, mixtral-8x7b, gemma-7b"
            }
        } 