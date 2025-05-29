"""
Command registry for managing and executing commands.

This module provides the central registry for all commands,
handling registration, lookup, and execution.
"""

from typing import Dict, List, TYPE_CHECKING, Optional
from rich import print as rprint

from .base import Command
from .system import ExitCommand, HelpCommand, ConfigCommand
from .provider import ProviderCommand
from .memory import MemoryCommand
from .rag import RAGCommand, SearchCommand
from .knowledge import KnowledgeCommand
from .metrics import MetricsCommand
from .academic import AcademicAnalyzeCommand
from ...observability.logger import get_logger

if TYPE_CHECKING:
    from ...core.agent import LearningAgent

logger = get_logger(__name__)


class CommandRegistry:
    """
    Central registry for all commands.
    
    Manages command registration, lookup, and execution with
    support for aliases and help generation.
    """
    
    def __init__(self):
        """Initialize the command registry."""
        self.commands: Dict[str, Command] = {}
        self.aliases: Dict[str, str] = {}
        logger.info("Command registry initialized")
    
    def register(self, command: Command, aliases: Optional[List[str]] = None) -> None:
        """
        Register a command with optional aliases.
        
        Args:
            command: Command instance to register
            aliases: Optional list of command aliases
        """
        command_name = command.name
        self.commands[command_name] = command
        
        # Register aliases
        if aliases:
            for alias in aliases:
                self.aliases[alias] = command_name
        
        logger.info(f"Registered command: {command_name} with aliases: {aliases or []}")
    
    def register_all_commands(self) -> None:
        """Register all available commands."""
        # System commands
        self.register(ExitCommand(), aliases=["quit", "q"])
        self.register(HelpCommand(), aliases=["h", "?"])
        self.register(ConfigCommand(), aliases=["cfg"])
        
        # Provider commands
        self.register(ProviderCommand(), aliases=["prov"])
        
        # Memory commands
        self.register(MemoryCommand(), aliases=["mem"])
        
        # RAG commands
        self.register(RAGCommand(), aliases=["retrieval"])
        self.register(SearchCommand(), aliases=["find"])
        
        # Knowledge commands
        self.register(KnowledgeCommand(), aliases=["kb", "knowledge"])
        
        # Metrics commands
        self.register(MetricsCommand(), aliases=["stats", "performance", "monitor"])
        
        # Academic commands (Week 7)
        self.register(AcademicAnalyzeCommand(), aliases=["paper", "analyze"])
        
        logger.info(f"Registered {len(self.commands)} commands with {len(self.aliases)} aliases")
    
    def get_command(self, name: str) -> Optional[Command]:
        """
        Get a command by name or alias.
        
        Args:
            name: Command name or alias
            
        Returns:
            Optional[Command]: Command instance if found, None otherwise
        """
        # Check direct command name
        if name in self.commands:
            return self.commands[name]
        
        # Check aliases
        if name in self.aliases:
            return self.commands[self.aliases[name]]
        
        return None
    
    def execute(self, cmd: str, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute a command by name.
        
        Args:
            cmd: Command name or alias
            args: Command arguments
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution, False to exit
        """
        command = self.get_command(cmd.lower())
        
        if command is None:
            rprint(f"[yellow]⚠️ Unknown command: {cmd}[/yellow]")
            rprint("[blue]💡 Use ':help' to see available commands[/blue]")
            return True
        
        try:
            return command.execute(args, agent)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            rprint(f"[red]❌ Command failed: {e}[/red]")
            return True  # Continue execution despite error
    
    def get_all_commands(self) -> Dict[str, Command]:
        """
        Get all registered commands.
        
        Returns:
            Dict[str, Command]: Dictionary of command name to command instance
        """
        return self.commands.copy()
    
    def get_command_help(self, cmd: str) -> Optional[str]:
        """
        Get help text for a specific command.
        
        Args:
            cmd: Command name or alias
            
        Returns:
            Optional[str]: Help text if command exists, None otherwise
        """
        command = self.get_command(cmd.lower())
        return command.get_help() if command else None
    
    def list_commands(self) -> List[str]:
        """
        Get a list of all command names.
        
        Returns:
            List[str]: List of command names
        """
        return list(self.commands.keys())
    
    def list_aliases(self) -> Dict[str, str]:
        """
        Get a dictionary of all aliases.
        
        Returns:
            Dict[str, str]: Dictionary of alias to command name
        """
        return self.aliases.copy() 