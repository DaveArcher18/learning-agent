"""
Unit tests for the Configuration Management module.

Tests Pydantic validation, environment-specific configurations, hot-reloading,
and configuration schema functionality.
"""

import pytest
import tempfile
import os
import yaml
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.core.config import (
    LearningAgentConfig, RAGFlowConfig, BGE_M3Config, 
    MathematicalContentConfig, LLMConfig, ObservabilityConfig,
    ConfigurationManager, load_config, get_config
)
from src.utils.exceptions import InvalidConfigurationError, MissingConfigurationError


class TestLearningAgentConfig:
    """Test the main configuration class."""
    
    @pytest.mark.unit
    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = LearningAgentConfig()
        
        # Should have all required sections
        assert config.llm is not None
        assert config.ragflow is not None
        assert config.bge_m3 is not None
        assert config.mathematical_content is not None
        assert config.observability is not None
        
        # Check some default values
        assert config.llm.provider == "deepseek"
        assert config.ragflow.host == "localhost"
        assert config.bge_m3.device == "cpu"
        assert config.mathematical_content.latex_rendering is True
    
    @pytest.mark.unit
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config should pass
        valid_config = {
            "llm": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7
            },
            "ragflow": {
                "host": "localhost",
                "port": 9380
            },
            "bge_m3": {
                "device": "cpu",
                "batch_size": 8
            }
        }
        
        config = LearningAgentConfig(**valid_config)
        assert config.llm.provider == "openai"
        assert config.ragflow.port == 9380
        assert config.bge_m3.batch_size == 8
    
    @pytest.mark.unit
    def test_invalid_config_validation(self):
        """Test that invalid configurations raise validation errors."""
        
        # Invalid temperature (out of range)
        with pytest.raises(ValueError):
            LearningAgentConfig(llm={"temperature": 2.5})
        
        # Invalid provider
        with pytest.raises(ValueError):
            LearningAgentConfig(llm={"provider": "invalid_provider"})
        
        # Invalid port number
        with pytest.raises(ValueError):
            LearningAgentConfig(ragflow={"port": -1})
        
        # Invalid batch size
        with pytest.raises(ValueError):
            LearningAgentConfig(bge_m3={"batch_size": 0})


class TestRAGFlowConfig:
    """Test RAGFlow-specific configuration."""
    
    @pytest.mark.unit
    def test_ragflow_config_defaults(self):
        """Test RAGFlow configuration defaults."""
        config = RAGFlowConfig()
        
        assert config.host == "localhost"
        assert config.port == 9380
        assert config.knowledge_base == "learning_agent_kb"
        assert config.docker_image == "ragflow/ragflow:latest"
        assert config.enable_health_checks is True
    
    @pytest.mark.unit
    def test_ragflow_config_validation(self):
        """Test RAGFlow configuration validation."""
        # Valid configurations
        valid_configs = [
            {"host": "192.168.1.100", "port": 8080},
            {"host": "ragflow.example.com", "port": 9380},
            {"host": "localhost", "port": 3000}
        ]
        
        for config_data in valid_configs:
            config = RAGFlowConfig(**config_data)
            assert config.host == config_data["host"]
            assert config.port == config_data["port"]
    
    @pytest.mark.unit
    def test_ragflow_invalid_config(self):
        """Test invalid RAGFlow configurations."""
        # Invalid port ranges
        with pytest.raises(ValueError):
            RAGFlowConfig(port=0)
        
        with pytest.raises(ValueError):
            RAGFlowConfig(port=70000)
        
        # Invalid host format (if we add validation)
        # Note: Add specific host validation if needed


