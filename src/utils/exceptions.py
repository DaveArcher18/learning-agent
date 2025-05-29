"""
Custom exception classes for the Learning Agent.

Provides a comprehensive exception hierarchy with error context, recovery suggestions,
and error aggregation capabilities. Follows maintainability, modularity, simplicity,
and observability principles.
"""

from __future__ import annotations

import sys
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Type
from dataclasses import dataclass, field
from enum import Enum

# Import our types for consistency
from ..core.types import ServiceStatus, LLMProvider


# =============================================================================
# Error Categories and Severity
# =============================================================================

class ErrorSeverity(Enum):
    """Error severity levels for prioritization and handling."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification and handling."""
    CONFIGURATION = "configuration"
    AUTHENTICATION = "authentication"
    NETWORK = "network"
    SERVICE = "service"
    VALIDATION = "validation"
    PROCESSING = "processing"
    RESOURCE = "resource"
    USER_INPUT = "user_input"
    INTERNAL = "internal"


# =============================================================================
# Error Context and Recovery Information
# =============================================================================

@dataclass
class ErrorContext:
    """Contextual information about an error."""
    timestamp: datetime = field(default_factory=datetime.now)
    service: Optional[str] = None
    operation: Optional[str] = None
    user_input: Optional[str] = None
    config_values: Optional[Dict[str, Any]] = None
    system_state: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None


@dataclass
class RecoveryAction:
    """Suggested recovery action for an error."""
    description: str
    action_type: str  # "user", "automatic", "manual"
    command: Optional[str] = None
    priority: int = 1  # Lower number = higher priority


@dataclass
class ErrorAggregation:
    """Aggregated error information for reporting."""
    error_type: str
    count: int
    first_seen: datetime
    last_seen: datetime
    contexts: List[ErrorContext] = field(default_factory=list)
    recovery_success_rate: float = 0.0


# =============================================================================
# Base Exception Class
# =============================================================================

