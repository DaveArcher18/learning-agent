# Learning Agent Architecture Documentation

## Overview

The Learning Agent has been completely refactored from a monolithic 1,272-line file into a **maintainable**, **modular**, **simple**, and **observable** system. This document describes the current architecture, design decisions, and component interactions.

## Guiding Principles

### Maintainability
- **Clear Intent**: Code is self-documenting with intention-revealing names
- **Single Responsibility**: Each component has one clear purpose
- **Predictable Behavior**: No hidden side-effects or magic

### Modularity
- **Cohesive Units**: Small, focused components that do one thing well
- **Minimal Interfaces**: Expose smallest public surface, hide internals
- **Loose Coupling**: Components can change independently

### Simplicity
- **Start Simple**: Simplest approach first, add complexity only when necessary
- **Explicit Logic**: Straight-line logic over clever shortcuts
- **No Premature Optimization**: Make it work, then make it fast if needed

### Observability
- **Built-in Visibility**: Code reveals runtime behavior and health
- **Structured Logging**: Consistent levels with meaningful context
- **Easy Diagnosis**: Clear error messages and traceable data flow

## Directory Structure

```
src/
├── main.py                     # Entry point with health checks
├── core/
│   ├── agent.py               # Simplified orchestration (~200 lines)
│   ├── config.py              # Pydantic configuration management
│   └── types.py               # Comprehensive type definitions
├── services/
│   ├── llm_service.py         # Multi-provider LLM management
│   ├── ragflow_service.py     # RAGFlow Docker & knowledge bases
│   ├── memory_service.py      # Conversation persistence
│   └── vector_service.py      # Legacy Qdrant support
├── rag/
│   ├── retrieval/
│   │   └── ragflow_client.py  # BGE-M3 retrieval & citations
│   └── models/
│       └── bge_m3_config.py   # M1 optimized configuration
├── text_processing/
│   ├── latex_renderer.py      # Mathematical expression display
│   └── markdown_renderer.py   # Rich console formatting
├── ui/
│   ├── console_interface.py   # User interaction handling
│   └── commands/              # Modular command system
│       ├── base.py           # Command infrastructure
│       ├── registry.py       # Command management
│       ├── system.py         # help, exit, config
│       ├── provider.py       # LLM provider switching
│       ├── memory.py         # Conversation management
│       ├── rag.py           # RAG operations
│       ├── knowledge.py     # Knowledge base management
│       └── metrics.py       # Performance monitoring
├── observability/
│   ├── logger.py            # Structured logging with correlation
│   ├── metrics.py           # Performance tracking
│   └── health.py            # Service monitoring & recovery
└── utils/
    └── exceptions.py        # Custom exception hierarchy
```

## Core Components

### 1. Core Agent (`src/core/agent.py`)

**Responsibility**: Pure orchestration and service coordination

**Key Features**:
- Dependency injection for all services
- Clean command vs query processing separation
- Comprehensive error handling with fallbacks
- Health status aggregation
- Service access methods for commands

**Simplified from**: 1,272 lines → ~200 lines

### 2. Service Layer

#### LLM Service (`src/services/llm_service.py`)
- **Multi-provider support**: DeepSeek, OpenAI, Anthropic, Ollama, Groq
- **Health monitoring**: Automatic failover with exponential backoff
- **Mathematical optimization**: Enhanced prompts for math content
- **Performance tracking**: Response times, token usage, error rates

#### RAGFlow Service (`src/services/ragflow_service.py`)
- **Docker management**: Container lifecycle, health checks
- **Knowledge base operations**: Creation, document upload, indexing
- **BGE-M3 integration**: Optimized for mathematical content
- **Performance monitoring**: Processing times, storage usage

#### Memory Service (`src/services/memory_service.py`)
- **Conversation management**: Session-based with context preservation
- **Persistence**: Export/import with JSON serialization
- **Mathematical tagging**: Specialized search for math content
- **Size management**: Automatic cleanup based on age/count

### 3. RAG Pipeline

#### RAGFlow Client (`src/rag/retrieval/ragflow_client.py`)
- **BGE-M3 multi-vector**: Dense + sparse + ColBERT reranking
- **Mathematical content optimization**: LaTeX preservation, equation detection
- **Citation extraction**: Sentence-level source tracking
- **Quality-first approach**: Exhaustive search for <10K pages
- **Advanced reranking**: Mathematical content prioritization

### 4. Observability

#### Structured Logging (`src/observability/logger.py`)
- **JSON formatting**: Machine-readable logs
- **Correlation IDs**: Request tracing across services
- **Performance timing**: Operation duration tracking
- **Event categorization**: `agent.*`, `llm.*`, `ragflow.*`, `rag.*`

#### Performance Metrics (`src/observability/metrics.py`)
- **Comprehensive tracking**: Response times, error rates, token usage
- **Background monitoring**: System resources (CPU, memory, disk)
- **Service metrics**: RAGFlow performance, BGE-M3 effectiveness
- **Export functionality**: Analysis and reporting

## Performance Characteristics

### Response Times
- **Simple queries**: 2-5 seconds
- **Mathematical queries**: 5-10 seconds (quality-first approach)
- **RAG retrieval**: 3-7 seconds (BGE-M3 multi-vector)
- **Command execution**: <1 second

### Memory Usage
- **Base agent**: ~50MB
- **BGE-M3 model**: ~2GB (CPU inference)
- **RAGFlow services**: ~4GB (Docker containers)
- **Total system**: ~8GB (optimized for 16GB MacBook)

---

*This architecture successfully achieves our core principles of **Maintainability**, **Modularity**, **Simplicity**, and **Observability** while dramatically improving performance, reliability, and developer experience.* 