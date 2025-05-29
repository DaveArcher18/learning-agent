"""
Unit tests for the LLM Service module.

Tests multi-provider support, health monitoring, automatic failover,
mathematical reasoning optimization, and performance metrics.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
from pathlib import Path
import time

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.services.llm_service import LLMService, LLMFactory
from src.core.config import LLMConfig
from src.utils.exceptions import LLMServiceError, APIKeyError, NetworkError
from src.core.types import LLMProvider


class TestLLMService:
    """Test suite for LLM service functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = LLMConfig(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=2048,
            timeout=30
        )
        self.llm_service = LLMService(self.config)
    
    @pytest.mark.unit
    def test_llm_service_initialization(self):
        """Test LLM service initialization."""
        assert self.llm_service is not None
        assert self.llm_service.current_provider == "deepseek"
        assert hasattr(self.llm_service, 'generate_response')
        assert hasattr(self.llm_service, 'switch_provider')
        assert hasattr(self.llm_service, 'health_check')
    
    @pytest.mark.unit
    def test_get_available_providers(self):
        """Test getting available LLM providers."""
        providers = self.llm_service.get_available_providers()
        
        assert isinstance(providers, list)
        assert len(providers) > 0
        
        # Check expected providers
        expected_providers = ["deepseek", "openai", "anthropic", "ollama", "groq"]
        for provider in expected_providers:
            assert provider in providers
    
    @pytest.mark.unit
    def test_get_current_provider(self):
        """Test getting current provider."""
        current = self.llm_service.get_current_provider()
        assert current == "deepseek"
        
        # After switching, should return new provider
        self.llm_service.switch_provider("openai")
        current = self.llm_service.get_current_provider()
        assert current == "openai"
    
    @pytest.mark.unit
    @patch('src.services.llm_service.openai.ChatCompletion.create')
    def test_generate_response_openai(self, mock_openai):
        """Test response generation with OpenAI."""
        # Setup mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response from OpenAI"
        mock_response.usage = Mock()
        mock_response.usage.total_tokens = 100
        mock_openai.return_value = mock_response
        
        # Switch to OpenAI and generate response
        self.llm_service.switch_provider("openai")
        response = self.llm_service.generate_response("Test query")
        
        assert response == "Test response from OpenAI"
        mock_openai.assert_called_once()
    
    @pytest.mark.unit
    @patch('requests.post')
    def test_generate_response_deepseek(self, mock_post):
        """Test response generation with DeepSeek."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Test response from DeepSeek"
                }
            }],
            "usage": {
                "total_tokens": 150
            }
        }
        mock_post.return_value = mock_response
        
        # Generate response with DeepSeek (default)
        response = self.llm_service.generate_response("Test query")
        
        assert response == "Test response from DeepSeek"
        mock_post.assert_called_once()
    
    @pytest.mark.unit
    def test_provider_switching(self):
        """Test switching between providers."""
        # Start with DeepSeek
        assert self.llm_service.current_provider == "deepseek"
        
        # Switch to OpenAI
        result = self.llm_service.switch_provider("openai")
        assert result is True
        assert self.llm_service.current_provider == "openai"
        
        # Switch to Anthropic
        result = self.llm_service.switch_provider("anthropic")
        assert result is True
        assert self.llm_service.current_provider == "anthropic"
        
        # Invalid provider should fail
        result = self.llm_service.switch_provider("invalid_provider")
        assert result is False
        assert self.llm_service.current_provider == "anthropic"  # Should remain unchanged
    
    @pytest.mark.unit
    @patch('src.services.llm_service.requests.post')
    def test_health_check_success(self, mock_post):
        """Test successful health check."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "OK"}}]
        }
        mock_post.return_value = mock_response
        
        health = self.llm_service.health_check()
        
        assert health["status"] == "healthy"
        assert health["provider"] == "deepseek"
        assert "response_time" in health
        assert health["response_time"] >= 0
    
    @pytest.mark.unit
    @patch('src.services.llm_service.requests.post')
    def test_health_check_failure(self, mock_post):
        """Test failed health check."""
        # Mock failed response
        mock_post.side_effect = Exception("Connection failed")
        
        health = self.llm_service.health_check()
        
        assert health["status"] == "unhealthy"
        assert health["provider"] == "deepseek"
        assert "error" in health
        assert "Connection failed" in health["error"]
    
    @pytest.mark.unit
    @patch('src.services.llm_service.requests.post')
    def test_automatic_failover(self, mock_post):
        """Test automatic failover to backup provider."""
        # First call fails, second succeeds
        mock_post.side_effect = [
            Exception("Primary provider failed"),
            Mock(status_code=200, json=lambda: {
                "choices": [{"message": {"content": "Backup response"}}],
                "usage": {"total_tokens": 80}
            })
        ]
        
        # Should automatically failover and succeed
        response = self.llm_service.generate_response("Test query", enable_failover=True)
        
        assert response == "Backup response"
        assert mock_post.call_count == 2  # Primary + failover
    
    @pytest.mark.unit
    def test_mathematical_reasoning_optimization(self):
        """Test mathematical reasoning optimization."""
        # Mathematical query should get optimized prompt
        math_query = "Solve the equation x^2 + 2x + 1 = 0"
        
        with patch.object(self.llm_service, '_generate_with_provider') as mock_generate:
            mock_generate.return_value = "Mathematical solution"
            
            response = self.llm_service.generate_response(math_query)
            
            # Check that mathematical optimization was applied
            call_args = mock_generate.call_args
            prompt = call_args[0][1]  # Second argument is the prompt
            
            assert "mathematical" in prompt.lower() or "math" in prompt.lower()
            assert response == "Mathematical solution"
    
    @pytest.mark.unit
    def test_error_handling_api_key_error(self):
        """Test handling of API key errors."""
        with patch('src.services.llm_service.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {"error": "Invalid API key"}
            mock_post.return_value = mock_response
            
            with pytest.raises(APIKeyError):
                self.llm_service.generate_response("Test query")
    
    @pytest.mark.unit
    def test_error_handling_network_error(self):
        """Test handling of network errors."""
        with patch('src.services.llm_service.requests.post') as mock_post:
            mock_post.side_effect = ConnectionError("Network unreachable")
            
            with pytest.raises(NetworkError):
                self.llm_service.generate_response("Test query")
    
    @pytest.mark.unit
    def test_retry_logic_exponential_backoff(self):
        """Test exponential backoff retry logic."""
        call_times = []
        
        def mock_failing_request(*args, **kwargs):
            call_times.append(time.time())
            if len(call_times) < 3:
                raise Exception("Temporary failure")
            else:
                return Mock(status_code=200, json=lambda: {
                    "choices": [{"message": {"content": "Success after retries"}}],
                    "usage": {"total_tokens": 90}
                })
        
        with patch('src.services.llm_service.requests.post', side_effect=mock_failing_request):
            response = self.llm_service.generate_response("Test query", max_retries=3)
            
            assert response == "Success after retries"
            assert len(call_times) == 3
            
            # Check exponential backoff (allowing some tolerance)
            if len(call_times) >= 2:
                time_diff = call_times[1] - call_times[0]
                assert time_diff >= 1.0  # At least 1 second delay
    
    @pytest.mark.unit
    def test_performance_metrics_tracking(self):
        """Test performance metrics tracking."""
        with patch('src.services.llm_service.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "Test response"}}],
                "usage": {"total_tokens": 100}
            }
            mock_post.return_value = mock_response
            
            # Generate several responses
            for i in range(3):
                self.llm_service.generate_response(f"Test query {i}")
            
            metrics = self.llm_service.get_metrics()
            
            assert isinstance(metrics, dict)
            assert "requests_total" in metrics
            assert "avg_response_time" in metrics
            assert "error_rate" in metrics
            assert "total_tokens_used" in metrics
            assert metrics["requests_total"] >= 3
    
    @pytest.mark.unit
    def test_conversation_context_handling(self):
        """Test conversation context handling."""
        conversation = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "2+2 equals 4."},
            {"role": "user", "content": "What about 3+3?"}
        ]
        
        with patch.object(self.llm_service, '_generate_with_provider') as mock_generate:
            mock_generate.return_value = "3+3 equals 6."
            
            response = self.llm_service.generate_response(
                "What about 3+3?", 
                conversation_context=conversation
            )
            
            # Check that conversation context was included
            call_args = mock_generate.call_args
            assert len(call_args[0]) >= 2  # Provider and prompt
            
            assert response == "3+3 equals 6."
    
    @pytest.mark.unit
    @pytest.mark.slow
    def test_timeout_handling(self):
        """Test request timeout handling."""
        # Configure short timeout
        self.llm_service.config.timeout = 1
        
        def slow_response(*args, **kwargs):
            time.sleep(2)  # Longer than timeout
            return Mock(status_code=200)
        
        with patch('src.services.llm_service.requests.post', side_effect=slow_response):
            with pytest.raises(Exception):  # Should timeout
                self.llm_service.generate_response("Test query")


