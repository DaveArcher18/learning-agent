"""
Type definitions for the Learning Agent.

Provides comprehensive type hints, protocols, and type aliases to improve type safety
and IDE support across all modules. Follows maintainability, modularity, simplicity,
and observability principles.
"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import (
    Any, Dict, List, Optional, Union, Callable, Protocol, TypeVar, Generic,
    Literal, TypedDict, NamedTuple, Awaitable, Iterator, AsyncIterator,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from datetime import datetime
    import logging

# Python version compatibility
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# =============================================================================
# Core Type Aliases
# =============================================================================

# Basic types
JSON = Dict[str, Any]
ConfigDict = Dict[str, Any]
MetricsDict = Dict[str, Union[int, float, str]]
HeadersDict = Dict[str, str]

# File system
PathLike = Union[str, Path]

# Service responses
ServiceResponse = Dict[str, Any]
HealthStatus = Dict[str, Any]

# Generic type variables
T = TypeVar('T')
R = TypeVar('R')

# =============================================================================
# Enums
# =============================================================================

class LogLevel(Enum):
    """Logging levels for structured logging."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ServiceStatus(Enum):
    """Service health status indicators."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"
    GROQ = "groq"
    OPENROUTER = "openrouter"


class RetrievalMode(Enum):
    """RAG retrieval modes."""
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    KEYWORD = "keyword"
    BGE_M3_MULTI = "bge_m3_multi"
    GRAPHRAG = "graphrag"
    RAPTOR = "raptor"


class DocumentType(Enum):
    """Supported document types for processing."""
    PDF = "pdf"
    MARKDOWN = "markdown"
    TEXT = "text"
    DOCX = "docx"
    HTML = "html"
    LATEX = "latex"


class CommandStatus(Enum):
    """Command execution status."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    CANCELLED = "cancelled"


# =============================================================================
# Configuration Types
# =============================================================================

class RAGFlowConfigDict(TypedDict):
    """Type definition for RAGFlow configuration dictionary."""
    host: str
    port: int
    docker_service: str
    knowledge_base: str
    enable_citations: bool
    enable_layout_parsing: bool


class BGE_M3ConfigDict(TypedDict):
    """Type definition for BGE-M3 configuration dictionary."""
    model_name: str
    device: str
    max_length: int
    batch_size: int
    dense_dim: int
    enable_sparse: bool
    enable_colbert: bool
    cache_embeddings: bool


class MathematicalContentConfigDict(TypedDict):
    """Type definition for mathematical content configuration dictionary."""
    chunk_size: int
    chunk_overlap_ratio: float
    preserve_latex: bool
    theorem_classification: bool
    proof_chain_tracking: bool
    citation_granularity: Literal["sentence", "paragraph", "document"]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass(frozen=True)
class Citation:
    """Represents a source citation with metadata."""
    text: str
    source: str
    page: Optional[int] = None
    line: Optional[int] = None
    confidence: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class RetrievalResult:
    """Result from RAG retrieval with metadata."""
    content: str
    score: float
    source: str
    citations: List[Citation]
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class LLMResponse:
    """Response from LLM service with metadata."""
    content: str
    provider: LLMProvider
    model: str
    tokens_used: int
    response_time: float
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class CommandResult:
    """Result of command execution."""
    status: CommandStatus
    message: str
    data: Optional[Any] = None
    error: Optional[Exception] = None
    execution_time: float = 0.0


@dataclass
class HealthCheckResult:
    """Result of a health check operation."""
    service: str
    status: ServiceStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    response_time: float = 0.0


@dataclass
class MetricsSnapshot:
    """Snapshot of system metrics at a point in time."""
    timestamp: datetime
    service_metrics: Dict[str, Any]
    system_metrics: Dict[str, Any]
    custom_metrics: Dict[str, Any]


# =============================================================================
# Protocols (Interfaces)
# =============================================================================

class Configurable(Protocol):
    """Protocol for objects that can be configured."""
    
    def configure(self, config: ConfigDict) -> None:
        """Configure the object with provided configuration."""
        ...


class HealthCheckable(Protocol):
    """Protocol for objects that can perform health checks."""
    
    async def health_check(self) -> HealthCheckResult:
        """Perform a health check and return the result."""
        ...


class MetricsCollectable(Protocol):
    """Protocol for objects that can collect metrics."""
    
    def collect_metrics(self) -> MetricsDict:
        """Collect and return current metrics."""
        ...


class Retrievable(Protocol):
    """Protocol for retrieval services."""
    
    async def retrieve(
        self, 
        query: str, 
        top_k: int = 10,
        mode: RetrievalMode = RetrievalMode.SEMANTIC
    ) -> List[RetrievalResult]:
        """Retrieve relevant documents for the given query."""
        ...


