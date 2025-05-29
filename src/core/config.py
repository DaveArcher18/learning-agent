"""
Enhanced configuration management for the Learning Agent.

Provides comprehensive configuration loading and management with Pydantic validation,
environment-specific configurations, hot-reloading, and schema documentation.
Supports RAGFlow integration, BGE-M3 embedding model, and mathematical content processing.
"""

import os
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Literal
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# Enhanced imports for validation and type safety
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError as PydanticValidationError
from rich import print as rprint

# Import our type definitions
from .types import (
    ConfigDict, ConfigValue, LLMProvider, LogLevel, 
    RAGFlowConfigDict, BGE_M3ConfigDict, MathematicalContentConfigDict
)

logger = logging.getLogger(__name__)


# =============================================================================
# Environment Configuration
# =============================================================================

class Environment(Enum):
    """Supported environment configurations."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


# =============================================================================
# Pydantic Configuration Models
# =============================================================================

class LLMProviderConfig(BaseModel):
    """Configuration for individual LLM providers."""
    api_key: Optional[str] = Field(default=None, description="API key for the provider")
    base_url: Optional[str] = Field(default=None, description="Custom base URL")
    timeout: Optional[int] = Field(default=30, description="Request timeout in seconds")


class LLMProvidersConfig(BaseModel):
    """Configuration for all LLM providers."""
    openai: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    openrouter: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    deepseek: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    anthropic: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    groq: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    ollama: LLMProviderConfig = Field(default_factory=LLMProviderConfig)


class RAGFlowConfig(BaseModel):
    """Validated RAGFlow service configuration."""
    host: str = Field(default="localhost", description="RAGFlow service host")
    port: int = Field(default=9380, ge=1, le=65535, description="RAGFlow service port")
    docker_service: str = Field(default="ragflow", description="Docker service name")
    knowledge_base: str = Field(default="mathematical_kb", description="Knowledge base name")
    enable_citations: bool = Field(default=True, description="Enable automatic citations")
    enable_layout_parsing: bool = Field(default=True, description="Enable layout-aware parsing")
    api: Dict[str, Any] = Field(default_factory=dict, description="API configuration")
    
    @field_validator('host')
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host format."""
        if not v or not isinstance(v, str):
            raise ValueError("Host must be a non-empty string")
        return v.strip()
    
    @field_validator('knowledge_base')
    @classmethod
    def validate_knowledge_base(cls, v: str) -> str:
        """Validate knowledge base name."""
        if not v or not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Knowledge base name must be alphanumeric with underscores/hyphens")
        return v.lower()


class BGE_M3Config(BaseModel):
    """Validated BGE-M3 embedding model configuration."""
    model_name: str = Field(default="BAAI/bge-m3", description="BGE-M3 model identifier")
    device: str = Field(default="cpu", description="Device for inference (cpu/cuda)")
    max_length: int = Field(default=8192, ge=512, le=8192, description="Maximum token length")
    batch_size: int = Field(default=4, ge=1, le=32, description="Batch size for processing")
    dense_dim: int = Field(default=512, ge=128, le=1024, description="Dense embedding dimension")
    enable_sparse: bool = Field(default=True, description="Enable sparse retrieval")
    enable_colbert: bool = Field(default=True, description="Enable ColBERT reranking")
    cache_embeddings: bool = Field(default=True, description="Cache embeddings for performance")
    
    @field_validator('device')
    @classmethod
    def validate_device(cls, v: str) -> str:
        """Validate device setting."""
        valid_devices = {"cpu", "cuda", "mps"}
        if v.lower() not in valid_devices:
            raise ValueError(f"Device must be one of {valid_devices}")
        return v.lower()
    
    @field_validator('model_name')
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate model name format."""
        if not v or "/" not in v:
            raise ValueError("Model name must be in format 'organization/model'")
        return v


class MathematicalContentConfig(BaseModel):
    """Validated mathematical content processing configuration."""
    chunk_size: int = Field(default=1000, ge=100, le=4000, description="Chunk size in tokens")
    chunk_overlap_ratio: float = Field(default=0.4, ge=0.0, le=0.8, description="Chunk overlap ratio")
    preserve_latex: bool = Field(default=True, description="Preserve LaTeX formatting")
    theorem_classification: bool = Field(default=True, description="Enable theorem classification")
    proof_chain_tracking: bool = Field(default=True, description="Track proof dependencies")
    citation_granularity: Literal["sentence", "paragraph", "document"] = Field(
        default="sentence", description="Citation granularity level"
    )
    
    @field_validator('chunk_overlap_ratio')
    @classmethod
    def validate_overlap_ratio(cls, v: float) -> float:
        """Validate overlap ratio is reasonable."""
        if v < 0.0 or v > 0.8:
            raise ValueError("Chunk overlap ratio must be between 0.0 and 0.8")
        return v


class LLMConfig(BaseModel):
    """Validated LLM configuration."""
    model: str = Field(default="qwen3:4b", description="Default model name")
    model_provider: LLMProvider = Field(default=LLMProvider.OLLAMA, description="LLM provider")
    openrouter_model: str = Field(default="deepseek/deepseek-prover-v2:free", description="OpenRouter model")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="Generation temperature")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="Maximum tokens to generate")
    providers: LLMProvidersConfig = Field(default_factory=LLMProvidersConfig, description="Provider configurations")
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate temperature range."""
        if v < 0.0 or v > 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v


