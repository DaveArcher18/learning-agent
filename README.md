# Learning Agent: Simple RAG Assistant with Memory

A streamlined, modular Retrieval-Augmented Generation (RAG) system designed with principles of **maintainability**, **modularity**, **simplicity**, and **observability**.

## 🏗️ Architecture Overview

The Learning Agent follows a clean, modular architecture with clear separation of concerns:

```
learning-agent/
├── config.yaml              # Single source of truth for all configuration
├── .env                     # API keys and sensitive environment variables  
├── learning_agent.py        # Main entry point
├── src/
│   ├── core/
│   │   ├── simple_config.py # Centralized configuration management
│   │   └── agent.py         # Main agent orchestration
│   ├── services/            # Core business logic services
│   │   ├── llm_service.py   # Language model interactions
│   │   ├── memory_service.py# Conversation memory management
│   │   └── ragflow_service.py# Document retrieval and processing
│   ├── ui/                  # User interface components
│   │   ├── console_interface.py
│   │   └── commands/        # Interactive commands
│   ├── text_processing/     # Text processing and rendering
│   └── observability/       # Logging and monitoring
└── tests/                   # Comprehensive test suite
```

### Design Principles

- **Maintainability**: Clear, self-documenting code with consistent patterns
- **Modularity**: Small, focused components with single responsibilities
- **Simplicity**: Straightforward solutions that solve the problem effectively
- **Observability**: Built-in logging and monitoring for runtime visibility

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration

The system uses **`config.yaml`** as the single source of truth for all settings:

```yaml
# Core settings
use_memory: true
use_web_fallback: true
web_results: 3

# LLM Configuration  
llm:
  model: "qwen3:4b"
  model_provider: "ollama"  # Options: ollama, openrouter, deepseek, openai, anthropic, groq
  temperature: 0.3

# RAGFlow Configuration (Advanced RAG)
ragflow:
  host: "localhost"
  port: 9380
  knowledge_base: "mathematical_kb"

# UI Configuration
ui:
  use_markdown_rendering: true
  enable_latex_processing: true
  code_highlighting: true
```

### 3. Environment Variables

Create a **`.env`** file for API keys (never commit this file):

```bash
# API Keys (only add what you need)
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GROQ_API_KEY=your_groq_key_here

# Optional environment overrides
LLM_PROVIDER=openrouter
RAGFLOW_HOST=localhost
```

The system automatically integrates these environment variables with the configuration from `config.yaml`.

### 4. Start the Agent

```bash
python learning_agent.py
```

## 💬 How to Interact with the Agent

### Basic Conversation

Simply type your questions and the agent will respond:

```
> What is machine learning?
> Explain quantum computing in simple terms
> How do neural networks work?
```

### Interactive Commands

Commands start with `:` and provide system control:

#### Memory Management
```bash
:memory on              # Enable conversation memory
:memory off             # Disable conversation memory  
:memory clear           # Clear conversation history
:memory show            # Show recent conversation history
:memory export chat.json # Export conversation to file
```

#### Provider Management
```bash
:provider               # Show current provider
:provider ollama        # Switch to local Ollama
:provider openrouter    # Switch to OpenRouter cloud service
:provider deepseek      # Switch to DeepSeek API
```

#### System Commands
```bash
:help                   # Show all available commands
:config                 # Show current configuration
:config get llm.model   # Get specific config value
:config set llm.temperature=0.7  # Set config value
:exit                   # Quit the application
```

#### Search and Retrieval
```bash
:search quantum theory  # Web search for information
:ragflow start         # Start RAGFlow service
:ragflow status        # Check RAGFlow service status
```

### Advanced Features

#### Markdown and LaTeX Support
The agent renders responses with rich formatting:
- **Bold** and *italic* text
- `code snippets` and code blocks
- Mathematical expressions: $E = mc^2$
- Lists and tables

#### Memory Persistence
Conversations are automatically saved and restored between sessions when memory is enabled.

#### Fallback Mechanisms
- If RAGFlow is unavailable, falls back to direct LLM
- If primary LLM fails, suggests switching providers
- Web search fallback for questions outside knowledge base

## 🔧 Configuration Management

### Centralized Configuration
All configuration is managed through `config.yaml`:

- **Single source of truth**: All settings in one place
- **Environment integration**: API keys from `.env` file
- **Runtime updates**: Change settings with `:config` commands
- **Validation**: Automatic validation of configuration values

### Configuration Hierarchy
1. **Base configuration**: `config.yaml`
2. **Environment overrides**: `.env` file variables
3. **Runtime updates**: `:config` commands

### Key Configuration Sections

#### LLM Settings
```yaml
llm:
  model: "qwen3:4b"
  model_provider: "ollama" 
  temperature: 0.3
  max_tokens: null
```

#### RAG Pipeline
```yaml
rag:
  top_k: 50
  final_k: 15
  similarity_threshold: 0.5
  enable_reranking: true
```

#### UI Preferences
```yaml
ui:
  use_markdown_rendering: true
  enable_latex_processing: true
  code_highlighting: true
```

## 🔍 Troubleshooting

### Configuration Issues
```bash
# Check current configuration
:config

# Validate configuration
python -c "from src.core.simple_config import get_config; get_config().validate_required_config()"

# Reset to defaults
cp config.yaml config.yaml.backup
# Edit config.yaml as needed
```

### API Key Issues
```bash
# Check if API key is loaded
:config get llm.providers.openai.api_key

# Common solutions:
# 1. Ensure .env file exists in project root
# 2. Check API key format (no extra spaces/quotes)
# 3. Verify API key permissions with provider
```

### Service Issues
```bash
# Check service status
:ragflow status

# Switch providers if one is down
:provider ollama        # Try local model
:provider openrouter    # Try cloud service
```

## 🧪 Development

### Running Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src
```

### Code Quality
The codebase follows strict quality guidelines:

- **Type hints**: All functions are fully typed
- **Documentation**: Comprehensive docstrings for all public interfaces
- **Error handling**: Graceful error handling with helpful messages
- **Logging**: Structured logging for observability
- **Testing**: Comprehensive unit and integration tests

### Architecture Compliance

Each component upholds the core principles:

- **Maintainability**: Self-documenting code with clear intent
- **Modularity**: Single responsibility components with well-defined interfaces
- **Simplicity**: Straightforward solutions without unnecessary complexity
- **Observability**: Built-in monitoring and diagnostic capabilities

## 📚 Advanced Usage

### Custom Configuration
Create environment-specific configs:
```bash
cp config.yaml config.dev.yaml
# Edit for development settings
python learning_agent.py  # Uses config.yaml by default
```

### Integration with External Services
The modular architecture makes it easy to integrate new services:

1. **Add service class** in `src/services/`
2. **Update configuration** in `config.yaml`
3. **Register service** in `agent.py`
4. **Add commands** in `src/ui/commands/`

### Performance Optimization
Configure for your use case:
```yaml
performance:
  target_response_time: 10
  enable_batch_processing: true
  memory_optimization: true
```

---

## 🎯 Design Goals Achieved

- **Simple Configuration**: Single `config.yaml` file controls everything
- **Clear Architecture**: Modular design with obvious component boundaries  
- **Easy Interaction**: Intuitive commands and helpful error messages
- **Observable Behavior**: Comprehensive logging and status reporting
- **Maintainable Code**: Clean, well-documented, testable implementation

The Learning Agent demonstrates how complex functionality can be delivered through simple, well-designed components that work together harmoniously.
