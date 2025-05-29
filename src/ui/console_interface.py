"""
Console interface for user interaction.

This module provides a clean interface for console-based user interaction,
including input handling, startup messages, and status displays.
"""

from typing import Optional
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

from ..observability.logger import get_logger

logger = get_logger(__name__)


class ConsoleInterface:
    """
    Manages console-based user interaction.
    
    Provides methods for displaying messages, getting user input,
    and managing the console interface state.
    """
    
    def __init__(self):
        """Initialize the console interface."""
        self.console = Console()
        logger.info("Console interface initialized")
    
    def show_startup_message(self) -> None:
        """Display the startup message and instructions."""
        rprint("\n[bold green]✨ Initializing LearningAgent...[/bold green]")
        rprint("\n[bold cyan]💬 LearningAgent ready! Type a question or use ':help' for commands.[/bold cyan]\n")
        logger.info("Startup message displayed")
    
    def get_user_input(self) -> str:
        """
        Get user input with proper handling of empty input.
        
        Returns:
            str: User input, stripped of whitespace
        """
        try:
            user_input = input("> ").strip()
            if user_input:
                logger.debug(f"User input received: {user_input[:50]}...")
            return user_input
        except (KeyboardInterrupt, EOFError):
            logger.info("User initiated exit via keyboard interrupt")
            raise
    
    def show_thinking(self) -> None:
        """Display thinking indicator."""
        rprint("[cyan]🔍 Thinking...[/cyan]")
    
    def show_error(self, message: str) -> None:
        """
        Display an error message.
        
        Args:
            message: Error message to display
        """
        rprint(f"[red]❌ {message}[/red]")
        logger.error(f"Error displayed to user: {message}")
    
    def show_warning(self, message: str) -> None:
        """
        Display a warning message.
        
        Args:
            message: Warning message to display
        """
        rprint(f"[yellow]⚠️ {message}[/yellow]")
        logger.warning(f"Warning displayed to user: {message}")
    
    def show_success(self, message: str) -> None:
        """
        Display a success message.
        
        Args:
            message: Success message to display
        """
        rprint(f"[green]✅ {message}[/green]")
        logger.info(f"Success message displayed: {message}")
    
    def show_info(self, message: str) -> None:
        """
        Display an info message.
        
        Args:
            message: Info message to display
        """
        rprint(f"[blue]ℹ️ {message}[/blue]")
        logger.info(f"Info message displayed: {message}")
    
    def show_panel(self, content: str, title: str = "", style: str = "blue") -> None:
        """
        Display content in a panel.
        
        Args:
            content: Content to display
            title: Panel title
            style: Panel style/color
        """
        panel = Panel(content, title=title, expand=False, border_style=style)
        self.console.print(panel)
        logger.debug(f"Panel displayed with title: {title}")
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        self.console.clear()
        logger.debug("Console screen cleared")
    
    def print_separator(self, char: str = "-", length: int = 50) -> None:
        """
        Print a separator line.
        
        Args:
            char: Character to use for separator
            length: Length of separator
        """
        rprint(char * length)
    
    def confirm(self, message: str) -> bool:
        """
        Ask for user confirmation.
        
        Args:
            message: Confirmation message
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        try:
            response = input(f"{message} (y/N): ").strip().lower()
            confirmed = response in ['y', 'yes']
            logger.debug(f"User confirmation: {confirmed}")
            return confirmed
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled confirmation")
            return False 