class LLMProvider_Protocol(Protocol):
    """Protocol for LLM service providers."""
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Generate response using the LLM."""
        ...
    
    async def health_check(self) -> bool:
        """Check if the provider is healthy."""
        ...


class CommandExecutor(Protocol):
    """Protocol for command execution."""
    
    async def execute(
        self, 
        command: str, 
        args: Optional[List[str]] = None
    ) -> CommandResult:
        """Execute a command with optional arguments."""
        ...


class DocumentProcessor(Protocol):
    """Protocol for document processing services."""
    
    async def process_document(
        self,
        content: str,
        doc_type: DocumentType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[RetrievalResult]:
        """Process a document and return processed chunks."""
        ...


class MemoryManager(Protocol):
    """Protocol for memory management services."""
    
    def store_conversation(
        self,
        session_id: str,
        user_message: str,
        assistant_response: str
    ) -> None:
        """Store a conversation turn."""
        ...
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Retrieve conversation history."""
        ...


# =============================================================================
# Abstract Base Classes
# =============================================================================

class BaseService(ABC):
    """Abstract base class for all services."""
    
    def __init__(self, name: str, config: ConfigDict) -> None:
        """Initialize the service with name and configuration."""
        self.name = name
        self.config = config
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the service."""
        ...
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the service gracefully."""
        ...
    
    @abstractmethod
    async def health_check(self) -> HealthCheckResult:
        """Perform health check."""
        ...
    
    @property
    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        return self._initialized


class BaseCommand(ABC):
    """Abstract base class for all commands."""
    
    def __init__(self, name: str, description: str) -> None:
        """Initialize command with name and description."""
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, args: List[str]) -> CommandResult:
        """Execute the command with provided arguments."""
        ...
    
    @abstractmethod
    def get_help(self) -> str:
        """Get help text for the command."""
        ...


class BaseRetriever(ABC):
    """Abstract base class for retrieval services."""
    
    def __init__(self, name: str, config: ConfigDict) -> None:
        """Initialize retriever with name and configuration."""
        self.name = name
        self.config = config
    
    @abstractmethod
    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievalResult]:
        """Retrieve relevant documents."""
        ...
    
    @abstractmethod
    async def index_document(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Index a document for retrieval."""
        ...


# =============================================================================
# Callback and Handler Types
# =============================================================================

# Event handlers
EventHandler = Callable[[str, Dict[str, Any]], None]
ErrorHandler = Callable[[Exception], None]
MetricsHandler = Callable[[MetricsSnapshot], None]

# Progress callbacks
ProgressCallback = Callable[[int, int, str], None]  # current, total, message

# Validation functions
ValidationFunction = Callable[[Any], bool]
TransformFunction = Callable[[T], R]

# =============================================================================
# Union Types for Common Patterns
# =============================================================================

# Configuration value types
ConfigValue = Union[str, int, float, bool, List[Any], Dict[str, Any]]

# Response types
APIResponse = Union[Dict[str, Any], str, bytes]

# Query types
QueryInput = Union[str, Dict[str, Any]]

# Result types
ProcessingResult = Union[RetrievalResult, LLMResponse, CommandResult]

# =============================================================================
# Type Guards
# =============================================================================

def is_health_check_result(obj: Any) -> bool:
    """Type guard for HealthCheckResult."""
    return (
        hasattr(obj, 'service') and
        hasattr(obj, 'status') and
        hasattr(obj, 'message')
    )


def is_retrieval_result(obj: Any) -> bool:
    """Type guard for RetrievalResult."""
    return (
        hasattr(obj, 'content') and
        hasattr(obj, 'score') and
        hasattr(obj, 'source')
    )


def is_llm_response(obj: Any) -> bool:
    """Type guard for LLMResponse."""
    return (
        hasattr(obj, 'content') and
        hasattr(obj, 'provider') and
        hasattr(obj, 'model')
    )


# =============================================================================
# Generic Classes
# =============================================================================

class ServiceRegistry(Generic[T]):
    """Generic service registry for managing services of a specific type."""
    
    def __init__(self) -> None:
        """Initialize empty service registry."""
        self._services: Dict[str, T] = {}
    
    def register(self, name: str, service: T) -> None:
        """Register a service with the given name."""
        self._services[name] = service
    
    def get(self, name: str) -> Optional[T]:
        """Get a service by name."""
        return self._services.get(name)
    
    def list_services(self) -> List[str]:
        """List all registered service names."""
        return list(self._services.keys())
    
    def unregister(self, name: str) -> bool:
        """Unregister a service by name."""
        if name in self._services:
            del self._services[name]
            return True
        return False


class EventEmitter(Generic[T]):
    """Generic event emitter for type-safe event handling."""
    
    def __init__(self) -> None:
        """Initialize event emitter."""
        self._handlers: Dict[str, List[Callable[[T], None]]] = {}
    
    def on(self, event: str, handler: Callable[[T], None]) -> None:
        """Register an event handler."""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)
    
    def emit(self, event: str, data: T) -> None:
        """Emit an event with data."""
        if event in self._handlers:
            for handler in self._handlers[event]:
                try:
                    handler(data)
                except Exception:
                    # Log error but continue with other handlers
                    pass
    
    def off(self, event: str, handler: Callable[[T], None]) -> bool:
        """Remove an event handler."""
        if event in self._handlers and handler in self._handlers[event]:
            self._handlers[event].remove(handler)
            return True
        return False 