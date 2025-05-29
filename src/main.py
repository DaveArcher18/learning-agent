"""
Main entry point for the Learning Agent.

This module provides the main entry point with startup health checks,
graceful shutdown handling, and proper error management.
"""

import sys
import signal
from typing import Optional
from rich import print as rprint
from dotenv import load_dotenv

from .core.agent import LearningAgent
from .core.config import ConfigManager
from .observability.logger import get_logger, setup_logging
from .observability.health import HealthChecker

logger = get_logger(__name__)


def signal_handler(signum: int, frame) -> None:
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down gracefully")
    rprint("\n[yellow]👋 Shutting down gracefully...[/yellow]")
    sys.exit(0)


def perform_startup_checks(config: ConfigManager) -> bool:
    """
    Perform startup health checks for all services.
    
    Args:
        config: Configuration manager instance
        
    Returns:
        bool: True if all checks pass, False otherwise
    """
    logger.info("Performing startup health checks")
    
    try:
        health_checker = HealthChecker(config)
        
        # Get detailed health status for configuration
        config_status = health_checker._check_configuration()
        if not config_status.healthy:
            rprint(f"[red]❌ Configuration check failed: {config_status.error}[/red]")
            rprint(f"[red]Details: {config_status.details}[/red]")
            return False
        else:
            rprint("[green]✅ Configuration check passed[/green]")
        
        # Check LLM service availability
        llm_status = health_checker._check_llm_service()
        if not llm_status.healthy:
            rprint(f"[yellow]⚠️ LLM service check failed: {llm_status.error}[/yellow]")
        else:
            rprint("[green]✅ LLM service check passed[/green]")
        
        # Check RAGFlow service (optional)
        ragflow_status = health_checker._check_ragflow_service()
        if not ragflow_status.healthy:
            rprint(f"[yellow]⚠️ RAGFlow service unavailable: {ragflow_status.error}[/yellow]")
        else:
            rprint("[green]✅ RAGFlow service check passed[/green]")
        
        logger.info("Startup health checks completed")
        return True
        
    except Exception as e:
        logger.error(f"Startup health checks failed: {e}")
        rprint(f"[red]❌ Startup health checks failed: {e}[/red]")
        return False


def main() -> None:
    """Main entrypoint for the learning agent."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Set up logging
        setup_logging()
        logger.info("Starting Learning Agent")
        
        # Load configuration
        config = ConfigManager()
        
        # Perform startup health checks
        if not perform_startup_checks(config):
            rprint("[red]❌ Startup checks failed. Please check your configuration.[/red]")
            sys.exit(1)
        
        # Create and run the agent
        agent = LearningAgent(config)
        agent.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        rprint("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        rprint(f"[red]❌ Fatal error: {e}[/red]")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("Learning Agent shutdown complete")


if __name__ == "__main__":
    main() 