"""
Structured logging configuration for the Learning Agent.

This module provides structured logging with JSON format, correlation IDs,
and performance timing for comprehensive observability.
"""

import logging
import json
import time
import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from contextlib import contextmanager
from functools import wraps

# Global correlation ID for request tracking
_correlation_id: Optional[str] = None


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Formats log records as JSON with consistent structure including
    correlation IDs, timestamps, and performance metrics.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            str: JSON formatted log entry
        """
        # Create base log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, 'correlation_id', _correlation_id),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add custom fields from extra
        for key, value in record.__dict__.items():
            if key not in {
                'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                'filename', 'module', 'lineno', 'funcName', 'created',
                'msecs', 'relativeCreated', 'thread', 'threadName',
                'processName', 'process', 'exc_info', 'exc_text', 'stack_info',
                'getMessage', 'correlation_id'
            } and not key.startswith('_'):
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Set up structured logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = StructuredFormatter()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


@contextmanager
def correlation_context(correlation_id: Optional[str] = None):
    """
    Context manager for correlation ID tracking.
    
    Args:
        correlation_id: Optional correlation ID, generates one if not provided
        
    Yields:
        str: The correlation ID for this context
    """
    global _correlation_id
    
    old_correlation_id = _correlation_id
    
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    _correlation_id = correlation_id
    
    try:
        yield correlation_id
    finally:
        _correlation_id = old_correlation_id


def with_correlation_id(correlation_id: Optional[str] = None):
    """
    Decorator to add correlation ID to function execution.
    
    Args:
        correlation_id: Optional correlation ID
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with correlation_context(correlation_id):
                return func(*args, **kwargs)
        return wrapper
    return decorator