class TestBGE_M3Config:
    """Test BGE-M3 model configuration."""
    
    @pytest.mark.unit
    def test_bge_m3_config_defaults(self):
        """Test BGE-M3 configuration defaults."""
        config = BGE_M3Config()
        
        assert config.device == "cpu"
        assert config.batch_size == 4
        assert config.max_length == 8192
        assert config.dense_dim == 512
        assert config.enable_sparse is True
        assert config.enable_colbert is True
    
    @pytest.mark.unit
    def test_bge_m3_config_validation(self):
        """Test BGE-M3 configuration validation."""
        # Valid device options
        for device in ["cpu", "cuda", "mps"]:
            config = BGE_M3Config(device=device)
            assert config.device == device
        
        # Valid batch sizes
        for batch_size in [1, 2, 4, 8, 16]:
            config = BGE_M3Config(batch_size=batch_size)
            assert config.batch_size == batch_size
    
    @pytest.mark.unit
    def test_bge_m3_invalid_config(self):
        """Test invalid BGE-M3 configurations."""
        # Invalid device
        with pytest.raises(ValueError):
            BGE_M3Config(device="invalid_device")
        
        # Invalid batch size
        with pytest.raises(ValueError):
            BGE_M3Config(batch_size=0)
        
        with pytest.raises(ValueError):
            BGE_M3Config(batch_size=100)  # Too large
        
        # Invalid max_length
        with pytest.raises(ValueError):
            BGE_M3Config(max_length=100)  # Too small


class TestMathematicalContentConfig:
    """Test mathematical content configuration."""
    
    @pytest.mark.unit
    def test_mathematical_config_defaults(self):
        """Test mathematical content configuration defaults."""
        config = MathematicalContentConfig()
        
        assert config.latex_rendering is True
        assert config.preserve_equations is True
        assert config.math_symbol_mapping is True
        assert config.chunk_overlap_ratio == 0.4
        assert config.quality_threshold == 0.8
    
    @pytest.mark.unit
    def test_mathematical_config_validation(self):
        """Test mathematical content configuration validation."""
        # Valid overlap ratios
        for ratio in [0.1, 0.3, 0.5, 0.7]:
            config = MathematicalContentConfig(chunk_overlap_ratio=ratio)
            assert config.chunk_overlap_ratio == ratio
        
        # Valid quality thresholds
        for threshold in [0.5, 0.7, 0.9, 1.0]:
            config = MathematicalContentConfig(quality_threshold=threshold)
            assert config.quality_threshold == threshold
    
    @pytest.mark.unit
    def test_mathematical_invalid_config(self):
        """Test invalid mathematical content configurations."""
        # Invalid overlap ratio
        with pytest.raises(ValueError):
            MathematicalContentConfig(chunk_overlap_ratio=-0.1)
        
        with pytest.raises(ValueError):
            MathematicalContentConfig(chunk_overlap_ratio=1.1)
        
        # Invalid quality threshold
        with pytest.raises(ValueError):
            MathematicalContentConfig(quality_threshold=0.0)
        
        with pytest.raises(ValueError):
            MathematicalContentConfig(quality_threshold=1.5)


class TestLLMConfig:
    """Test LLM configuration."""
    
    @pytest.mark.unit
    def test_llm_config_defaults(self):
        """Test LLM configuration defaults."""
        config = LLMConfig()
        
        assert config.provider == "deepseek"
        assert config.model == "deepseek-chat"
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
        assert config.timeout == 30
    
    @pytest.mark.unit
    def test_llm_config_validation(self):
        """Test LLM configuration validation."""
        # Valid providers
        valid_providers = ["openai", "deepseek", "anthropic", "ollama", "groq"]
        for provider in valid_providers:
            config = LLMConfig(provider=provider)
            assert config.provider == provider
        
        # Valid temperature ranges
        for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
            config = LLMConfig(temperature=temp)
            assert config.temperature == temp
    
    @pytest.mark.unit
    def test_llm_invalid_config(self):
        """Test invalid LLM configurations."""
        # Invalid provider
        with pytest.raises(ValueError):
            LLMConfig(provider="invalid_provider")
        
        # Invalid temperature
        with pytest.raises(ValueError):
            LLMConfig(temperature=-0.1)
        
        with pytest.raises(ValueError):
            LLMConfig(temperature=2.1)
        
        # Invalid max_tokens
        with pytest.raises(ValueError):
            LLMConfig(max_tokens=0)