class RAGConfig(BaseModel):
    """Validated RAG pipeline configuration."""
    top_k: int = Field(default=50, ge=1, le=100, description="Initial retrieval count")
    final_k: int = Field(default=15, ge=1, le=50, description="Final selection count")
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Similarity threshold")
    enable_reranking: bool = Field(default=True, description="Enable result reranking")
    enable_graphrag: bool = Field(default=True, description="Enable GraphRAG")
    enable_raptor: bool = Field(default=True, description="Enable RAPTOR")
    
    @field_validator('final_k')
    @classmethod
    def validate_final_k(cls, v: int) -> int:
        """Validate final_k is reasonable (cross-field validation handled in model_validator)."""
        return v


class UIConfig(BaseModel):
    """Validated UI configuration."""
    use_markdown_rendering: bool = Field(default=True, description="Enable markdown rendering")
    enable_latex_processing: bool = Field(default=True, description="Enable LaTeX processing")
    use_advanced_latex_rendering: bool = Field(default=True, description="Advanced LaTeX rendering")
    code_highlighting: bool = Field(default=True, description="Enable code highlighting")
    enable_rich_console: bool = Field(default=True, description="Enable rich console")


class PerformanceConfig(BaseModel):
    """Validated performance configuration."""
    target_response_time: int = Field(default=10, ge=1, le=60, description="Target response time in seconds")
    enable_batch_processing: bool = Field(default=True, description="Enable batch processing")
    memory_optimization: bool = Field(default=True, description="Enable memory optimization")
    cpu_optimization: bool = Field(default=True, description="Enable CPU optimization")


class ObservabilityConfig(BaseModel):
    """Validated observability configuration."""
    enable_structured_logging: bool = Field(default=True, description="Enable structured logging")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    enable_health_checks: bool = Field(default=True, description="Enable health monitoring")


class DocumentsConfig(BaseModel):
    """Validated documents processing configuration."""
    path: str = Field(default="data/documents", description="Path to documents directory")
    chunk_size: int = Field(default=4000, ge=100, le=8000, description="Chunk size in tokens")
    chunk_overlap: int = Field(default=500, ge=0, le=2000, description="Chunk overlap in tokens")
    preserve_boundaries: bool = Field(default=True, description="Preserve logical boundaries when chunking")


class RetrievalConfig(BaseModel):
    """Validated retrieval configuration."""
    max_chunks: int = Field(default=5, ge=1, le=20, description="Maximum chunks to retrieve")
    enable_fallback: bool = Field(default=True, description="Enable retrieval fallback mechanisms")


