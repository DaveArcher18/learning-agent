"""
Command system package.

This package contains all command classes and the command registry
for the Learning Agent's user interface.
"""

from .base import Command, CommandMiddleware, command_decorator, CommandResult
from .registry import CommandRegistry
from .system import ExitCommand, HelpCommand, ConfigCommand
from .provider import ProviderCommand
from .memory import MemoryCommand
from .rag import RAGCommand, SearchCommand
from .knowledge import KnowledgeCommand

__all__ = [
    "Command",
    "CommandMiddleware", 
    "command_decorator",
    "CommandResult",
    "CommandRegistry",
    "ExitCommand",
    "HelpCommand", 
    "ConfigCommand",
    "ProviderCommand",
    "MemoryCommand",
    "RAGCommand",
    "SearchCommand",
    "KnowledgeCommand",
]
