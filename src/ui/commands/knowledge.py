"""
Knowledge commands for knowledge base management.

This module contains commands for managing knowledge bases,
document upload, and content organization.
"""

from typing import TYPE_CHECKING, List, Dict, Any
from rich import print as rprint
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TaskID

from .base import Command, command_decorator
from ...observability.logger import get_logger

if TYPE_CHECKING:
    from ...core.agent import LearningAgent

logger = get_logger(__name__)


@command_decorator(
    name="knowledge",
    description="Manage knowledge bases and documents",
    aliases=["kb"]
)
class KnowledgeCommand(Command):
    """Manage knowledge bases and documents."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the knowledge command.
        
        Args:
            args: Knowledge command arguments
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            self._show_knowledge_status(agent)
        else:
            parts = args.strip().split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "list":
                self._list_knowledge_bases(agent)
            elif action == "create":
                name = parts[1] if len(parts) > 1 else None
                self._create_knowledge_base(agent, name)
            elif action == "delete":
                name = parts[1] if len(parts) > 1 else None
                self._delete_knowledge_base(agent, name)
            elif action == "upload":
                file_path = parts[1] if len(parts) > 1 else None
                self._upload_document(agent, file_path)
            elif action == "status":
                self._show_knowledge_status(agent)
            elif action == "docs":
                kb_name = parts[1] if len(parts) > 1 else None
                self._list_documents(agent, kb_name)
            elif action == "stats":
                self._show_knowledge_stats(agent)
            else:
                rprint(f"[yellow]⚠️ Unknown knowledge action: {action}[/yellow]")
                self._show_knowledge_help()
        
        return True
    
    def _show_knowledge_status(self, agent: 'LearningAgent') -> None:
        """
        Show knowledge base status overview.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        
        # Create status table
        table = Table(title="📚 Knowledge Base Status", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Details", style="yellow")
        
        # Get knowledge base statistics
        kb_count = ragflow_service.get_knowledge_base_count()
        doc_count = ragflow_service.get_document_count()
        total_size = ragflow_service.get_total_storage_size()
        indexed_docs = ragflow_service.get_indexed_document_count()
        
        table.add_row("Knowledge Bases", str(kb_count), "Total bases created")
        table.add_row("Documents", str(doc_count), f"Indexed: {indexed_docs}")
        table.add_row("Storage Used", f"{total_size:.2f} MB", "Total storage consumed")
        table.add_row("BGE-M3 Status", "🟢 Ready" if ragflow_service.is_model_loaded("bge-m3") else "🔴 Not Ready", "Embedding model")
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _list_knowledge_bases(self, agent: 'LearningAgent') -> None:
        """
        List all knowledge bases.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        
        try:
            knowledge_bases = ragflow_service.list_knowledge_bases()
            
            if not knowledge_bases:
                rprint("[yellow]📝 No knowledge bases found[/yellow]")
                rprint("[blue]💡 Create one with: :knowledge create <name>[/blue]")
                return
            
            # Create knowledge bases table
            table = Table(title="📚 Knowledge Bases", show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Documents", style="white")
            table.add_column("Size", style="yellow")
            table.add_column("Created", style="green")
            table.add_column("Status", style="blue")
            
            for kb in knowledge_bases:
                name = kb.get("name", "Unknown")
                doc_count = kb.get("document_count", 0)
                size = kb.get("size_mb", 0)
                created = kb.get("created_date", "Unknown")
                status = "🟢 Active" if kb.get("active", True) else "🔴 Inactive"
                
                table.add_row(
                    name,
                    str(doc_count),
                    f"{size:.1f} MB",
                    created,
                    status
                )
            
            rprint("\n")
            rprint(table)
            rprint()
            
        except Exception as e:
            rprint(f"[red]❌ Failed to list knowledge bases: {e}[/red]")
            logger.error(f"Failed to list knowledge bases: {e}")
    
    def _create_knowledge_base(self, agent: 'LearningAgent', name: str = None) -> None:
        """
        Create a new knowledge base.
        
        Args:
            agent: Learning agent instance
            name: Name for the new knowledge base
        """
        if not name:
            rprint("[yellow]⚠️ Please specify a knowledge base name[/yellow]")
            rprint("[blue]💡 Usage: :knowledge create <name>[/blue]")
            return
        
        ragflow_service = agent.get_ragflow_service()
        
        try:
            rprint(f"[cyan]🔄 Creating knowledge base: {name}[/cyan]")
            
            kb_id = ragflow_service.create_knowledge_base(
                name=name,
                description=f"Knowledge base created via Learning Agent",
                embedding_model="bge-m3"
            )
            
            rprint(f"[green]✅ Knowledge base '{name}' created successfully[/green]")
            rprint(f"[blue]💡 ID: {kb_id}[/blue]")
            logger.info(f"Knowledge base created: {name} (ID: {kb_id})")
            
        except Exception as e:
            rprint(f"[red]❌ Failed to create knowledge base: {e}[/red]")
            logger.error(f"Failed to create knowledge base {name}: {e}")
    
    def _delete_knowledge_base(self, agent: 'LearningAgent', name: str = None) -> None:
        """
        Delete a knowledge base.
        
        Args:
            agent: Learning agent instance
            name: Name of the knowledge base to delete
        """
        if not name:
            rprint("[yellow]⚠️ Please specify a knowledge base name[/yellow]")
            rprint("[blue]💡 Usage: :knowledge delete <name>[/blue]")
            return
        
        ragflow_service = agent.get_ragflow_service()
        
        # Confirm before deletion
        from ...ui.console_interface import ConsoleInterface
        console = ConsoleInterface()
        
        if console.confirm(f"Are you sure you want to delete knowledge base '{name}'? This cannot be undone."):
            try:
                ragflow_service.delete_knowledge_base(name)
                rprint(f"[green]✅ Knowledge base '{name}' deleted successfully[/green]")
                logger.info(f"Knowledge base deleted: {name}")
                
            except Exception as e:
                rprint(f"[red]❌ Failed to delete knowledge base: {e}[/red]")
                logger.error(f"Failed to delete knowledge base {name}: {e}")
        else:
            rprint("[blue]💡 Deletion cancelled[/blue]")
    
    def _upload_document(self, agent: 'LearningAgent', file_path: str = None) -> None:
        """
        Upload a document to a knowledge base.
        
        Args:
            agent: Learning agent instance
            file_path: Path to the document to upload
        """
        if not file_path:
            rprint("[yellow]⚠️ Please specify a file path[/yellow]")
            rprint("[blue]💡 Usage: :knowledge upload <file_path>[/blue]")
            return
        
        ragflow_service = agent.get_ragflow_service()
        
        # Check if file exists
        import os
        if not os.path.exists(file_path):
            rprint(f"[red]❌ File not found: {file_path}[/red]")
            return
        
        # Get available knowledge bases
        try:
            knowledge_bases = ragflow_service.list_knowledge_bases()
            
            if not knowledge_bases:
                rprint("[yellow]⚠️ No knowledge bases available[/yellow]")
                rprint("[blue]💡 Create one first with: :knowledge create <name>[/blue]")
                return
            
            # Show knowledge bases and let user choose
            rprint("\n[cyan]📚 Available Knowledge Bases:[/cyan]")
            for i, kb in enumerate(knowledge_bases, 1):
                rprint(f"  {i}. {kb['name']}")
            
            # Get user choice
            from ...ui.console_interface import ConsoleInterface
            console = ConsoleInterface()
            
            choice = input("\nEnter knowledge base number (or press Enter for first): ").strip()
            kb_index = 0 if not choice else int(choice) - 1
            
            if kb_index < 0 or kb_index >= len(knowledge_bases):
                rprint("[red]❌ Invalid knowledge base selection[/red]")
                return
            
            selected_kb = knowledge_bases[kb_index]
            
            # Upload document with progress
            rprint(f"[cyan]📤 Uploading {os.path.basename(file_path)} to {selected_kb['name']}...[/cyan]")
            
            with Progress() as progress:
                task = progress.add_task("Uploading...", total=100)
                
                def progress_callback(percent):
                    progress.update(task, completed=percent)
                
                doc_id = ragflow_service.upload_document(
                    knowledge_base_id=selected_kb['id'],
                    file_path=file_path,
                    progress_callback=progress_callback
                )
            
            rprint(f"[green]✅ Document uploaded successfully[/green]")
            rprint(f"[blue]💡 Document ID: {doc_id}[/blue]")
            logger.info(f"Document uploaded: {file_path} to {selected_kb['name']}")
            
        except Exception as e:
            rprint(f"[red]❌ Failed to upload document: {e}[/red]")
            logger.error(f"Failed to upload document {file_path}: {e}")
    
    def _list_documents(self, agent: 'LearningAgent', kb_name: str = None) -> None:
        """
        List documents in a knowledge base.
        
        Args:
            agent: Learning agent instance
            kb_name: Name of the knowledge base
        """
        ragflow_service = agent.get_ragflow_service()
        
        try:
            if not kb_name:
                # Show all documents across all knowledge bases
                documents = ragflow_service.list_all_documents()
                title = "📄 All Documents"
            else:
                # Show documents for specific knowledge base
                documents = ragflow_service.list_documents(kb_name)
                title = f"📄 Documents in '{kb_name}'"
            
            if not documents:
                rprint("[yellow]📝 No documents found[/yellow]")
                return
            
            # Create documents table
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan")
            table.add_column("KB", style="yellow") if not kb_name else None
            table.add_column("Type", style="white", no_wrap=True)
            table.add_column("Size", style="green")
            table.add_column("Status", style="blue")
            table.add_column("Uploaded", style="white")
            
            for doc in documents:
                name = doc.get("name", "Unknown")
                kb = doc.get("knowledge_base", "Unknown") if not kb_name else None
                doc_type = doc.get("type", "Unknown")
                size = doc.get("size_kb", 0)
                status = "🟢 Indexed" if doc.get("indexed", False) else "🔄 Processing"
                uploaded = doc.get("upload_date", "Unknown")
                
                row = [name]
                if not kb_name:
                    row.append(kb)
                row.extend([doc_type, f"{size:.1f} KB", status, uploaded])
                
                table.add_row(*row)
            
            rprint("\n")
            rprint(table)
            rprint()
            
        except Exception as e:
            rprint(f"[red]❌ Failed to list documents: {e}[/red]")
            logger.error(f"Failed to list documents for {kb_name}: {e}")
    
    def _show_knowledge_stats(self, agent: 'LearningAgent') -> None:
        """
        Show detailed knowledge base statistics.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        
        try:
            stats = ragflow_service.get_knowledge_stats()
            
            # Create stats table
            table = Table(title="📊 Knowledge Base Statistics", show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")
            table.add_column("Description", style="yellow")
            
            table.add_row("Total Knowledge Bases", str(stats.get("total_kb", 0)), "Created knowledge bases")
            table.add_row("Total Documents", str(stats.get("total_docs", 0)), "Uploaded documents")
            table.add_row("Indexed Documents", str(stats.get("indexed_docs", 0)), "Ready for search")
            table.add_row("Processing Queue", str(stats.get("processing_queue", 0)), "Documents being processed")
            table.add_row("Total Chunks", str(stats.get("total_chunks", 0)), "Document chunks created")
            table.add_row("Storage Used", f"{stats.get('storage_mb', 0):.2f} MB", "Total storage consumed")
            table.add_row("Embeddings Generated", str(stats.get("embeddings_count", 0)), "BGE-M3 embeddings created")
            table.add_row("Average Chunk Size", f"{stats.get('avg_chunk_size', 0)} chars", "Chunk size optimization")
            
            rprint("\n")
            rprint(table)
            rprint()
            
        except Exception as e:
            rprint(f"[red]❌ Failed to get knowledge statistics: {e}[/red]")
            logger.error(f"Failed to get knowledge statistics: {e}")
    
    def _show_knowledge_help(self) -> None:
        """Show knowledge command help."""
        help_panel = Panel(
            "[bold]Knowledge Command Usage:[/bold]\n\n"
            "• [cyan]:knowledge[/cyan] - Show knowledge base status\n"
            "• [cyan]:knowledge list[/cyan] - List all knowledge bases\n"
            "• [cyan]:knowledge create <name>[/cyan] - Create new knowledge base\n"
            "• [cyan]:knowledge delete <name>[/cyan] - Delete knowledge base\n"
            "• [cyan]:knowledge upload <file>[/cyan] - Upload document\n"
            "• [cyan]:knowledge docs [kb_name][/cyan] - List documents\n"
            "• [cyan]:knowledge stats[/cyan] - Show detailed statistics\n\n"
            "[bold]Supported File Types:[/bold]\n"
            "• PDF, DOCX, TXT, MD, HTML, CSV, JSON",
            title="❓ Knowledge Help",
            border_style="yellow"
        )
        rprint(help_panel) 