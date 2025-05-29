"""
Core agent orchestration module.

This module contains the streamlined LearningAgent class that coordinates
all services and components with dependency injection for maintainability.
"""

import sys
from typing import Optional, Dict, Any, List
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console

from ..services.llm_service import LLMService
from ..services.ragflow_service import RAGFlowService
from ..services.memory_service import MemoryService
from ..services.document_service import DocumentService, DocumentChunk
from ..text_processing.markdown_renderer import MarkdownRenderer, MarkdownRenderingConfig
from ..ui.console_interface import ConsoleInterface
from ..ui.commands.registry import CommandRegistry
from ..observability.logger import get_logger
from .config import ConfigManager

logger = get_logger(__name__)


class LearningAgent:
    """
    Streamlined Learning Agent that orchestrates all services.
    
    This class focuses purely on coordination and dependency injection,
    delegating all specific functionality to specialized services.
    Implements universal retrieval - all queries trigger document retrieval.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the Learning Agent with dependency injection.
        
        Args:
            config: Configuration manager instance
        """
        logger.info("Initializing LearningAgent")
        
        # Store configuration
        self.config = config
        
        # Initialize core services with dependency injection
        self._initialize_services()
        
        # Initialize UI components
        self._initialize_ui()
        
        # Register commands
        self._register_commands()
        
        logger.info("LearningAgent initialization complete")
    
    def _initialize_services(self) -> None:
        """Initialize all core services with error handling."""
        try:
            # Initialize Document service first
            self.document_service = DocumentService(self.config)
            logger.info("Document service initialized successfully")
            
            # Initialize LLM service
            self.llm_service = LLMService(self.config)
            logger.info("LLM service initialized successfully")
            
            # Initialize RAGFlow service (optional)
            try:
                self.ragflow_service = RAGFlowService(self.config)
                logger.info("RAGFlow service initialized successfully")
            except Exception as e:
                logger.warning(f"RAGFlow service unavailable: {e}")
                self.ragflow_service = None
            
            # Initialize memory service
            self.memory_service = MemoryService(self.config)
            logger.info("Memory service initialized successfully")
            
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
            rprint(f"[red]❌ Service initialization failed: {e}[/red]")
            raise
    
    def _initialize_ui(self) -> None:
        """Initialize UI components."""
        try:
            self.console_interface = ConsoleInterface()
            
            # Create MarkdownRenderingConfig from ConfigManager
            ui_config = self.config.config.ui
            markdown_config = MarkdownRenderingConfig(
                enable_latex_processing=ui_config.enable_latex_processing,
                enable_rich_panels=ui_config.use_markdown_rendering,
                enable_syntax_highlighting=ui_config.code_highlighting,
                academic_formatting=ui_config.use_advanced_latex_rendering
            )
            
            self.markdown_renderer = MarkdownRenderer(markdown_config)
            logger.info("UI components initialized successfully")
            
        except Exception as e:
            logger.error(f"UI initialization failed: {e}")
            rprint(f"[red]❌ UI initialization failed: {e}[/red]")
            raise
    
    def _register_commands(self) -> None:
        """Register all available commands."""
        try:
            self.command_registry = CommandRegistry()
            self.command_registry.register_all_commands()
            logger.info("Commands registered successfully")
            
        except Exception as e:
            logger.error(f"Command registration failed: {e}")
            rprint(f"[red]❌ Command registration failed: {e}[/red]")
            raise
    
    def run(self) -> None:
        """Main chat loop."""
        rprint("[dim]Type ':help' for commands or ':exit' to quit[/dim]\n")
        
        while True:
            try:
                # Get user input
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands (starting with ':')
                if user_input.startswith(':'):
                    cmd_parts = user_input[1:].split(maxsplit=1)
                    cmd = cmd_parts[0].lower()
                    args = cmd_parts[1] if len(cmd_parts) > 1 else ""
                    
                    # Process command
                    if not self.process_command(cmd, args):
                        break  # Exit requested
                    continue
                
                # Generate response to user input
                response = self.generate_response(user_input)
                
                # Render response with markdown support
                if self.config.config.ui.use_markdown_rendering:
                    self.markdown_renderer.render_response(response)
                else:
                    rprint(response)
                
                rprint()  # Empty line for readability
                
            except KeyboardInterrupt:
                rprint("\n[yellow]Use ':exit' to quit gracefully[/yellow]")
            except EOFError:
                break
            except Exception as e:
                logger.error(f"Chat loop error: {e}")
                rprint(f"[red]❌ Unexpected error: {e}[/red]")
    
    def process_command(self, cmd: str, args: str) -> bool:
        """
        Process command inputs starting with ':'.
        
        Args:
            cmd: Command name
            args: Command arguments
            
        Returns:
            bool: True to continue, False to exit
        """
        logger.info(f"Processing command: {cmd} with args: {args}")
        
        try:
            return self.command_registry.execute(cmd, args, self)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            rprint(f"[red]❌ Command execution failed: {e}[/red]")
            return True  # Continue on command errors
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input using universal retrieval.
        ALL queries trigger document retrieval - no content detection.
        
        Args:
            user_input: User's input message
            
        Returns:
            str: Generated response
        """
        logger.info(f"Generating response for input: {user_input[:100]}...")
        
        try:
            # Add user message to memory
            if self.config.config.use_memory:
                self.memory_service.add_user_message(user_input)
                messages = self.memory_service.get_messages()
            else:
                messages = []
            
            # UNIVERSAL RETRIEVAL: Always attempt to retrieve relevant context
            relevant_context = self._retrieve_relevant_context(user_input)
            
            # Try RAGFlow first if available
            if self.ragflow_service and self.ragflow_service.is_available():
                try:
                    response = self.ragflow_service.retrieve_and_answer(
                        user_input, messages
                    )
                    if self.config.config.use_memory:
                        self.memory_service.add_ai_message(response)
                    logger.info("Response generated using RAGFlow")
                    return response
                    
                except Exception as e:
                    logger.warning(f"RAGFlow retrieval failed, using document retrieval: {e}")
            
            # Fallback to document service + LLM
            context = self._build_context(relevant_context, messages)
            
            llm_response = self.llm_service.generate_response(
                user_input, 
                context=context
            )
            response = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
            
            if self.config.config.use_memory:
                self.memory_service.add_ai_message(response)
            
            logger.info("Response generated using document retrieval + LLM")
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            error_msg = self._format_error_message(e)
            return error_msg
    
    def _retrieve_relevant_context(self, query: str) -> List[DocumentChunk]:
        """
        Retrieve relevant document chunks for the query.
        
        Args:
            query: User's query
            
        Returns:
            List of relevant DocumentChunk objects
        """
        try:
            relevant_chunks = self.document_service.search_chunks(
                query, 
                max_chunks=self.config.config.rag.final_k
            )
            
            if relevant_chunks:
                logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks")
                for chunk in relevant_chunks:
                    logger.debug(f"Retrieved chunk from {chunk.source_file} ({chunk.chunk_index}/{chunk.total_chunks})")
            else:
                logger.info("No relevant chunks found for query")
            
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return []
    
    def _build_context(self, chunks: List[DocumentChunk], messages: List[Dict[str, Any]]) -> str:
        """
        Build context string from document chunks and conversation history.
        
        Args:
            chunks: Retrieved document chunks
            messages: Conversation history
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Add document context if available
        if chunks:
            context_parts.append("=== RETRIEVED DOCUMENTS ===")
            for chunk in chunks:
                context_parts.append(f"\n--- From {chunk.source_file} (chunk {chunk.chunk_index + 1}/{chunk.total_chunks}) ---")
                context_parts.append(chunk.content)
                context_parts.append("")  # Empty line for separation
        
        # Add conversation history if available
        if messages:
            context_parts.append("=== CONVERSATION HISTORY ===")
            for msg in messages[-3:]:  # Use last 3 messages for context
                role = "User" if msg.get('role') == 'user' else "Assistant"
                content = msg.get('content', '')
                context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts) if context_parts else None
    
    def _format_error_message(self, error: Exception) -> str:
        """
        Format error messages with helpful troubleshooting information.
        
        Args:
            error: The exception that occurred
            
        Returns:
            str: Formatted error message with troubleshooting steps
        """
        error_str = str(error)
        
        if "Connection refused" in error_str or "Max retries exceeded" in error_str:
            return (
                "I couldn't connect to the language model service. "
                "\n\nTroubleshooting steps:\n"
                "1. Check if your LLM service is running\n"
                "2. Verify your API keys in the .env file\n"
                "3. Try switching providers with ':provider' command\n"
                "4. Use ':help' for more assistance"
            )
        elif "API key" in error_str:
            return (
                "There was an issue with the API key. "
                "\n\nTroubleshooting steps:\n"
                "1. Check your .env file for correct API keys\n"
                "2. Verify your API key permissions\n"
                "3. Try switching to a different provider with ':provider'"
            )
        else:
            return (
                f"I encountered an error: {error_str}\n\n"
                "Try using ':help' to see available commands or ':provider' to switch providers."
            )
    
    # Service accessors for commands
    def get_llm_service(self) -> LLMService:
        """Get LLM service instance."""
        return self.llm_service
    
    def get_ragflow_service(self) -> Optional[RAGFlowService]:
        """Get RAGFlow service instance."""
        return self.ragflow_service
    
    def get_memory_service(self) -> MemoryService:
        """Get memory service instance."""
        return self.memory_service
    
    def get_config(self) -> ConfigManager:
        """Get configuration instance."""
        return self.config 