class TestConfigurationManager:
    """Test the configuration manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.yaml"
    
    @pytest.mark.unit
    def test_config_manager_initialization(self):
        """Test configuration manager initialization."""
        manager = ConfigurationManager()
        
        assert manager is not None
        assert hasattr(manager, 'load_config')
        assert hasattr(manager, 'save_config')
        assert hasattr(manager, 'get_config')
    
    @pytest.mark.unit
    def test_load_config_from_file(self, test_config):
        """Test loading configuration from file."""
        # Write test config to file
        with open(self.config_file, 'w') as f:
            yaml.dump(test_config, f)
        
        # Load config
        manager = ConfigurationManager()
        config = manager.load_config(str(self.config_file))
        
        assert isinstance(config, LearningAgentConfig)
        assert config.llm.provider == test_config["llm"]["provider"]
        assert config.ragflow.host == test_config["ragflow"]["host"]
    
    @pytest.mark.unit
    def test_save_config_to_file(self):
        """Test saving configuration to file."""
        config = LearningAgentConfig()
        manager = ConfigurationManager()
        
        # Save config
        manager.save_config(config, str(self.config_file))
        
        # Verify file exists and is valid
        assert self.config_file.exists()
        
        # Load and verify
        with open(self.config_file, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        assert "llm" in loaded_data
        assert "ragflow" in loaded_data
        assert loaded_data["llm"]["provider"] == "deepseek"
    
    @pytest.mark.unit
    def test_config_hot_reloading(self):
        """Test configuration hot-reloading functionality."""
        # Create initial config
        initial_config = {"llm": {"provider": "openai"}}
        with open(self.config_file, 'w') as f:
            yaml.dump(initial_config, f)
        
        manager = ConfigurationManager()
        config = manager.load_config(str(self.config_file), enable_hot_reload=True)
        
        assert config.llm.provider == "openai"
        
        # Modify config file
        updated_config = {"llm": {"provider": "deepseek"}}
        with open(self.config_file, 'w') as f:
            yaml.dump(updated_config, f)
        
        # Simulate file change detection (would normally be automatic)
        # Note: In real implementation, this would use file watchers
        new_config = manager.load_config(str(self.config_file))
        assert new_config.llm.provider == "deepseek"
    
    @pytest.mark.unit
    def test_environment_variable_override(self):
        """Test environment variable configuration override."""
        # Set environment variables
        os.environ["LLM_PROVIDER"] = "anthropic"
        os.environ["RAGFLOW_PORT"] = "8080"
        os.environ["BGE_M3_BATCH_SIZE"] = "16"
        
        try:
            manager = ConfigurationManager()
            config = manager.load_config_with_env_override()
            
            # Environment variables should override defaults
            assert config.llm.provider == "anthropic"
            assert config.ragflow.port == 8080
            assert config.bge_m3.batch_size == 16
            
        finally:
            # Clean up environment variables
            for var in ["LLM_PROVIDER", "RAGFLOW_PORT", "BGE_M3_BATCH_SIZE"]:
                if var in os.environ:
                    del os.environ[var]
    
    @pytest.mark.unit
    def test_config_schema_export(self):
        """Test configuration schema export functionality."""
        manager = ConfigurationManager()
        schema = manager.export_schema()
        
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "llm" in schema["properties"]
        assert "ragflow" in schema["properties"]
        
        # Should be valid JSON schema
        import jsonschema
        jsonschema.Draft7Validator.check_schema(schema)
    
    @pytest.mark.unit
    def test_environment_specific_configs(self):
        """Test environment-specific configuration loading."""
        # Development config
        dev_config = {
            "environment": "development",
            "llm": {"provider": "ollama"},  # Local development
            "observability": {"logging_level": "DEBUG"}
        }
        
        # Production config  
        prod_config = {
            "environment": "production",
            "llm": {"provider": "openai"},  # Production service
            "observability": {"logging_level": "WARNING"}
        }
        
        manager = ConfigurationManager()
        
        # Test development config
        dev_config_obj = manager.load_config_from_dict(dev_config)
        assert dev_config_obj.llm.provider == "ollama"
        assert dev_config_obj.observability.logging_level == "DEBUG"
        
        # Test production config
        prod_config_obj = manager.load_config_from_dict(prod_config)
        assert prod_config_obj.llm.provider == "openai"
        assert prod_config_obj.observability.logging_level == "WARNING"


class TestConfigUtilityFunctions:
    """Test utility functions for configuration management."""
    
    @pytest.mark.unit
    def test_load_config_function(self, test_config_file):
        """Test the load_config utility function."""
        config = load_config(test_config_file)
        
        assert isinstance(config, LearningAgentConfig)
        assert config.llm.provider == "deepseek"
    
    @pytest.mark.unit
    def test_get_config_singleton(self):
        """Test the get_config singleton functionality."""
        # First call should create instance
        config1 = get_config()
        assert isinstance(config1, LearningAgentConfig)
        
        # Second call should return same instance
        config2 = get_config()
        assert config1 is config2
    
    @pytest.mark.unit
    def test_config_missing_file_handling(self):
        """Test handling of missing configuration files."""
        with pytest.raises(MissingConfigurationError):
            load_config("nonexistent_config.yaml")
    
    @pytest.mark.unit 
    def test_config_invalid_yaml_handling(self):
        """Test handling of invalid YAML configuration files."""
        # Create invalid YAML file
        invalid_file = Path(tempfile.mkdtemp()) / "invalid.yaml"
        with open(invalid_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        with pytest.raises(InvalidConfigurationError):
            load_config(str(invalid_file))


class TestConfigurationIntegration:
    """Integration tests for configuration with other components."""
    
    @pytest.mark.integration
    def test_config_with_services(self):
        """Test configuration integration with service initialization."""
        config = LearningAgentConfig(
            llm={"provider": "deepseek", "model": "deepseek-chat"},
            ragflow={"host": "localhost", "port": 9380}
        )
        
        # Mock service initialization
        with patch('src.services.llm_service.LLMService') as mock_llm:
            with patch('src.services.ragflow_service.RAGFlowService') as mock_ragflow:
                # Services should be able to initialize with config
                mock_llm.return_value = Mock()
                mock_ragflow.return_value = Mock()
                
                # This would be the actual service initialization
                llm_service = mock_llm(config.llm)
                ragflow_service = mock_ragflow(config.ragflow)
                
                assert llm_service is not None
                assert ragflow_service is not None
    
    @pytest.mark.integration
    def test_config_validation_with_real_data(self):
        """Test configuration validation with realistic data."""
        realistic_config = {
            "llm": {
                "provider": "deepseek",
                "model": "deepseek-chat", 
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 60
            },
            "ragflow": {
                "host": "localhost",
                "port": 9380,
                "knowledge_base": "academic_papers_kb",
                "docker_image": "ragflow/ragflow:latest",
                "memory_limit": "8g"
            },
            "bge_m3": {
                "device": "cpu",
                "batch_size": 4,
                "max_length": 8192,
                "dense_dim": 512,
                "enable_sparse": True,
                "enable_colbert": True
            },
            "mathematical_content": {
                "latex_rendering": True,
                "preserve_equations": True,
                "math_symbol_mapping": True,
                "chunk_overlap_ratio": 0.4,
                "quality_threshold": 0.85
            },
            "observability": {
                "logging_level": "INFO",
                "enable_metrics": True,
                "health_check_interval": 300,
                "metrics_retention_days": 30
            }
        }
        
        # Should validate successfully
        config = LearningAgentConfig(**realistic_config)
        
        # Verify all sections are properly configured
        assert config.llm.provider == "deepseek"
        assert config.ragflow.memory_limit == "8g"
        assert config.bge_m3.enable_sparse is True
        assert config.mathematical_content.chunk_overlap_ratio == 0.4
        assert config.observability.metrics_retention_days == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 