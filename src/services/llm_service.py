"""
LLM Service Module

Provides a factory class for managing different LLM providers with health monitoring,
retry logic, and optimization for mathematical reasoning tasks.

This module focuses on:
- Provider abstraction and management
- Connection health monitoring  
- Retry logic with exponential backoff
- Mathematical reasoning optimization
- Structured logging for provider operations
- Performance metrics collection
"""

import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import backoff

# Core imports 
from ..core.config import ConfigManager
from ..observability.metrics import record_llm_request, get_metrics_collector

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    GROQ = "groq"

@dataclass
class LLMResponse:
    """Standardized LLM response structure"""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    mathematical_content: bool = False

@dataclass
class ProviderHealth:
    """Health status for an LLM provider"""
    is_healthy: bool
    last_check: float
    error_count: int
    avg_response_time: float
    last_error: Optional[str] = None

class LLMServiceError(Exception):
    """Custom exception for LLM service errors"""
    def __init__(self, message: str, provider: str = None, retryable: bool = True):
        self.provider = provider
        self.retryable = retryable
        super().__init__(message)

class LLMService:
    """
    Enhanced LLM service with mathematical reasoning optimization.
    
    Features:
    - Multiple provider support with automatic failover
    - Health monitoring and retry logic
    - Mathematical content optimization
    - Structured logging and metrics
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize LLM service with configuration.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.providers: Dict[str, Any] = {}
        self.health_status: Dict[str, ProviderHealth] = {}
        self.current_provider = None
        self._initialize_providers()
        logger.info("LLM service initialized", extra={
            "available_providers": list(self.providers.keys()),
            "default_provider": self.config.get("llm.default_provider", "deepseek")
        })
    
    def _initialize_providers(self) -> None:
        """Initialize only OpenRouter LLM provider"""
        # OpenRouter - Primary and only provider
        self._setup_openrouter()
        
        # Set default provider
        default_provider = self.config.get("llm.model_provider", "openrouter")
        if default_provider in self.providers:
            self.current_provider = default_provider
        else:
            # Fall back to first available provider
            self.current_provider = next(iter(self.providers.keys())) if self.providers else None
    
    def _setup_openrouter(self) -> None:
        """Setup OpenRouter provider"""
        try:
            import openai
            
            api_key = self.config.get("llm.providers.openrouter.api_key")
            if not api_key:
                logger.warning("OpenRouter API key not configured")
                return
            
            # OpenRouter requires specific headers
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/learning-agent",  # Optional: specify your app
                    "X-Title": "Learning Agent",  # Optional: specify your app name
                }
            )
            
            self.providers["openrouter"] = {
                "client": client,
                "model": self.config.get("llm.model", "deepseek/deepseek-prover-v2:free"),
                "max_tokens": self.config.get("llm.max_tokens", 4000),
                "temperature": self.config.get("llm.temperature", 0.3),
                "mathematical_optimized": True
            }
            
            self.health_status["openrouter"] = ProviderHealth(
                is_healthy=True, last_check=time.time(), error_count=0, avg_response_time=0.0
            )
            
            logger.info("OpenRouter provider initialized")
            
        except ImportError:
            logger.error("OpenAI library not available for OpenRouter provider")
        except Exception as e:
            logger.error("Failed to initialize OpenRouter provider", extra={"error": str(e)})
    
    @backoff.on_exception(
        backoff.expo,
        LLMServiceError,
        max_tries=3,
        max_time=30
    )
    def generate_response(
        self, 
        query: str, 
        context: Optional[str] = None,
        mathematical_content: bool = False,
        provider: Optional[str] = None
    ) -> LLMResponse:
        """
        Generate response using the specified or best available provider.
        
        Args:
            query: User query
            context: Optional context from RAG retrieval
            mathematical_content: Whether content contains mathematical expressions
            provider: Specific provider to use (optional)
            
        Returns:
            LLMResponse: Generated response with metadata
            
        Raises:
            LLMServiceError: If all providers fail or no providers available
        """
        start_time = time.time()
        
        # Select provider
        selected_provider = provider or self._get_healthy_provider(mathematical_content)
        if not selected_provider:
            error_msg = "No healthy LLM providers available"
            logger.error(error_msg)
            # Record error in metrics
            record_llm_request("unknown", "unknown", 0, False)
            raise LLMServiceError(error_msg, retryable=False)
        
        # Build optimized prompt
        prompt = self._build_prompt(query, context, mathematical_content)
        
        try:
            # Generate response
            raw_response = self._call_provider(selected_provider, prompt)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Extract response content and metadata
            provider_config = self.providers[selected_provider]
            
            # Create structured response
            response = LLMResponse(
                content=raw_response.content,
                provider=selected_provider,
                model=provider_config["model"],
                response_time=response_time,
                mathematical_content=mathematical_content,
                tokens_used=raw_response.tokens_used or self._estimate_tokens(raw_response.content)
            )
            
            # Update health metrics
            self._update_health_metrics(selected_provider, response_time, True)
            
            # Record successful metrics
            record_llm_request(
                provider=selected_provider,
                model=provider_config["model"],
                response_time=response_time,
                success=True,
                token_count=response.tokens_used
            )
            
            logger.info("LLM response generated successfully", extra={
                "provider": selected_provider,
                "model": provider_config["model"],
                "response_time": response_time,
                "mathematical_content": mathematical_content,
                "estimated_tokens": response.tokens_used
            })
            
            return response
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f"LLM generation failed with {selected_provider}: {str(e)}"
            
            # Update health metrics
            self._update_health_metrics(selected_provider, response_time, False, str(e))
            
            # Record failed metrics
            provider_config = self.providers.get(selected_provider, {})
            record_llm_request(
                provider=selected_provider,
                model=provider_config.get("model", "unknown"),
                response_time=response_time,
                success=False
            )
            
            logger.error(error_msg, extra={
                "provider": selected_provider,
                "error": str(e),
                "response_time": response_time
            })
            
            raise LLMServiceError(error_msg, provider=selected_provider, retryable=True)
    
    def _build_prompt(self, query: str, context: Optional[str], mathematical_content: bool) -> str:
        """Build optimized prompt for mathematical reasoning"""
        if mathematical_content:
            # Enhanced prompt for mathematical content
            system_prompt = self.config.get(
                "llm.mathematical_system_prompt",
                "You are an expert in mathematics and mathematical reasoning. "
                "Provide clear, step-by-step explanations with proper mathematical notation. "
                "Use LaTeX formatting for mathematical expressions where appropriate."
            )
        else:
            system_prompt = self.config.get(
                "llm.default_system_prompt",
                "You are a helpful AI assistant. Provide clear and accurate responses."
            )
        
        if context:
            prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuery: {query}"
        else:
            prompt = f"{system_prompt}\n\nQuery: {query}"
        
        return prompt
    
    def _call_provider(self, provider: str, prompt: str) -> Any:
        """Call specific provider with standardized interface"""
        provider_config = self.providers[provider]
        
        if provider in ["deepseek", "openai", "openrouter"]:
            try:
                response = provider_config["client"].chat.completions.create(
                    model=provider_config["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=provider_config["max_tokens"],
                    temperature=provider_config["temperature"]
                )
                
                # Robust response handling
                if not response:
                    raise LLMServiceError(f"Empty response from {provider}")
                
                if not hasattr(response, 'choices') or not response.choices:
                    raise LLMServiceError(f"No choices in response from {provider}")
                
                if len(response.choices) == 0:
                    raise LLMServiceError(f"Empty choices list from {provider}")
                
                choice = response.choices[0]
                if not hasattr(choice, 'message') or not choice.message:
                    raise LLMServiceError(f"No message in response choice from {provider}")
                
                content = choice.message.content
                if content is None:
                    raise LLMServiceError(f"Null content in response from {provider}")
                
                # Extract token usage safely
                tokens_used = None
                if hasattr(response, 'usage') and response.usage:
                    tokens_used = getattr(response.usage, 'total_tokens', None)
                
                return type('Response', (), {
                    'content': content,
                    'tokens_used': tokens_used
                })()
                
            except Exception as e:
                if isinstance(e, LLMServiceError):
                    raise
                raise LLMServiceError(f"API call failed for {provider}: {str(e)}")
        
        elif provider == "anthropic":
            try:
                response = provider_config["client"].messages.create(
                    model=provider_config["model"],
                    max_tokens=provider_config["max_tokens"],
                    temperature=provider_config["temperature"],
                    messages=[{"role": "user", "content": prompt}]
                )
                
                if not response or not hasattr(response, 'content') or not response.content:
                    raise LLMServiceError(f"Empty or invalid response from {provider}")
                
                content = response.content[0].text if response.content else None
                if content is None:
                    raise LLMServiceError(f"Null content in response from {provider}")
                
                tokens_used = None
                if hasattr(response, 'usage') and response.usage:
                    tokens_used = getattr(response.usage, 'total_tokens', None)
                
                return type('Response', (), {
                    'content': content,
                    'tokens_used': tokens_used
                })()
                
            except Exception as e:
                if isinstance(e, LLMServiceError):
                    raise
                raise LLMServiceError(f"API call failed for {provider}: {str(e)}")
        
        elif provider == "ollama":
            try:
                response = provider_config["client"].chat(
                    model=provider_config["model"],
                    messages=[{"role": "user", "content": prompt}],
                    options={"temperature": provider_config["temperature"]}
                )
                
                if not response or 'message' not in response:
                    raise LLMServiceError(f"Empty or invalid response from {provider}")
                
                content = response['message'].get('content')
                if content is None:
                    raise LLMServiceError(f"Null content in response from {provider}")
                
                return type('Response', (), {
                    'content': content,
                    'tokens_used': None
                })()
                
            except Exception as e:
                if isinstance(e, LLMServiceError):
                    raise
                raise LLMServiceError(f"API call failed for {provider}: {str(e)}")
        
        elif provider == "groq":
            try:
                response = provider_config["client"].chat.completions.create(
                    model=provider_config["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=provider_config["max_tokens"],
                    temperature=provider_config["temperature"]
                )
                
                if not response or not hasattr(response, 'choices') or not response.choices:
                    raise LLMServiceError(f"Empty or invalid response from {provider}")
                
                choice = response.choices[0]
                if not hasattr(choice, 'message') or not choice.message:
                    raise LLMServiceError(f"No message in response choice from {provider}")
                
                content = choice.message.content
                if content is None:
                    raise LLMServiceError(f"Null content in response from {provider}")
                
                tokens_used = None
                if hasattr(response, 'usage') and response.usage:
                    tokens_used = getattr(response.usage, 'total_tokens', None)
                
                return type('Response', (), {
                    'content': content,
                    'tokens_used': tokens_used
                })()
                
            except Exception as e:
                if isinstance(e, LLMServiceError):
                    raise
                raise LLMServiceError(f"API call failed for {provider}: {str(e)}")
        
        else:
            raise LLMServiceError(f"Unknown provider: {provider}")
    
    def _check_provider_health(self, provider: str) -> bool:
        """Check if a provider is healthy"""
        if provider not in self.health_status:
            return False
        
        health = self.health_status[provider]
        
        # Consider unhealthy if too many recent errors
        if health.error_count > 3:
            return False
        
        # Check if last health check was recent
        if time.time() - health.last_check > 300:  # 5 minutes
            # Perform health check
            return self._perform_health_check(provider)
        
        return health.is_healthy
    
    def _perform_health_check(self, provider: str) -> bool:
        """Perform active health check on provider"""
        try:
            # Simple test query
            test_response = self._call_provider(provider, "Test connection. Respond with 'OK'.")
            
            self.health_status[provider].is_healthy = True
            self.health_status[provider].last_check = time.time()
            self.health_status[provider].error_count = 0
            
            logger.debug(f"Health check passed for {provider}")
            return True
            
        except Exception as e:
            self.health_status[provider].is_healthy = False
            self.health_status[provider].last_check = time.time()
            self.health_status[provider].last_error = str(e)
            
            logger.warning(f"Health check failed for {provider}", extra={"error": str(e)})
            return False
    
    def _get_healthy_provider(self, prefer_mathematical: bool = False) -> Optional[str]:
        """Get a healthy provider, preferring mathematical optimization if requested"""
        healthy_providers = [
            p for p in self.providers.keys() 
            if self._check_provider_health(p)
        ]
        
        if not healthy_providers:
            return None
        
        # Prefer DeepSeek for mathematical content
        if prefer_mathematical and "deepseek" in healthy_providers:
            return "deepseek"
        
        # Return first healthy provider
        return healthy_providers[0]
    
    def _update_health_metrics(self, provider: str, response_time: float, success: bool, error: str = None) -> None:
        """Update health status and metrics for a provider"""
        if provider in self.health_status:
            health = self.health_status[provider]
            health.last_check = time.time()
            
            if success:
                health.is_healthy = True
                health.error_count = max(0, health.error_count - 1)  # Decrease error count on success
                # Update rolling average response time
                health.avg_response_time = (health.avg_response_time + response_time) / 2
            else:
                health.error_count += 1
                health.last_error = error
                # Mark unhealthy if too many consecutive errors
                if health.error_count >= 3:
                    health.is_healthy = False
                    logger.warning(f"Provider {provider} marked unhealthy after {health.error_count} errors")
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for a given text.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            int: Estimated token count
        """
        # Simple estimation: ~4 characters per token for most models
        # This is a rough approximation, more sophisticated methods could use tiktoken
        return max(1, len(text) // 4)
    
    def switch_provider(self, provider: str) -> bool:
        """
        Switch to a different LLM provider.
        
        Args:
            provider: Provider name to switch to
            
        Returns:
            bool: True if switch successful, False otherwise
        """
        if provider not in self.providers:
            logger.warning(f"Provider {provider} not available")
            return False
        
        if not self._check_provider_health(provider):
            logger.warning(f"Provider {provider} is not healthy")
            return False
        
        old_provider = self.current_provider
        self.current_provider = provider
        
        # Record provider switch in metrics
        collector = get_metrics_collector()
        collector.record_custom_metric(
            "llm.provider_switch",
            1.0,
            tags={"from": old_provider or "none", "to": provider}
        )
        
        logger.info(f"Switched LLM provider from {old_provider} to {provider}")
        return True
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed status for all providers."""
        return {
            provider: {
                "healthy": health.is_healthy,
                "error_count": health.error_count,
                "avg_response_time": health.avg_response_time,
                "last_error": health.last_error,
                "last_check": health.last_check
            }
            for provider, health in self.health_status.items()
        }


# =============================================================================
# Factory for backward compatibility
# =============================================================================

class LLMFactory:
    """
    Factory class for creating LLM service instances.
    
    Provides backward compatibility with existing code and tests.
    """
    
    @staticmethod
    def create_service(config: ConfigManager) -> LLMService:
        """Create an LLM service instance."""
        return LLMService(config)
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of available providers."""
        return ["deepseek", "openai", "anthropic", "ollama", "groq"]
    
    @staticmethod
    def get_provider_config(provider: str) -> Dict[str, Any]:
        """Get default configuration for a provider."""
        configs = {
            "deepseek": {
                "model": "deepseek-chat",
                "temperature": 0.1,
                "max_tokens": 4000,
                "mathematical_optimized": True
            },
            "openai": {
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 4000
            },
            "anthropic": {
                "model": "claude-3-sonnet-20240229",
                "temperature": 0.1,
                "max_tokens": 4000
            },
            "ollama": {
                "model": "qwen3:4b",
                "temperature": 0.1,
                "max_tokens": 4000
            },
            "groq": {
                "model": "mixtral-8x7b-32768",
                "temperature": 0.1,
                "max_tokens": 4000
            }
        }
        return configs.get(provider, {}) 