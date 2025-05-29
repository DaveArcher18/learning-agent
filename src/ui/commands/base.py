"""
Base command infrastructure.

This module provides the abstract base classes and decorators for
implementing the command system with proper registration and middleware.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any, Optional, Callable
from functools import wraps

from ...observability.logger import get_logger

if TYPE_CHECKING:
    from ...core.agent import LearningAgent

logger = get_logger(__name__)


class Command(ABC):
    """
    Abstract base class for all commands.
    
    Commands are responsible for handling specific user actions
    and interacting with the agent's services.
    """
    
    def __init__(self):
        """Initialize the command."""
        self.name = self.__class__.__name__.lower().replace('command', '')
        self.description = self.__doc__ or "No description available"
    
    @abstractmethod
    def execute(self, args: str, agent: 'LearningAgent') -> bool:
        """
        Execute the command.
        
        Args:
            args: Command arguments as a string
            agent: The learning agent instance
            
        Returns:
            bool: True to continue execution, False to exit
        """
        pass
    
    def get_help(self) -> str:
        """
        Get help text for this command.
        
        Returns:
            str: Help text for the command
        """
        return f"{self.name}: {self.description}"
    
    def validate_args(self, args: str) -> bool:
        """
        Validate command arguments.
        
        Args:
            args: Command arguments to validate
            
        Returns:
            bool: True if arguments are valid, False otherwise
        """
        return True  # Default implementation accepts all arguments


class CommandMiddleware:
    """
    Middleware for command execution.
    
    Provides logging, timing, and error handling for commands.
    """
    
    @staticmethod
    def log_execution(func: Callable) -> Callable:
        """
        Decorator to log command execution.
        
        Args:
            func: Command execution function
            
        Returns:
            Callable: Wrapped function with logging
        """
        @wraps(func)
        def wrapper(self, args: str, agent: 'LearningAgent') -> bool:
            command_name = self.__class__.__name__
            logger.info(f"Executing command: {command_name} with args: {args}")
            
            try:
                result = func(self, args, agent)
                logger.info(f"Command {command_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"Command {command_name} failed: {e}")
                raise
        
        return wrapper
    
    @staticmethod
    def validate_agent(func: Callable) -> Callable:
        """
        Decorator to validate agent instance.
        
        Args:
            func: Command execution function
            
        Returns:
            Callable: Wrapped function with agent validation
        """
        @wraps(func)
        def wrapper(self, args: str, agent: 'LearningAgent') -> bool:
            if agent is None:
                logger.error("Agent instance is None")
                raise ValueError("Agent instance is required")
            
            return func(self, args, agent)
        
        return wrapper
    
    @staticmethod
    def handle_errors(func: Callable) -> Callable:
        """
        Decorator to handle command errors gracefully.
        
        Args:
            func: Command execution function
            
        Returns:
            Callable: Wrapped function with error handling
        """
        @wraps(func)
        def wrapper(self, args: str, agent: 'LearningAgent') -> bool:
            try:
                return func(self, args, agent)
            except KeyboardInterrupt:
                logger.info("Command interrupted by user")
                return True  # Continue execution
            except Exception as e:
                logger.error(f"Command error: {e}")
                from rich import print as rprint
                rprint(f"[red]❌ Command failed: {e}[/red]")
                return True  # Continue execution despite error
        
        return wrapper


def command_decorator(name: Optional[str] = None, 
                     description: Optional[str] = None,
                     aliases: Optional[list] = None):
    """
    Decorator for registering commands.
    
    Args:
        name: Command name (defaults to class name)
        description: Command description
        aliases: List of command aliases
        
    Returns:
        Callable: Decorator function
    """
    def decorator(cls):
        # Store metadata on the class
        cls._command_name = name or cls.__name__.lower().replace('command', '')
        cls._command_description = description or cls.__doc__ or "No description available"
        cls._command_aliases = aliases or []
        
        # Apply middleware decorators to execute method
        if hasattr(cls, 'execute'):
            cls.execute = CommandMiddleware.handle_errors(
                CommandMiddleware.validate_agent(
                    CommandMiddleware.log_execution(cls.execute)
                )
            )
        
        return cls
    
    return decorator


class CommandResult:
    """
    Result of command execution.
    
    Provides structured information about command execution results.
    """
    
    def __init__(self, 
                 success: bool, 
                 continue_execution: bool = True,
                 message: Optional[str] = None,
                 data: Optional[Dict[str, Any]] = None):
        """
        Initialize command result.
        
        Args:
            success: Whether the command executed successfully
            continue_execution: Whether to continue agent execution
            message: Optional result message
            data: Optional result data
        """
        self.success = success
        self.continue_execution = continue_execution
        self.message = message
        self.data = data or {}
    
    def __bool__(self) -> bool:
        """Return continue_execution for backward compatibility."""
        return self.continue_execution 