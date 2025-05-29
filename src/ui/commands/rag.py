"""
RAG commands for retrieval and search operations.

This module contains commands for RAG operations including
search, retrieval configuration, and knowledge base queries.
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
    name="rag",
    description="Manage RAG retrieval settings and operations",
    aliases=["retrieval"]
)
class RAGCommand(Command):
    """Manage RAG retrieval settings and operations."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the RAG command.
        
        Args:
            args: RAG command arguments (status, config, test, reindex)
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            self._show_rag_status(agent)
        else:
            parts = args.strip().split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "status":
                self._show_rag_status(agent)
            elif action == "config":
                self._show_rag_config(agent)
            elif action == "test":
                query = parts[1] if len(parts) > 1 else "test query"
                self._test_retrieval(agent, query)
            elif action == "reindex":
                self._reindex_knowledge(agent)
            elif action == "stats":
                self._show_rag_stats(agent)
            elif action == "health":
                self._check_rag_health(agent)
            else:
                rprint(f"[yellow]⚠️ Unknown RAG action: {action}[/yellow]")
                self._show_rag_help()
        
        return True
    
    def _show_rag_status(self, agent: 'LearningAgent') -> None:
        """
        Show RAG system status.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        config = agent.get_config()
        
        # Create status table
        table = Table(title="🔍 RAG System Status", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Status", style="white")
        table.add_column("Details", style="yellow")
        
        # RAGFlow service status
        ragflow_status = "🟢 Available" if ragflow_service.is_available() else "🔴 Unavailable"
        ragflow_details = f"Docker: {ragflow_service.get_docker_status()}"
        
        table.add_row("RAGFlow Service", ragflow_status, ragflow_details)
        
        # BGE-M3 model status
        bge_status = "🟢 Loaded" if ragflow_service.is_model_loaded("bge-m3") else "🔴 Not Loaded"
        bge_details = f"Model: {config.get('embedding_model', 'bge-m3')}"
        
        table.add_row("BGE-M3 Model", bge_status, bge_details)
        
        # Knowledge base status
        kb_count = ragflow_service.get_knowledge_base_count()
        kb_status = f"🟢 {kb_count} bases" if kb_count > 0 else "🔴 No bases"
        kb_details = f"Documents: {ragflow_service.get_document_count()}"
        
        table.add_row("Knowledge Bases", kb_status, kb_details)
        
        # Retrieval configuration
        retrieval_mode = config.get("retrieval_mode", "hybrid")
        retrieval_status = "🟢 Configured"
        retrieval_details = f"Mode: {retrieval_mode}, Top-K: {config.get('top_k', 10)}"
        
        table.add_row("Retrieval Config", retrieval_status, retrieval_details)
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _show_rag_config(self, agent: 'LearningAgent') -> None:
        """
        Show RAG configuration settings.
        
        Args:
            agent: Learning agent instance
        """
        config = agent.get_config()
        
        # Create config table
        table = Table(title="⚙️ RAG Configuration", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Description", style="yellow")
        
        # RAG configuration items
        rag_config_items = [
            ("use_ragflow", "Enable RAGFlow integration"),
            ("embedding_model", "Embedding model name"),
            ("retrieval_mode", "Retrieval strategy"),
            ("top_k", "Number of documents to retrieve"),
            ("chunk_size", "Document chunk size"),
            ("chunk_overlap", "Chunk overlap percentage"),
            ("rerank_top_k", "Reranking top-K"),
            ("enable_citations", "Automatic citation extraction"),
            ("mathematical_content", "Mathematical content optimization"),
        ]
        
        for key, description in rag_config_items:
            value = config.get(key, "Not set")
            table.add_row(key, str(value), description)
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _show_rag_stats(self, agent: 'LearningAgent') -> None:
        """
        Show RAG performance statistics.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        stats = ragflow_service.get_retrieval_stats()
        
        # Create stats table
        table = Table(title="📊 RAG Performance Statistics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Description", style="yellow")
        
        table.add_row("Total Queries", str(stats.get("total_queries", 0)), "Total retrieval queries")
        table.add_row("Avg Response Time", f"{stats.get('avg_response_time', 0):.2f}s", "Average retrieval time")
        table.add_row("Cache Hit Rate", f"{stats.get('cache_hit_rate', 0):.1%}", "Embedding cache hits")
        table.add_row("Documents Retrieved", str(stats.get("total_documents", 0)), "Total documents retrieved")
        table.add_row("Citations Generated", str(stats.get("citations_generated", 0)), "Automatic citations")
        table.add_row("Math Content Hits", str(stats.get("math_content_hits", 0)), "Mathematical content matches")
        table.add_row("Reranking Success", f"{stats.get('reranking_success_rate', 0):.1%}", "Reranking effectiveness")
        
        rprint("\n")
        rprint(table)
        rprint()
    
    def _test_retrieval(self, agent: 'LearningAgent', query: str) -> None:
        """
        Test retrieval with a query.
        
        Args:
            agent: Learning agent instance
            query: Test query
        """
        ragflow_service = agent.get_ragflow_service()
        
        rprint(f"[cyan]🧪 Testing retrieval with query: '{query}'[/cyan]")
        
        try:
            # Perform test retrieval
            results = ragflow_service.test_retrieval(query)
            
            if results:
                rprint(f"[green]✅ Retrieved {len(results)} documents[/green]")
                
                # Show top results
                for i, result in enumerate(results[:3], 1):
                    score = result.get("score", 0)
                    content = result.get("content", "")[:200] + "..."
                    source = result.get("source", "Unknown")
                    
                    panel = Panel(
                        f"[bold]Score:[/bold] {score:.3f}\n"
                        f"[bold]Source:[/bold] {source}\n"
                        f"[bold]Content:[/bold] {content}",
                        title=f"📄 Result {i}",
                        border_style="green",
                        expand=False
                    )
                    rprint(panel)
            else:
                rprint("[yellow]⚠️ No documents retrieved[/yellow]")
                
        except Exception as e:
            rprint(f"[red]❌ Retrieval test failed: {e}[/red]")
            logger.error(f"Retrieval test failed: {e}")
    
    def _reindex_knowledge(self, agent: 'LearningAgent') -> None:
        """
        Reindex knowledge base.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        
        # Confirm before reindexing
        from ...ui.console_interface import ConsoleInterface
        console = ConsoleInterface()
        
        if console.confirm("Are you sure you want to reindex the knowledge base? This may take time."):
            rprint("[cyan]🔄 Starting knowledge base reindexing...[/cyan]")
            
            try:
                ragflow_service.reindex_knowledge_base()
                rprint("[green]✅ Knowledge base reindexing completed[/green]")
                logger.info("Knowledge base reindexing completed")
            except Exception as e:
                rprint(f"[red]❌ Reindexing failed: {e}[/red]")
                logger.error(f"Knowledge base reindexing failed: {e}")
        else:
            rprint("[blue]💡 Reindexing cancelled[/blue]")
    
    def _check_rag_health(self, agent: 'LearningAgent') -> None:
        """
        Check RAG system health.
        
        Args:
            agent: Learning agent instance
        """
        ragflow_service = agent.get_ragflow_service()
        
        rprint("[cyan]🏥 Checking RAG system health...[/cyan]")
        
        health_checks = [
            ("RAGFlow Service", ragflow_service.is_available()),
            ("Docker Container", ragflow_service.is_docker_healthy()),
            ("BGE-M3 Model", ragflow_service.is_model_loaded("bge-m3")),
            ("Knowledge Base", ragflow_service.get_knowledge_base_count() > 0),
            ("Embedding Cache", ragflow_service.is_cache_healthy()),
        ]
        
        # Create health table
        table = Table(title="🏥 RAG Health Check", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Status", style="white")
        
        all_healthy = True
        for component, is_healthy in health_checks:
            status = "🟢 Healthy" if is_healthy else "🔴 Unhealthy"
            if not is_healthy:
                all_healthy = False
            table.add_row(component, status)
        
        rprint("\n")
        rprint(table)
        
        if all_healthy:
            rprint("\n[green]✅ All RAG components are healthy[/green]")
        else:
            rprint("\n[yellow]⚠️ Some RAG components need attention[/yellow]")
        rprint()
    
    def _show_rag_help(self) -> None:
        """Show RAG command help."""
        help_panel = Panel(
            "[bold]RAG Command Usage:[/bold]\n\n"
            "• [cyan]:rag[/cyan] - Show RAG system status\n"
            "• [cyan]:rag config[/cyan] - Show RAG configuration\n"
            "• [cyan]:rag test <query>[/cyan] - Test retrieval\n"
            "• [cyan]:rag stats[/cyan] - Show performance statistics\n"
            "• [cyan]:rag health[/cyan] - Check system health\n"
            "• [cyan]:rag reindex[/cyan] - Reindex knowledge base",
            title="❓ RAG Help",
            border_style="yellow"
        )
        rprint(help_panel)


@command_decorator(
    name="search",
    description="Search knowledge base with advanced options",
    aliases=["find"]
)
class SearchCommand(Command):
    """Search knowledge base with advanced options."""
    
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the search command.
        
        Args:
            args: Search query and options
            agent: Learning agent instance
            
        Returns:
            bool: True to continue execution
        """
        if not args.strip():
            rprint("[yellow]⚠️ Please provide a search query[/yellow]")
            rprint("[blue]💡 Usage: :search <query> [--top-k N] [--mode hybrid|semantic|keyword][/blue]")
            return True
        
        # Parse search arguments
        query, options = self._parse_search_args(args)
        
        # Perform search
        self._perform_search(agent, query, options)
        
        return True
    
    def _parse_search_args(self, args: str) -> tuple:
        """
        Parse search arguments and options.
        
        Args:
            args: Raw search arguments
            
        Returns:
            tuple: (query, options_dict)
        """
        parts = args.split()
        query_parts = []
        options = {}
        
        i = 0
        while i < len(parts):
            if parts[i].startswith('--'):
                option = parts[i][2:]
                if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                    options[option] = parts[i + 1]
                    i += 2
                else:
                    options[option] = True
                    i += 1
            else:
                query_parts.append(parts[i])
                i += 1
        
        query = ' '.join(query_parts)
        return query, options
    
    def _perform_search(self, agent: 'LearningAgent', query: str, options: Dict[str, Any]) -> None:
        """
        Perform the search operation.
        
        Args:
            agent: Learning agent instance
            query: Search query
            options: Search options
        """
        ragflow_service = agent.get_ragflow_service()
        
        # Set search parameters
        top_k = int(options.get('top-k', 10))
        mode = options.get('mode', 'hybrid')
        
        rprint(f"[cyan]🔍 Searching for: '{query}' (mode: {mode}, top-k: {top_k})[/cyan]")
        
        try:
            # Perform search
            results = ragflow_service.search_knowledge_base(
                query=query,
                top_k=top_k,
                mode=mode
            )
            
            if results:
                rprint(f"\n[green]✅ Found {len(results)} results[/green]\n")
                
                # Display results
                for i, result in enumerate(results, 1):
                    score = result.get("score", 0)
                    content = result.get("content", "")
                    source = result.get("source", "Unknown")
                    citations = result.get("citations", [])
                    
                    # Truncate content for display
                    display_content = content[:300] + "..." if len(content) > 300 else content
                    
                    # Format citations
                    citation_text = ""
                    if citations:
                        citation_text = f"\n[bold]Citations:[/bold] {', '.join(citations)}"
                    
                    panel = Panel(
                        f"[bold]Score:[/bold] {score:.3f}\n"
                        f"[bold]Source:[/bold] {source}\n"
                        f"[bold]Content:[/bold] {display_content}"
                        f"{citation_text}",
                        title=f"📄 Result {i}",
                        border_style="blue",
                        expand=False
                    )
                    rprint(panel)
                    
                    # Ask if user wants to see more results
                    if i >= 5 and i < len(results):
                        from ...ui.console_interface import ConsoleInterface
                        console = ConsoleInterface()
                        if not console.confirm(f"Show more results? ({len(results) - i} remaining)"):
                            break
            else:
                rprint("[yellow]⚠️ No results found[/yellow]")
                rprint("[blue]💡 Try different keywords or check if documents are indexed[/blue]")
                
        except Exception as e:
            rprint(f"[red]❌ Search failed: {e}[/red]")
            logger.error(f"Search failed: {e}") 