class PerformanceLogger:
    """
    Logger for performance metrics and timing.
    
    Provides methods for timing operations and logging performance data.
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize performance logger.
        
        Args:
            logger: Base logger instance
        """
        self.logger = logger
    
    @contextmanager
    def timer(self, operation: str, **context):
        """
        Context manager for timing operations.
        
        Args:
            operation: Name of the operation being timed
            **context: Additional context to log
            
        Yields:
            Dict[str, Any]: Timer context with timing information
        """
        start_time = time.time()
        timer_context = {"operation": operation, "start_time": start_time}
        timer_context.update(context)
        
        self.logger.info(
            f"Starting {operation}",
            extra={
                "event_type": "operation_start",
                "operation": operation,
                **context
            }
        )
        
        try:
            yield timer_context
            
            duration = time.time() - start_time
            self.logger.info(
                f"Completed {operation}",
                extra={
                    "event_type": "operation_complete",
                    "operation": operation,
                    "duration_seconds": duration,
                    "status": "success",
                    **context
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                f"Failed {operation}",
                extra={
                    "event_type": "operation_failed",
                    "operation": operation,
                    "duration_seconds": duration,
                    "status": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    **context
                },
                exc_info=True
            )
            raise
    
    def log_metrics(self, metrics: Dict[str, Any], category: str = "metrics"):
        """
        Log performance metrics.
        
        Args:
            metrics: Dictionary of metrics to log
            category: Category for the metrics
        """
        self.logger.info(
            f"Performance metrics: {category}",
            extra={
                "event_type": "metrics",
                "category": category,
                **metrics
            }
        )


class EventLogger:
    """
    Logger for specific event types with structured data.
    
    Provides methods for logging different types of events with
    consistent structure and categorization.
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize event logger.
        
        Args:
            logger: Base logger instance
        """
        self.logger = logger
    
    def agent_startup(self, config: Dict[str, Any]):
        """Log agent startup event."""
        self.logger.info(
            "Agent startup",
            extra={
                "event_type": "agent.startup",
                "config": config
            }
        )
    
    def agent_query(self, query: str, query_type: str = "user"):
        """Log agent query event."""
        self.logger.info(
            "Agent query received",
            extra={
                "event_type": "agent.query",
                "query_length": len(query),
                "query_type": query_type,
                "query_preview": query[:100] if len(query) > 100 else query
            }
        )
    
    def agent_response(self, response: str, response_time: float):
        """Log agent response event."""
        self.logger.info(
            "Agent response generated",
            extra={
                "event_type": "agent.response",
                "response_length": len(response),
                "response_time_seconds": response_time
            }
        )
    
    def llm_switch(self, old_provider: str, new_provider: str):
        """Log LLM provider switch event."""
        self.logger.info(
            "LLM provider switched",
            extra={
                "event_type": "llm.switch",
                "old_provider": old_provider,
                "new_provider": new_provider
            }
        )
    
    def llm_request(self, provider: str, model: str, tokens: int):
        """Log LLM request event."""
        self.logger.debug(
            "LLM request sent",
            extra={
                "event_type": "llm.request",
                "provider": provider,
                "model": model,
                "token_count": tokens
            }
        )
    
    def llm_error(self, provider: str, error: str, error_type: str):
        """Log LLM error event."""
        self.logger.error(
            "LLM request failed",
            extra={
                "event_type": "llm.error",
                "provider": provider,
                "error_type": error_type,
                "error_message": error
            }
        )
    
    def ragflow_startup(self, status: str, config: Dict[str, Any]):
        """Log RAGFlow startup event."""
        self.logger.info(
            "RAGFlow startup",
            extra={
                "event_type": "ragflow.startup",
                "status": status,
                "config": config
            }
        )
    
    def ragflow_query(self, query: str, top_k: int, mode: str):
        """Log RAGFlow query event."""
        self.logger.info(
            "RAGFlow query",
            extra={
                "event_type": "ragflow.query",
                "query_length": len(query),
                "top_k": top_k,
                "mode": mode
            }
        )
    
    def ragflow_health(self, status: str, details: Dict[str, Any]):
        """Log RAGFlow health check event."""
        self.logger.info(
            "RAGFlow health check",
            extra={
                "event_type": "ragflow.health",
                "status": status,
                **details
            }
        )
    
    def rag_retrieval(self, query: str, results_count: int, response_time: float):
        """Log RAG retrieval event."""
        self.logger.info(
            "RAG retrieval completed",
            extra={
                "event_type": "rag.retrieval",
                "query_length": len(query),
                "results_count": results_count,
                "response_time_seconds": response_time
            }
        )
    
    def rag_reranking(self, initial_count: int, final_count: int, improvement: float):
        """Log RAG reranking event."""
        self.logger.info(
            "RAG reranking completed",
            extra={
                "event_type": "rag.reranking",
                "initial_count": initial_count,
                "final_count": final_count,
                "improvement_score": improvement
            }
        )
    
    def rag_citations(self, citations_count: int, accuracy_score: float):
        """Log RAG citations event."""
        self.logger.info(
            "RAG citations generated",
            extra={
                "event_type": "rag.citations",
                "citations_count": citations_count,
                "accuracy_score": accuracy_score
            }
        )
    
    def knowledge_upload(self, file_path: str, kb_name: str, file_size: int):
        """Log knowledge base document upload event."""
        self.logger.info(
            "Document uploaded to knowledge base",
            extra={
                "event_type": "knowledge.upload",
                "file_path": file_path,
                "knowledge_base": kb_name,
                "file_size_bytes": file_size
            }
        )
    
    def knowledge_processing(self, doc_id: str, chunks_created: int, processing_time: float):
        """Log knowledge base document processing event."""
        self.logger.info(
            "Document processing completed",
            extra={
                "event_type": "knowledge.processing",
                "document_id": doc_id,
                "chunks_created": chunks_created,
                "processing_time_seconds": processing_time
            }
        )
    
    def memory_operation(self, operation: str, message_count: int, memory_size: int):
        """Log memory operation event."""
        self.logger.info(
            f"Memory {operation}",
            extra={
                "event_type": "memory.operation",
                "operation": operation,
                "message_count": message_count,
                "memory_size_bytes": memory_size
            }
        )
    
    def command_execution(self, command: str, args: str, success: bool, duration: float):
        """Log command execution event."""
        self.logger.info(
            f"Command executed: {command}",
            extra={
                "event_type": "command.execution",
                "command": command,
                "args": args,
                "success": success,
                "duration_seconds": duration
            }
        ) 