class LearningAgentConfig(BaseModel):
    """Main configuration model with comprehensive validation."""
    
    # Environment settings
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Runtime environment")
    
    # Core settings
    use_memory: bool = Field(default=True, description="Enable conversation memory")
    use_web_fallback: bool = Field(default=True, description="Enable web search fallback")
    web_results: int = Field(default=3, ge=1, le=10, description="Number of web results")
    
    # Prompt settings
    prompt_template: str = Field(
        default=(
            "Answer the question based on the following context with automatic citations. "
            "Preserve mathematical notation and provide granular source attribution.\n\n"
            "Context:\n{context}\n\nQuestion: {question}\n"
        ),
        description="Prompt template for generation"
    )
    
    # Component configurations
    llm: LLMConfig = Field(default_factory=LLMConfig, description="LLM configuration")
    ragflow: RAGFlowConfig = Field(default_factory=RAGFlowConfig, description="RAGFlow configuration")
    bge_m3: BGE_M3Config = Field(default_factory=BGE_M3Config, description="BGE-M3 configuration")
    mathematical_content: MathematicalContentConfig = Field(
        default_factory=MathematicalContentConfig, description="Mathematical content configuration"
    )
    rag: RAGConfig = Field(default_factory=RAGConfig, description="RAG pipeline configuration")
    ui: UIConfig = Field(default_factory=UIConfig, description="UI configuration")
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig, description="Performance configuration")
    observability: ObservabilityConfig = Field(
        default_factory=ObservabilityConfig, description="Observability configuration"
    )
    documents: DocumentsConfig = Field(default_factory=DocumentsConfig, description="Documents configuration")
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig, description="Retrieval configuration")
    
    # Legacy settings (for migration)
    legacy_qdrant: Optional[Dict[str, Any]] = Field(default=None, description="Legacy Qdrant settings")
    
    @model_validator(mode='before')
    @classmethod
    def validate_configuration_consistency(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate cross-field consistency."""
        # Ensure BGE-M3 device compatibility
        if isinstance(values, dict):
            bge_m3 = values.get('bge_m3', {})
            if isinstance(bge_m3, dict):
                device = bge_m3.get('device', 'cpu')
                if device == 'cuda':
                    # Log warning for M1 Mac users
                    logger.warning("CUDA device specified on M1 Mac - falling back to CPU")
                    bge_m3['device'] = 'cpu'
            
            # Validate RAG configuration consistency
            rag = values.get('rag', {})
            if isinstance(rag, dict):
                top_k = rag.get('top_k', 50)
                final_k = rag.get('final_k', 15)
                if final_k > top_k:
                    rag['final_k'] = top_k
        
        return values
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "str_strip_whitespace": True,
        "frozen": False,  # Allow updates through proper methods
    }


# =============================================================================
# Configuration Manager
# =============================================================================

class ConfigManager:
    """
    Enhanced configuration manager with Pydantic validation and environment integration.
    
    Handles configuration loading from YAML/JSON files, environment variable integration,
    hot-reloading, and comprehensive validation.
    """
    
    def __init__(
        self, 
        config_path: Optional[str] = None,
        environment: Optional[Environment] = None,
        auto_reload: bool = False
    ) -> None:
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (defaults to config.yaml)
            environment: Runtime environment (auto-detected if not provided)
            auto_reload: Enable automatic configuration reloading
        """
        self.config_path = Path(config_path or "config.yaml")
        self.environment = environment or Environment.DEVELOPMENT
        self.auto_reload = auto_reload
        
        # Internal state
        self._config: Optional[LearningAgentConfig] = None
        self._last_modified: Optional[datetime] = None
        self._watchers: List[callable] = []
        
        # Load initial configuration
        self.reload_config()
        
        logger.info(f"ConfigManager initialized with {self.config_path}")
    
    def reload_config(self) -> None:
        """Reload configuration from file and environment variables."""
        try:
            # Load base configuration from file
            raw_config = self._load_raw_config()
            
            # Apply environment-specific overrides
            raw_config = self._apply_environment_overrides(raw_config)
            
            # Integrate environment variables (API keys, etc.)
            raw_config = self._integrate_environment_variables(raw_config)
            
            # Create validated configuration
            self._config = LearningAgentConfig(**raw_config)
            
            # Update modification time
            if self.config_path.exists():
                self._last_modified = datetime.fromtimestamp(self.config_path.stat().st_mtime)
            
            # Notify watchers
            self._notify_watchers()
            
            logger.info("Configuration reloaded successfully")
            
        except PydanticValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            rprint(f"[red]❌ Configuration validation failed: {e}[/red]")
            raise
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")
            rprint(f"[red]❌ Failed to reload configuration: {e}[/red]")
            raise
    
    def _load_raw_config(self) -> Dict[str, Any]:
        """Load raw configuration from file."""
        if not self.config_path.exists():
            rprint(f"[yellow]⚠️ Config file '{self.config_path}' not found. Using defaults.[/yellow]")
            return {}
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                if self.config_path.suffix.lower() == '.json':
                    return json.load(f)
                else:
                    return yaml.safe_load(f) or {}
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            rprint(f"[red]❌ Failed to parse config file: {e}[/red]")
            return {}
    
    def _apply_environment_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment-specific configuration overrides."""
        config = config.copy()
        config['environment'] = self.environment.value
        
        # Environment-specific overrides
        if self.environment == Environment.PRODUCTION:
            config.setdefault('observability', {})['log_level'] = LogLevel.WARNING.value
            config.setdefault('performance', {})['target_response_time'] = 15
            config.setdefault('rag', {})['top_k'] = 30  # Faster retrieval in prod
            
        elif self.environment == Environment.DEVELOPMENT:
            config.setdefault('observability', {})['log_level'] = LogLevel.DEBUG.value
            config.setdefault('performance', {})['target_response_time'] = 30
            
        elif self.environment == Environment.TESTING:
            config.setdefault('observability', {})['log_level'] = LogLevel.ERROR.value
            config.setdefault('performance', {})['target_response_time'] = 5
            config['use_memory'] = False  # No memory in tests
        
        return config
    
    def _integrate_environment_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate environment variables into configuration."""
        config = config.copy()
        
        # Ensure nested structures exist
        config.setdefault('llm', {}).setdefault('providers', {})
        config.setdefault('ragflow', {}).setdefault('api', {})
        
        # API Key mappings from environment variables
        api_key_mappings = {
            'OPENAI_API_KEY': ['llm', 'providers', 'openai', 'api_key'],
            'OPENAI_API_KEY': ['llm', 'providers', 'openrouter', 'api_key'],  # OpenRouter uses OpenAI key
            'DEEPSEEK_API_KEY': ['llm', 'providers', 'deepseek', 'api_key'],
            'ANTHROPIC_API_KEY': ['llm', 'providers', 'anthropic', 'api_key'],
            'GROQ_API_KEY': ['llm', 'providers', 'groq', 'api_key'],
            'RAGFLOW_API_KEY': ['ragflow', 'api', 'key'],
        }
        
        # Load API keys from environment
        for env_var, config_path in api_key_mappings.items():
            api_key = os.getenv(env_var)
            if api_key:
                # Navigate to the correct nested location
                current = config
                for key in config_path[:-1]:
                    current = current.setdefault(key, {})
                current[config_path[-1]] = api_key
                logger.debug(f"Loaded {env_var} from environment")
        
        # Other environment variable integrations
        env_mappings = {
            'LLM_PROVIDER': ['llm', 'model_provider'],
            'RAGFLOW_HOST': ['ragflow', 'host'],
            'RAGFLOW_PORT': ['ragflow', 'port'],
            'BGE_M3_DEVICE': ['bge_m3', 'device'],
            'BGE_M3_BATCH_SIZE': ['bge_m3', 'batch_size'],
            'LOG_LEVEL': ['observability', 'log_level'],
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                # Type conversion
                if config_path[-1] in ['port', 'batch_size']:
                    try:
                        env_value = int(env_value)
                    except ValueError:
                        logger.warning(f"Invalid integer value for {env_var}: {env_value}")
                        continue
                elif config_path[-1] in ['log_level']:
                    env_value = env_value.upper()
                
                # Set the value
                current = config
                for key in config_path[:-1]:
                    current = current.setdefault(key, {})
                current[config_path[-1]] = env_value
                logger.debug(f"Applied {env_var}={env_value} to configuration")
        
        return config
    
    def check_for_updates(self) -> bool:
        """Check if configuration file has been updated."""
        if not self.config_path.exists() or not self._last_modified:
            return False
        
        current_modified = datetime.fromtimestamp(self.config_path.stat().st_mtime)
        return current_modified > self._last_modified
    
    def add_watcher(self, callback: callable) -> None:
        """Add a configuration change watcher."""
        self._watchers.append(callback)
    
    def remove_watcher(self, callback: callable) -> None:
        """Remove a configuration change watcher."""
        if callback in self._watchers:
            self._watchers.remove(callback)
    
    def _notify_watchers(self) -> None:
        """Notify all configuration change watchers."""
        for watcher in self._watchers:
            try:
                watcher(self._config)
            except Exception as e:
                rprint(f"[red]❌ Configuration watcher error: {e}[/red]")
    
    @property
    def config(self) -> LearningAgentConfig:
        """Get current configuration, checking for updates if auto-reload is enabled."""
        if self.auto_reload and self.check_for_updates():
            self.reload_config()
        
        if self._config is None:
            raise RuntimeError("Configuration not loaded")
        
        return self._config
    
    # Convenience property accessors
    @property
    def ragflow(self) -> RAGFlowConfig:
        """Get RAGFlow configuration."""
        return self.config.ragflow
    
    @property
    def bge_m3(self) -> BGE_M3Config:
        """Get BGE-M3 configuration."""
        return self.config.bge_m3
    
    @property
    def mathematical_content(self) -> MathematicalContentConfig:
        """Get mathematical content configuration."""
        return self.config.mathematical_content
    
    @property
    def llm(self) -> LLMConfig:
        """Get LLM configuration."""
        return self.config.llm
    
    @property
    def rag(self) -> RAGConfig:
        """Get RAG configuration."""
        return self.config.rag
    
    # Backward compatibility methods
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key (backward compatibility)."""
        try:
            keys = key.split('.')
            value = self.config.dict()
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception:
            return default
    
    def update(self, key: str, value: Any) -> None:
        """Update configuration value (creates new config instance)."""
        config_dict = self.config.dict()
        keys = key.split('.')
        
        # Navigate to the parent of the target key
        current = config_dict
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        
        # Recreate config with validation
        try:
            self._config = LearningAgentConfig(**config_dict)
            self._notify_watchers()
        except PydanticValidationError as e:
            rprint(f"[red]❌ Configuration update failed validation: {e}[/red]")
            raise
    
    def save_config(self, path: Optional[Path] = None) -> None:
        """Save current configuration to file."""
        save_path = path or self.config_path
        
        config_dict = self.config.dict()
        # Remove computed/runtime fields
        config_dict.pop('environment', None)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if save_path.suffix.lower() == '.json':
                    json.dump(config_dict, f, indent=2, default=str)
                else:
                    yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            
            rprint(f"[green]✅ Configuration saved to {save_path}[/green]")
            
        except Exception as e:
            rprint(f"[red]❌ Failed to save configuration: {e}[/red]")
            raise
    
    def validate_config(self) -> bool:
        """Validate current configuration."""
        try:
            # Re-validate current configuration
            LearningAgentConfig(**self.config.dict())
            return True
        except PydanticValidationError:
            return False
    
    def get_schema(self) -> Dict[str, Any]:
        """Get configuration schema for documentation."""
        return LearningAgentConfig.schema()
    
    def export_schema_docs(self, output_path: Optional[Path] = None) -> None:
        """Export configuration schema documentation."""
        schema = self.get_schema()
        output_path = output_path or Path("config-schema.json")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2)
            
            rprint(f"[green]✅ Configuration schema exported to {output_path}[/green]")
            
        except Exception as e:
            rprint(f"[red]❌ Failed to export schema: {e}[/red]")
            raise


# =============================================================================
# Global Configuration Instance
# =============================================================================

# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(
    config_path: Optional[str] = None,
    environment: Optional[Environment] = None,
    auto_reload: bool = False
) -> ConfigManager:
    """Get or create global configuration manager instance."""
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(
            config_path=config_path,
            environment=environment,
            auto_reload=auto_reload
        )
    
    return _config_manager


def get_config() -> LearningAgentConfig:
    """Get current configuration (convenience function)."""
    return get_config_manager().config


def load_config(config_path: str = None) -> LearningAgentConfig:
    """Load configuration from file (backward compatibility function)."""
    manager = get_config_manager(config_path=config_path)
    return manager.config


# Backward compatibility
ConfigManager.DEFAULT_CONFIG = {
    "model": "qwen3:4b",
    "model_provider": "ollama",
    "temperature": 0.3,
    "use_memory": True,
    # ... (legacy structure for migration)
}

# Alias for backward compatibility with tests
ConfigurationManager = ConfigManager


if __name__ == "__main__":
    """Test suite for configuration management."""
    rprint("[bold cyan]🧪 Running Enhanced ConfigManager Test Suite...[/bold cyan]")
    
    # Test 1: Basic functionality
    rprint("\n[b]Test 1: Basic functionality[/b]")
    manager = ConfigManager()
    rprint("Model:", manager.get("model"))
    rprint("RAGFlow host:", manager.get("ragflow.host"))
    rprint("BGE-M3 device:", manager.get("bge_m3.device"))
    
    # Test 2: Typed configurations
    rprint("\n[b]Test 2: Typed configurations[/b]")
    ragflow_config = manager.get_ragflow_config()
    rprint(f"RAGFlow config: {ragflow_config}")
    
    bge_m3_config = manager.get_bge_m3_config()
    rprint(f"BGE-M3 config: {bge_m3_config}")
    
    # Test 3: Updates with dot notation
    rprint("\n[b]Test 3: Updates with dot notation[/b]")
    manager.update("ragflow.port", 9999)
    rprint("Updated RAGFlow port:", manager.get("ragflow.port"))
    
    # Test 4: Configuration validation
    rprint("\n[b]Test 4: Configuration validation[/b]")
    is_valid = manager.validate_config()
    rprint(f"Configuration valid: {is_valid}")
    
    rprint("\n[bold cyan]✅ Enhanced ConfigManager Test Suite Complete.[/bold cyan]") 