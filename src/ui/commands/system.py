"""
System commands for basic agent operations.

This module contains commands for system-level operations like
exit, help, and configuration management.
"""

from typing import TYPE_CHECKING
from rich import print as rprint
from rich.table import Table
from rich.panel import Panel

from .base import Command, command_decorator
from ...observability.logger import get_logger

if TYPE_CHECKING:
    from ...core.agent import LearningAgent

logger = get_logger(__name__)


@command_decorator(
    name="exit",
    description="Exit the Learning Agent",
    aliases=["quit", "q"]
)
class ExitCommand(Command):
    """Exit the Learning Agent gracefully."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the exit command.
        
        Args:
            args: Command arguments (unused)
            agent: Learning agent instance
            
        Returns:
            bool: False to exit the application
        """
        rprint("\n[bold yellow]👋 Thank you for using LearningAgent![/bold yellow]")
        rprint("[cyan]💡 Your conversation history has been saved.[/cyan]")
        logger.info("Exit command executed")
        return False  # Signal to exit


@command_decorator(
    name="help",
    description="Show help information",
    aliases=["h", "?"]
)
class HelpCommand(Command):
    """Show help information for commands and usage."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the help command.
        
        Args:
            args: Optional specific command to get help for
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if args.strip():
            # Show help for specific command
            self._show_command_help(args.strip(), agent)
        else:
            # Show general help
            self._show_general_help(agent)
        
        return True
    
    def _show_command_help(self, command_name: str, agent: 'LearningAgent') -> None:
        """
        Show help for a specific command.
        
        Args:
            command_name: Name of the command to show help for
            agent: Learning agent instance
        """
        help_text = agent.command_registry.get_command_help(command_name)
        
        if help_text:
            rprint(f"\n[bold cyan]Help for '{command_name}':[/bold cyan]")
            rprint(f"[white]{help_text}[/white]\n")
        else:
            rprint(f"[yellow]⚠️ No help available for command '{command_name}'[/yellow]")
            rprint("[blue]💡 Use ':help' to see all available commands[/blue]")
    
    def _show_general_help(self, agent: 'LearningAgent') -> None:
        """
        Show general help information.
        
        Args:
            agent: Learning agent instance
        """
        # Create help table
        table = Table(title="🤖 LearningAgent Commands", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Aliases", style="yellow")
        
        # Add commands to table
        commands = agent.command_registry.get_all_commands()
        aliases_map = agent.command_registry.list_aliases()
        
        for cmd_name, command in sorted(commands.items()):
            # Find aliases for this command
            cmd_aliases = [alias for alias, target in aliases_map.items() if target == cmd_name]
            aliases_str = ", ".join(cmd_aliases) if cmd_aliases else "-"
            
            table.add_row(
                f":{cmd_name}",
                command.description,
                aliases_str
            )
        
        rprint("\n")
        rprint(table)
        
        # Show usage examples
        usage_panel = Panel(
            "[bold]Usage Examples:[/bold]\n\n"
            "• Ask a question: [cyan]What is machine learning?[/cyan]\n"
            "• Get help: [cyan]:help[/cyan] or [cyan]:h[/cyan]\n"
            "• Switch provider: [cyan]:provider openai[/cyan]\n"
            "• Clear memory: [cyan]:memory clear[/cyan]\n"
            "• Search knowledge: [cyan]:search quantum computing[/cyan]\n"
            "• Exit: [cyan]:exit[/cyan] or [cyan]:quit[/cyan]",
            title="💡 Quick Start",
            border_style="blue"
        )
        rprint(usage_panel)
        rprint()


@command_decorator(
    name="config",
    description="Show or modify configuration settings",
    aliases=["cfg"]
)
class ConfigCommand(Command):
    """Show or modify configuration settings."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the config command.
        
        Args:
            args: Configuration arguments (show, set key=value, get key)
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            self._show_config(agent)
        else:
            parts = args.strip().split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "show":
                self._show_config(agent)
            elif action == "get" and len(parts) > 1:
                self._get_config_value(parts[1], agent)
            elif action == "set" and len(parts) > 1:
                self._set_config_value(parts[1], agent)
            else:
                rprint("[yellow]⚠️ Invalid config command[/yellow]")
                rprint("[blue]💡 Usage: :config [show|get key|set key=value][/blue]")
        
        return True
    
    def _show_config(self, agent: 'LearningAgent') -> None:
        """
        Show current configuration.
        
        Args:
            agent: Learning agent instance
        """
        config = agent.get_config()
        
        # Create configuration table
        table = Table(title="⚙️ Current Configuration", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Description", style="yellow")
        
        # Key configuration items to display
        config_items = [
            ("model_provider", "LLM provider"),
            ("model", "LLM model name"),
            ("temperature", "Response creativity"),
            ("use_memory", "Conversation memory"),
            ("use_markdown_rendering", "Rich text display"),
            ("enable_latex_processing", "Math expression rendering"),
            ("use_ragflow", "RAGFlow integration"),
            ("collection", "Vector database collection"),
        ]
        
        for key, description in config_items:
            value = config.get(key, "Not set")
            table.add_row(f"{key}", str(value), description)
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _get_config_value(self, key: str, agent: 'LearningAgent') -> None:
        """
        Get a specific configuration value.
        
        Args:
            key: Configuration key
            agent: Learning agent instance
        """
        config = agent.get_config()
        value = config.get(key)
        
        if value is not None:
            rprint(f"[cyan]{key}[/cyan] = [white]{value}[/white]")
        else:
            rprint(f"[yellow]⚠️ Configuration key '{key}' not found[/yellow]")
    
    def _set_config_value(self, key_value: str, agent: 'LearningAgent') -> None:
        """
        Set a configuration value.
        
        Args:
            key_value: Key=value string
            agent: Learning agent instance
        """
        if "=" not in key_value:
            rprint("[yellow]⚠️ Invalid format. Use: key=value[/yellow]")
            return
        
        key, value = key_value.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        # Convert string values to appropriate types
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)
        elif value.replace(".", "").isdigit():
            value = float(value)
        
        config = agent.get_config()
        config.set(key, value)
        
        rprint(f"[green]✅ Set {key} = {value}[/green]")
        logger.info(f"Configuration updated: {key} = {value}") 