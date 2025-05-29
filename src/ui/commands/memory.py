"""
Memory commands for conversation management.

This module contains commands for managing conversation memory,
including clearing, viewing, and exporting conversation history.
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
    name="memory",
    description="Manage conversation memory",
    aliases=["mem"]
)
class MemoryCommand(Command):
    """Manage conversation memory and history."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the memory command.
        
        Args:
            args: Memory command arguments (clear, show, export, enable, disable)
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            self._show_memory_status(agent)
        else:
            parts = args.strip().split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "clear":
                self._clear_memory(agent)
            elif action == "show":
                self._show_memory_content(agent)
            elif action == "status":
                self._show_memory_status(agent)
            elif action == "export":
                filename = parts[1] if len(parts) > 1 else None
                self._export_memory(agent, filename)
            elif action == "import":
                filename = parts[1] if len(parts) > 1 else None
                self._import_memory(agent, filename)
            elif action == "enable":
                self._enable_memory(agent)
            elif action == "disable":
                self._disable_memory(agent)
            elif action == "stats":
                self._show_memory_stats(agent)
            else:
                rprint(f"[yellow]⚠️ Unknown memory action: {action}[/yellow]")
                self._show_memory_help()
        
        return True
    
    def _show_memory_status(self, agent: 'LearningAgent') -> None:
        """
        Show memory status and basic information.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        
        # Create status table
        table = Table(title="🧠 Memory Status", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        
        # Memory status information
        is_enabled = memory_service.is_enabled()
        message_count = memory_service.get_message_count()
        memory_size = memory_service.get_memory_size()
        max_messages = memory_service.get_max_messages()
        
        table.add_row("Status", "🟢 Enabled" if is_enabled else "🔴 Disabled")
        table.add_row("Messages", f"{message_count}")
        table.add_row("Memory Size", f"{memory_size} characters")
        table.add_row("Max Messages", f"{max_messages}")
        table.add_row("Auto Cleanup", "🟢 Enabled" if memory_service.has_auto_cleanup() else "🔴 Disabled")
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _show_memory_content(self, agent: 'LearningAgent') -> None:
        """
        Show conversation memory content.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        messages = memory_service.get_messages()
        
        if not messages:
            rprint("[yellow]📝 No conversation history available[/yellow]")
            return
        
        rprint(f"\n[bold cyan]📚 Conversation History ({len(messages)} messages)[/bold cyan]\n")
        
        for i, message in enumerate(messages[-10:], 1):  # Show last 10 messages
            role = "User" if message.type == "human" else "Assistant"
            icon = "💬" if message.type == "human" else "🤖"
            content = message.content[:100] + "..." if len(message.content) > 100 else message.content
            
            panel = Panel(
                content,
                title=f"{icon} {role} (Message {len(messages) - 10 + i})",
                border_style="blue" if message.type == "human" else "green",
                expand=False
            )
            rprint(panel)
        
        if len(messages) > 10:
            rprint(f"\n[yellow]💡 Showing last 10 messages. Total: {len(messages)}[/yellow]")
        rprint()
    
    def _show_memory_stats(self, agent: 'LearningAgent') -> None:
        """
        Show detailed memory statistics.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        stats = memory_service.get_statistics()
        
        # Create stats table
        table = Table(title="📊 Memory Statistics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Description", style="yellow")
        
        table.add_row("Total Messages", str(stats.get("total_messages", 0)), "All messages in history")
        table.add_row("User Messages", str(stats.get("user_messages", 0)), "Messages from user")
        table.add_row("AI Messages", str(stats.get("ai_messages", 0)), "Messages from AI")
        table.add_row("Average Length", f"{stats.get('avg_message_length', 0):.0f}", "Average message length")
        table.add_row("Total Characters", str(stats.get("total_characters", 0)), "Total character count")
        table.add_row("Session Duration", f"{stats.get('session_duration', 0):.1f}m", "Current session time")
        table.add_row("Memory Usage", f"{stats.get('memory_usage_percent', 0):.1f}%", "Memory capacity used")
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _clear_memory(self, agent: 'LearningAgent') -> None:
        """
        Clear conversation memory.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        
        # Confirm before clearing
        from ...ui.console_interface import ConsoleInterface
        console = ConsoleInterface()
        
        if console.confirm("Are you sure you want to clear all conversation memory?"):
            memory_service.clear()
            rprint("[green]✅ Conversation memory cleared[/green]")
            logger.info("Conversation memory cleared by user")
        else:
            rprint("[blue]💡 Memory clear cancelled[/blue]")
    
    def _export_memory(self, agent: 'LearningAgent', filename: str = None) -> None:
        """
        Export conversation memory to file.
        
        Args:
            agent: Learning agent instance
            filename: Optional filename for export
        """
        memory_service = agent.get_memory_service()
        
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.json"
        
        try:
            exported_file = memory_service.export_conversation(filename)
            rprint(f"[green]✅ Conversation exported to: {exported_file}[/green]")
            logger.info(f"Conversation exported to: {exported_file}")
        except Exception as e:
            rprint(f"[red]❌ Export failed: {e}[/red]")
            logger.error(f"Memory export failed: {e}")
    
    def _import_memory(self, agent: 'LearningAgent', filename: str = None) -> None:
        """
        Import conversation memory from file.
        
        Args:
            agent: Learning agent instance
            filename: Filename to import from
        """
        if not filename:
            rprint("[yellow]⚠️ Please specify a filename to import[/yellow]")
            rprint("[blue]💡 Usage: :memory import filename.json[/blue]")
            return
        
        memory_service = agent.get_memory_service()
        
        try:
            message_count = memory_service.import_conversation(filename)
            rprint(f"[green]✅ Imported {message_count} messages from: {filename}[/green]")
            logger.info(f"Conversation imported from: {filename}")
        except Exception as e:
            rprint(f"[red]❌ Import failed: {e}[/red]")
            logger.error(f"Memory import failed: {e}")
    
    def _enable_memory(self, agent: 'LearningAgent') -> None:
        """
        Enable conversation memory.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        memory_service.set_enabled(True)
        rprint("[green]✅ Conversation memory enabled[/green]")
        logger.info("Conversation memory enabled")
    
    def _disable_memory(self, agent: 'LearningAgent') -> None:
        """
        Disable conversation memory.
        
        Args:
            agent: Learning agent instance
        """
        memory_service = agent.get_memory_service()
        memory_service.set_enabled(False)
        rprint("[yellow]⚠️ Conversation memory disabled[/yellow]")
        logger.info("Conversation memory disabled")
    
    def _show_memory_help(self) -> None:
        """Show memory command help."""
        help_panel = Panel(
            "[bold]Memory Command Usage:[/bold]\n\n"
            "• [cyan]:memory[/cyan] - Show memory status\n"
            "• [cyan]:memory show[/cyan] - Show conversation history\n"
            "• [cyan]:memory clear[/cyan] - Clear all memory\n"
            "• [cyan]:memory stats[/cyan] - Show detailed statistics\n"
            "• [cyan]:memory export [file][/cyan] - Export conversation\n"
            "• [cyan]:memory import <file>[/cyan] - Import conversation\n"
            "• [cyan]:memory enable[/cyan] - Enable memory\n"
            "• [cyan]:memory disable[/cyan] - Disable memory",
            title="❓ Memory Help",
            border_style="yellow"
        )
        rprint(help_panel) 