class TestLLMFactory:
    """Test suite for LLM factory functionality."""
    
    @pytest.mark.unit
    def test_factory_create_service(self):
        """Test creating LLM service through factory."""
        config = LLMConfig(provider="openai")
        service = LLMFactory.create_service(config)
        
        assert isinstance(service, LLMService)
        assert service.current_provider == "openai"
    
    @pytest.mark.unit
    def test_factory_get_provider_config(self):
        """Test getting provider-specific configuration."""
        openai_config = LLMFactory.get_provider_config("openai")
        deepseek_config = LLMFactory.get_provider_config("deepseek")
        anthropic_config = LLMFactory.get_provider_config("anthropic")
        
        assert isinstance(openai_config, dict)
        assert isinstance(deepseek_config, dict)
        assert isinstance(anthropic_config, dict)
        
        # Check that configs have expected fields
        assert "model" in openai_config
        assert "model" in deepseek_config
        assert "model" in anthropic_config
    
    @pytest.mark.unit
    def test_factory_invalid_provider(self):
        """Test factory handling of invalid providers."""
        with pytest.raises(ValueError):
            LLMFactory.get_provider_config("invalid_provider")


class TestLLMServiceIntegration:
    """Integration tests for LLM service with other components."""
    
    @pytest.mark.integration
    def test_integration_with_config(self):
        """Test LLM service integration with configuration."""
        from src.core.config import LearningAgentConfig
        
        # Create full configuration
        full_config = LearningAgentConfig(
            llm={
                "provider": "deepseek",
                "model": "deepseek-chat",
                "temperature": 0.5,
                "max_tokens": 1024
            }
        )
        
        service = LLMService(full_config.llm)
        
        assert service.current_provider == "deepseek"
        assert service.config.temperature == 0.5
        assert service.config.max_tokens == 1024
    
    @pytest.mark.integration
    @pytest.mark.requires_llm
    def test_integration_with_memory_service(self, mock_memory_service):
        """Test LLM service integration with memory service."""
        # Mock conversation from memory service
        conversation = mock_memory_service.get_conversation.return_value
        
        with patch.object(self.llm_service, '_generate_with_provider') as mock_generate:
            mock_generate.return_value = "Response with context"
            
            response = self.llm_service.generate_response(
                "New question",
                conversation_context=conversation
            )
            
            assert response == "Response with context"
            mock_generate.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.mathematical
    def test_integration_with_latex_renderer(self):
        """Test LLM service integration with LaTeX renderer."""
        from src.text_processing.latex_renderer import LatexRenderer
        
        # Generate response with mathematical content
        math_response = "The solution is $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$"
        
        with patch.object(self.llm_service, '_generate_with_provider') as mock_generate:
            mock_generate.return_value = math_response
            
            response = self.llm_service.generate_response("Solve quadratic equation")
            
            # Should be able to render mathematical content
            renderer = LatexRenderer()
            rendered = renderer.render_latex(response)
            
            assert "x = " in rendered
            assert "$" not in rendered  # LaTeX should be converted


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 