class LearningAgentError(Exception):
    """
    Base exception class for all Learning Agent errors.
    
    Provides comprehensive error information including context, recovery suggestions,
    and classification for proper handling and observability.
    """
    
    def __init__(
        self,
        message: str,
        *,
        category: ErrorCategory = ErrorCategory.INTERNAL,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[ErrorContext] = None,
        recovery_actions: Optional[List[RecoveryAction]] = None,
        user_message: Optional[str] = None,
        technical_details: Optional[Dict[str, Any]] = None,
        caused_by: Optional[Exception] = None
    ) -> None:
        """
        Initialize Learning Agent error.
        
        Args:
            message: Technical error message for developers
            category: Error category for classification
            severity: Error severity level
            context: Contextual information about the error
            recovery_actions: Suggested recovery actions
            user_message: User-friendly error message
            technical_details: Additional technical information
            caused_by: Underlying exception that caused this error
        """
        super().__init__(message)
        
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext()
        self.recovery_actions = recovery_actions or []
        self.user_message = user_message or self._generate_user_message()
        self.technical_details = technical_details or {}
        self.caused_by = caused_by
        
        # Capture stack trace
        self.stack_trace = traceback.format_exc() if sys.exc_info()[0] else None
    
    def _generate_user_message(self) -> str:
        """Generate a user-friendly error message."""
        category_messages = {
            ErrorCategory.CONFIGURATION: "There's an issue with the configuration settings.",
            ErrorCategory.AUTHENTICATION: "There's an authentication problem.",
            ErrorCategory.NETWORK: "There's a network connectivity issue.",
            ErrorCategory.SERVICE: "A service is currently unavailable.",
            ErrorCategory.VALIDATION: "The provided data is invalid.",
            ErrorCategory.PROCESSING: "There was an error processing your request.",
            ErrorCategory.RESOURCE: "System resources are insufficient.",
            ErrorCategory.USER_INPUT: "There's an issue with the input provided.",
            ErrorCategory.INTERNAL: "An internal error occurred.",
        }
        return category_messages.get(self.category, "An unexpected error occurred.")
    
    def get_recovery_suggestions(self) -> List[str]:
        """Get user-friendly recovery suggestions."""
        return [action.description for action in self.recovery_actions]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging and reporting."""
        return {
            "type": self.__class__.__name__,
            "message": str(self),
            "user_message": self.user_message,
            "category": self.category.value,
            "severity": self.severity.value,
            "context": {
                "timestamp": self.context.timestamp.isoformat(),
                "service": self.context.service,
                "operation": self.context.operation,
                "correlation_id": self.context.correlation_id,
            },
            "recovery_actions": [
                {
                    "description": action.description,
                    "type": action.action_type,
                    "command": action.command,
                    "priority": action.priority,
                }
                for action in self.recovery_actions
            ],
            "technical_details": self.technical_details,
            "caused_by": str(self.caused_by) if self.caused_by else None,
            "stack_trace": self.stack_trace,
        }
    
    def __str__(self) -> str:
        """String representation with context."""
        base_msg = super().__str__()
        if self.context.service:
            return f"[{self.context.service}] {base_msg}"
        return base_msg


# =============================================================================
# Configuration Errors
# =============================================================================

class ConfigurationError(LearningAgentError):
    """Base class for configuration-related errors."""
    
    def __init__(self, message: str, **kwargs) -> None:
        kwargs.setdefault('category', ErrorCategory.CONFIGURATION)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        super().__init__(message, **kwargs)


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""
    
    def __init__(self, config_key: str, **kwargs) -> None:
        message = f"Missing required configuration: {config_key}"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Add '{config_key}' to your configuration file",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description="Check the configuration documentation for valid values",
                action_type="manual",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"Please add the required configuration setting: {config_key}")
        
        super().__init__(message, **kwargs)


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration values are invalid."""
    
    def __init__(self, config_key: str, invalid_value: Any, expected: str, **kwargs) -> None:
        message = f"Invalid configuration for '{config_key}': {invalid_value} (expected: {expected})"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Set '{config_key}' to a valid value: {expected}",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description="Validate your configuration file",
                action_type="user",
                command="config validate",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"The configuration value for '{config_key}' is invalid. {expected}")
        kwargs.setdefault('technical_details', {
            'config_key': config_key,
            'invalid_value': str(invalid_value),
            'expected': expected,
        })
        
        super().__init__(message, **kwargs)


# =============================================================================
# Authentication Errors
# =============================================================================

class AuthenticationError(LearningAgentError):
    """Base class for authentication-related errors."""
    
    def __init__(self, message: str, **kwargs) -> None:
        kwargs.setdefault('category', ErrorCategory.AUTHENTICATION)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        super().__init__(message, **kwargs)


class APIKeyError(AuthenticationError):
    """Raised when API key is missing or invalid."""
    
    def __init__(self, provider: str, **kwargs) -> None:
        message = f"Invalid or missing API key for {provider}"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Set a valid API key for {provider} in your environment variables",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description=f"Switch to a different LLM provider",
                action_type="user",
                command="provider switch",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"Please provide a valid API key for {provider}")
        kwargs.setdefault('technical_details', {'provider': provider})
        
        super().__init__(message, **kwargs)


# =============================================================================
# Service Errors
# =============================================================================

class ServiceError(LearningAgentError):
    """Base class for service-related errors."""
    
    def __init__(self, message: str, **kwargs) -> None:
        kwargs.setdefault('category', ErrorCategory.SERVICE)
        kwargs.setdefault('severity', ErrorSeverity.MEDIUM)
        super().__init__(message, **kwargs)


class LLMServiceError(ServiceError):
    """Raised when LLM service encounters an error."""
    
    def __init__(self, provider: LLMProvider, operation: str, **kwargs) -> None:
        message = f"LLM service error ({provider.value}): {operation} failed"
        
        recovery_actions = [
            RecoveryAction(
                description="Retry the operation",
                action_type="automatic",
                priority=1
            ),
            RecoveryAction(
                description="Switch to a different LLM provider",
                action_type="user",
                command="provider switch",
                priority=2
            ),
            RecoveryAction(
                description="Check service health",
                action_type="user",
                command="rag status",
                priority=3
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"The {provider.value} service is having issues. Please try again.")
        kwargs.setdefault('technical_details', {
            'provider': provider.value,
            'operation': operation,
        })
        
        super().__init__(message, **kwargs)


class VectorServiceError(ServiceError):
    """Raised when vector/RAG service encounters an error."""
    
    def __init__(self, service_name: str, operation: str, **kwargs) -> None:
        message = f"Vector service error ({service_name}): {operation} failed"
        
        recovery_actions = [
            RecoveryAction(
                description="Check if RAGFlow service is running",
                action_type="user",
                command="rag status",
                priority=1
            ),
            RecoveryAction(
                description="Restart RAGFlow service",
                action_type="user",
                command="make ragflow-restart",
                priority=2
            ),
            RecoveryAction(
                description="Check Docker containers",
                action_type="manual",
                priority=3
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', "The knowledge retrieval service is unavailable. Please check the service status.")
        kwargs.setdefault('technical_details', {
            'service_name': service_name,
            'operation': operation,
        })
        
        super().__init__(message, **kwargs)


class RAGFlowServiceError(VectorServiceError):
    """Raised when RAGFlow service encounters an error."""
    
    def __init__(self, operation: str, **kwargs) -> None:
        super().__init__("RAGFlow", operation, **kwargs)


class MemoryServiceError(ServiceError):
    """Raised when memory service encounters an error."""
    
    def __init__(self, operation: str, **kwargs) -> None:
        message = f"Memory service error: {operation} failed"
        
        recovery_actions = [
            RecoveryAction(
                description="Clear conversation memory",
                action_type="user",
                command="memory clear",
                priority=1
            ),
            RecoveryAction(
                description="Disable memory temporarily",
                action_type="user",
                command="memory disable",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', "There's an issue with conversation memory. Consider clearing it.")
        kwargs.setdefault('technical_details', {'operation': operation})
        
        super().__init__(message, **kwargs)


# =============================================================================
# Processing Errors
# =============================================================================

class ProcessingError(LearningAgentError):
    """Base class for processing-related errors."""
    
    def __init__(self, message: str, **kwargs) -> None:
        kwargs.setdefault('category', ErrorCategory.PROCESSING)
        kwargs.setdefault('severity', ErrorSeverity.MEDIUM)
        super().__init__(message, **kwargs)


class DocumentProcessingError(ProcessingError):
    """Raised when document processing fails."""
    
    def __init__(self, document_name: str, reason: str, **kwargs) -> None:
        message = f"Failed to process document '{document_name}': {reason}"
        
        recovery_actions = [
            RecoveryAction(
                description="Check if the document format is supported",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description="Try processing a different document",
                action_type="user",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"Unable to process the document '{document_name}'. Please check the file format.")
        kwargs.setdefault('technical_details', {
            'document_name': document_name,
            'reason': reason,
        })
        
        super().__init__(message, **kwargs)


class LaTeXRenderingError(ProcessingError):
    """Raised when LaTeX rendering fails."""
    
    def __init__(self, latex_content: str, **kwargs) -> None:
        message = f"Failed to render LaTeX content: {latex_content[:100]}..."
        
        recovery_actions = [
            RecoveryAction(
                description="Try with simpler LaTeX expressions",
                action_type="user",
                priority=1
            ),
            RecoveryAction(
                description="Disable advanced LaTeX rendering",
                action_type="user",
                command="config update ui.use_advanced_latex_rendering false",
                priority=2
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', "Unable to render mathematical expressions. Displaying as plain text.")
        kwargs.setdefault('technical_details', {'latex_content': latex_content[:200]})
        
        super().__init__(message, **kwargs)


# =============================================================================
# Network and Resource Errors
# =============================================================================

class NetworkError(LearningAgentError):
    """Raised when network operations fail."""
    
    def __init__(self, message: str, **kwargs) -> None:
        kwargs.setdefault('category', ErrorCategory.NETWORK)
        kwargs.setdefault('severity', ErrorSeverity.MEDIUM)
        
        recovery_actions = [
            RecoveryAction(
                description="Check your internet connection",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description="Retry the operation",
                action_type="automatic",
                priority=2
            ),
            RecoveryAction(
                description="Try again later",
                action_type="user",
                priority=3
            ),
        ]
        
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', "Network connection issue. Please check your internet connection.")
        
        super().__init__(message, **kwargs)


class ResourceError(LearningAgentError):
    """Raised when system resources are insufficient."""
    
    def __init__(self, resource_type: str, **kwargs) -> None:
        message = f"Insufficient {resource_type} resources"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Free up {resource_type} resources",
                action_type="manual",
                priority=1
            ),
            RecoveryAction(
                description="Reduce batch size or complexity",
                action_type="user",
                priority=2
            ),
            RecoveryAction(
                description="Enable memory optimization",
                action_type="user",
                command="config update performance.memory_optimization true",
                priority=3
            ),
        ]
        
        kwargs.setdefault('category', ErrorCategory.RESOURCE)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"System {resource_type} is running low. Please free up resources.")
        kwargs.setdefault('technical_details', {'resource_type': resource_type})
        
        super().__init__(message, **kwargs)


# =============================================================================
# User Input and Validation Errors
# =============================================================================

class ValidationError(LearningAgentError):
    """Raised when data validation fails."""
    
    def __init__(self, field: str, value: Any, constraint: str, **kwargs) -> None:
        message = f"Validation failed for '{field}': {constraint}"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Provide a valid value for '{field}': {constraint}",
                action_type="user",
                priority=1
            ),
        ]
        
        kwargs.setdefault('category', ErrorCategory.VALIDATION)
        kwargs.setdefault('severity', ErrorSeverity.LOW)
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"Invalid input for '{field}'. {constraint}")
        kwargs.setdefault('technical_details', {
            'field': field,
            'value': str(value),
            'constraint': constraint,
        })
        
        super().__init__(message, **kwargs)


class UserInputError(LearningAgentError):
    """Raised when user input is invalid or malformed."""
    
    def __init__(self, input_type: str, reason: str, **kwargs) -> None:
        message = f"Invalid {input_type}: {reason}"
        
        recovery_actions = [
            RecoveryAction(
                description=f"Provide valid {input_type}",
                action_type="user",
                priority=1
            ),
            RecoveryAction(
                description="Check the help documentation",
                action_type="user",
                command="help",
                priority=2
            ),
        ]
        
        kwargs.setdefault('category', ErrorCategory.USER_INPUT)
        kwargs.setdefault('severity', ErrorSeverity.LOW)
        kwargs.setdefault('recovery_actions', recovery_actions)
        kwargs.setdefault('user_message', f"Invalid {input_type}. {reason}")
        kwargs.setdefault('technical_details', {
            'input_type': input_type,
            'reason': reason,
        })
        
        super().__init__(message, **kwargs)


# =============================================================================
# Error Aggregation and Reporting
# =============================================================================

class ErrorAggregator:
    """Aggregates and analyzes errors for reporting and pattern detection."""
    
    def __init__(self, max_errors: int = 1000) -> None:
        """Initialize error aggregator with maximum error storage."""
        self.max_errors = max_errors
        self._errors: List[LearningAgentError] = []
        self._aggregations: Dict[str, ErrorAggregation] = {}
    
    def add_error(self, error: LearningAgentError) -> None:
        """Add an error to the aggregator."""
        self._errors.append(error)
        
        # Maintain size limit
        if len(self._errors) > self.max_errors:
            self._errors = self._errors[-self.max_errors:]
        
        # Update aggregations
        error_type = error.__class__.__name__
        if error_type not in self._aggregations:
            self._aggregations[error_type] = ErrorAggregation(
                error_type=error_type,
                count=0,
                first_seen=error.context.timestamp,
                last_seen=error.context.timestamp,
            )
        
        agg = self._aggregations[error_type]
        agg.count += 1
        agg.last_seen = error.context.timestamp
        agg.contexts.append(error.context)
        
        # Maintain context limit
        if len(agg.contexts) > 10:
            agg.contexts = agg.contexts[-10:]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors."""
        total_errors = len(self._errors)
        if total_errors == 0:
            return {"total_errors": 0, "aggregations": {}}
        
        # Calculate statistics
        severity_counts = {}
        category_counts = {}
        
        for error in self._errors:
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
            category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
        
        return {
            "total_errors": total_errors,
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "aggregations": {
                error_type: {
                    "count": agg.count,
                    "first_seen": agg.first_seen.isoformat(),
                    "last_seen": agg.last_seen.isoformat(),
                    "recovery_success_rate": agg.recovery_success_rate,
                }
                for error_type, agg in self._aggregations.items()
            },
        }
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors as dictionaries."""
        recent = self._errors[-limit:] if len(self._errors) >= limit else self._errors
        return [error.to_dict() for error in reversed(recent)]
    
    def clear_errors(self) -> None:
        """Clear all stored errors."""
        self._errors.clear()
        self._aggregations.clear()


# =============================================================================
# Global Error Aggregator
# =============================================================================

# Global error aggregator instance
_error_aggregator: Optional[ErrorAggregator] = None


def get_error_aggregator() -> ErrorAggregator:
    """Get or create global error aggregator instance."""
    global _error_aggregator
    
    if _error_aggregator is None:
        _error_aggregator = ErrorAggregator()
    
    return _error_aggregator


def report_error(error: LearningAgentError) -> None:
    """Report an error to the global aggregator."""
    get_error_aggregator().add_error(error)


# =============================================================================
# Utility Functions
# =============================================================================

def create_error_context(
    service: Optional[str] = None,
    operation: Optional[str] = None,
    user_input: Optional[str] = None,
    correlation_id: Optional[str] = None,
    **kwargs
) -> ErrorContext:
    """Create an error context with common fields."""
    return ErrorContext(
        service=service,
        operation=operation,
        user_input=user_input,
        correlation_id=correlation_id,
        system_state=kwargs
    )


def handle_exception(
    exc: Exception,
    service: Optional[str] = None,
    operation: Optional[str] = None,
    user_input: Optional[str] = None,
    correlation_id: Optional[str] = None
) -> LearningAgentError:
    """
    Convert a generic exception to a Learning Agent error.
    
    Args:
        exc: The original exception
        service: Service where the error occurred
        operation: Operation being performed
        user_input: User input that caused the error
        correlation_id: Correlation ID for tracing
    
    Returns:
        LearningAgentError: Wrapped exception with context
    """
    context = create_error_context(
        service=service,
        operation=operation,
        user_input=user_input,
        correlation_id=correlation_id
    )
    
    # Map common exception types to specific errors
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return NetworkError(
            f"Network error: {str(exc)}",
            context=context,
            caused_by=exc
        )
    elif isinstance(exc, MemoryError):
        return ResourceError(
            "memory",
            context=context,
            caused_by=exc
        )
    elif isinstance(exc, ValueError):
        return ValidationError(
            "value",
            str(exc),
            "Valid input required",
            context=context,
            caused_by=exc
        )
    else:
        # Generic wrapping
        return LearningAgentError(
            f"Unexpected error: {str(exc)}",
            category=ErrorCategory.INTERNAL,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            caused_by=exc
        ) 