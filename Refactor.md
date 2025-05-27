# Learning Agent Refactoring Plan

**Objective**: Transform the monolithic 1,272-line `learning_agent.py` into a maintainable, modular, simple, and observable codebase.

**Principles**: Maintainability • Modularity • Simplicity • Observability

---

## 📊 Current State Analysis

- **Main file**: `learning_agent.py` (1,272 lines)
- **Key issues**:
  - Monolithic structure with mixed concerns
  - 150+ lines of inline LaTeX processing mixed with business logic
  - Limited error visibility and debugging capabilities
  - Complex command handling mixed with business logic
  - No structured logging or metrics
  - Simple RAG pipeline with Qdrant (no advanced features like reranking, citations, layout-aware processing)
  - **Migration needed**: Qdrant → RAGFlow for superior document processing and retrieval

---

## 🗂️ Target Architecture

```
src/
├── __init__.py
├── main.py                    # Entry point (minimal)
├── core/
│   ├── __init__.py
│   ├── agent.py              # Simplified main agent class
│   └── config.py             # Enhanced configuration management
├── rag/                      # RAG pipeline (top-level) - RAGFlow integration
│   ├── __init__.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── ragflow_client.py # RAGFlow API client and retriever
│   │   ├── qdrant_legacy.py  # Legacy Qdrant support (migration fallback)
│   │   ├── reranking.py      # Document reranking strategies
│   │   ├── hybrid.py         # Hybrid retrieval (semantic + keyword)
│   │   └── citations.py     # Citation extraction and formatting
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── documents.py      # Document preprocessing pipeline
│   │   ├── chunking.py       # Advanced chunking strategies
│   │   ├── markdown.py       # Markdown document processing
│   │   └── layout_aware.py   # OCR, tables, figures (RAGFlow integration)
│   ├── pipeline.py           # RAG orchestration - RAGFlow primary
│   ├── migration.py          # Qdrant → RAGFlow data migration
│   └── evaluation.py         # RAG performance metrics
├── services/
│   ├── __init__.py
│   ├── llm_service.py        # LLM factory and management
│   ├── vector_service.py     # Legacy Qdrant operations (migration support)
│   ├── ragflow_service.py    # RAGFlow Docker management and health checks
│   └── memory_service.py     # Chat memory management
├── text_processing/
│   ├── __init__.py
│   ├── latex_renderer.py     # LaTeX/math expression display
│   ├── markdown_renderer.py  # Rich markdown rendering
│   └── formatters.py         # Text formatting utilities
├── ui/
│   ├── __init__.py
│   ├── console_interface.py  # Rich console management
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── base.py          # Command base classes
│   │   ├── database.py      # Database commands
│   │   ├── provider.py      # Provider switching
│   │   ├── rag.py           # RAG-specific commands
│   │   └── system.py        # System commands (help, exit, etc.)
│   └── response_renderer.py  # Response formatting and display
├── observability/
│   ├── __init__.py
│   ├── logger.py            # Structured logging
│   ├── metrics.py           # Performance metrics
│   └── health.py            # Health checks
└── utils/
    ├── __init__.py
    └── exceptions.py         # Custom exception classes
```

---

## 🎯 Refactoring Phases

### Phase 1: Foundation & Modularity (High Priority)

#### Task 1.1: Create Project Structure & Migration Setup
- [ ] Create `src/` directory structure
- [ ] Create all necessary `__init__.py` files
- [ ] Move existing utility files to appropriate locations:
  - `config_utils.py` → `src/core/config.py`
  - `qdrant_utils.py` → `src/services/vector_service.py` (legacy support)
- [ ] Set up RAGFlow Docker infrastructure:
  - [ ] Create `docker-compose.ragflow.yml`
  - [ ] Add RAGFlow environment variables to `.env.sample`
  - [ ] Add Makefile targets for RAGFlow management

#### Task 1.2: Extract RAG Pipeline & RAGFlow Integration (Critical)
- [ ] Create `src/rag/` directory structure
  - [ ] Create all necessary `__init__.py` files
  - [ ] Move existing RAG logic from `learning_agent.py`

- [ ] Create `src/rag/retrieval/ragflow_client.py`
  - [ ] Implement RAGFlow API client with full feature support
  - [ ] Create RAGFlowRetriever class with LangChain compatibility
  - [ ] Add knowledge base management methods
  - [ ] Include automatic citation extraction and granular source tracking
  - [ ] Implement hybrid retrieval (semantic + keyword fusion)
  - [ ] Add reranking capabilities with model-based reranking

- [ ] Create `src/rag/retrieval/graphrag.py`
  - [ ] Implement GraphRAG integration for knowledge graph-enhanced retrieval
  - [ ] Add entity-relationship extraction and N-hop traversal
  - [ ] Include community detection and PageRank-based relevance scoring
  - [ ] Support multi-hop reasoning for complex queries

- [ ] Create `src/rag/retrieval/raptor.py`
  - [ ] Implement RAPTOR (Recursive Abstractive Processing) for hierarchical summarization
  - [ ] Add clustering-based optimal chunking with UMAP and Gaussian Mixture Models
  - [ ] Support multi-level abstraction and tree-structured organization

- [ ] Create `src/rag/pipeline.py`
  - [ ] Extract `RetrievalService` class and rename to `RAGPipeline`
  - [ ] Set RAGFlow as the sole retriever (no Qdrant fallback)
  - [ ] Integrate GraphRAG and RAPTOR techniques
  - [ ] Include comprehensive logging and metrics for all advanced features

- [ ] Create `src/rag/migration.py`
  - [ ] Export existing Qdrant data to RAGFlow-compatible format
  - [ ] Batch document upload to RAGFlow knowledge base with layout awareness
  - [ ] Validation tools comparing old vs new retrieval quality

- [ ] Create `src/rag/processing/documents.py`
  - [ ] Extract document preprocessing logic
  - [ ] Support for markdown documents (RAGFlow native)
  - [ ] Integration with RAGFlow's DeepDoc for layout-aware processing
  - [ ] OCR capabilities for image-based documents
  - [ ] Table Structure Recognition (TSR) for complex tables
  - [ ] Figure and caption extraction with embedded text analysis

- [ ] Create `src/rag/processing/layout_aware.py`
  - [ ] Implement layout component recognition (Text, Title, Figure, Table, etc.)
  - [ ] Advanced table parsing with hierarchy headers and spanning cells
  - [ ] Figure-caption relationship mapping
  - [ ] Multi-format optimization (PDF, DOCX, Excel, PPT)

#### Task 1.3: Extract Text Rendering (Critical for UX)
- [ ] Create `src/text_processing/latex_renderer.py`
  - [ ] Extract all LaTeX regex patterns into a dedicated class
  - [ ] Create `LatexRenderer` class with methods:
    - `render_latex(text: str) -> str`
    - `_process_block_environments(text: str) -> str`
    - `_process_math_symbols(text: str) -> str`
    - `_process_greek_letters(text: str) -> str`
  - [ ] Add comprehensive docstrings and type hints
  - [ ] Include error handling for malformed LaTeX
  - [ ] Focus on beautiful math expression display for user experience

- [ ] Create `src/text_processing/markdown_renderer.py`
  - [ ] Extract Rich markdown rendering logic
  - [ ] Create `MarkdownRenderer` class with methods:
    - `render_response(text: str, title: str) -> None`
    - `render_panel(text: str, title: str) -> None`
  - [ ] Handle ImportError fallbacks gracefully

#### Task 1.4: Extract Service Layer & RAGFlow Services
- [ ] Create `src/services/llm_service.py`
  - [ ] Move `LLMFactory` class
  - [ ] Add connection health monitoring
  - [ ] Implement retry logic with exponential backoff
  - [ ] Add structured logging for provider switches

- [ ] Create `src/services/ragflow_service.py`
  - [ ] RAGFlow Docker container management
  - [ ] Health checks and service monitoring
  - [ ] Knowledge base lifecycle management
  - [ ] Document upload and indexing orchestration

- [ ] Create `src/services/memory_service.py`
  - [ ] Move `ChatMemory` class
  - [ ] Add memory size limits and cleanup
  - [ ] Add conversation export/import functionality

- [ ] Remove `qdrant_utils.py` and all Qdrant dependencies
  - [ ] Create one-time migration script in `tools/migrate_to_ragflow.py`
  - [ ] Export Qdrant data for final RAGFlow import
  - [ ] Clean up all Qdrant configuration and code references

### Phase 2: Simplify Core Agent (Medium Priority)

#### Task 2.1: Streamline Main Agent Class
- [ ] Create `src/core/agent.py`
  - [ ] Reduce `LearningAgent` to ~200 lines focused on orchestration
  - [ ] Remove all inline text processing
  - [ ] Extract initialization logic to separate methods
  - [ ] Implement dependency injection for services

- [ ] Create `src/main.py`
  - [ ] Move main entry point logic
  - [ ] Add startup health checks
  - [ ] Implement graceful shutdown handling

#### Task 2.2: Extract Command System
- [ ] Create `src/ui/commands/base.py`
  - [ ] Move abstract `Command` class
  - [ ] Add command registration decorators
  - [ ] Implement command middleware for logging

- [ ] Create command modules:
  - [ ] `src/ui/commands/system.py` (exit, help, config)
  - [ ] `src/ui/commands/provider.py` (provider switching)
  - [ ] `src/ui/commands/memory.py` (memory management)
  - [ ] `src/ui/commands/rag.py` (RAGFlow operations, GraphRAG controls, RAPTOR configuration)
  - [ ] `src/ui/commands/knowledge.py` (knowledge base management, document processing, layout analysis)

### Phase 3: Add Observability (High Priority)

#### Task 3.1: Implement Structured Logging
- [ ] Create `src/observability/logger.py`
  - [ ] Set up structured logging with JSON format
  - [ ] Define log levels and categories:
    - `agent.startup`, `agent.query`, `agent.error`
    - `llm.switch`, `llm.request`, `llm.error`
    - `ragflow.startup`, `ragflow.query`, `ragflow.health`, `ragflow.error`
    - `rag.retrieval`, `rag.reranking`, `rag.citations`, `rag.graphrag`, `rag.raptor`
    - `layout.ocr`, `layout.table_recognition`, `layout.figure_extraction`
    - `knowledge.upload`, `knowledge.processing`, `knowledge.indexing`
  - [ ] Add correlation IDs for request tracking
  - [ ] Include performance timing

#### Task 3.2: Add Performance Metrics
- [ ] Create `src/observability/metrics.py`
  - [ ] Track key metrics:
    - Response generation time and quality scores
    - RAGFlow retrieval success/failure rates
    - Citation accuracy and coverage (RAGFlow automatic citations)
    - Document reranking effectiveness and precision improvements
    - GraphRAG entity extraction and relationship mapping accuracy
    - RAPTOR hierarchical summarization performance
    - Layout-aware processing success rates (OCR, TSR, figure extraction)
    - Knowledge base indexing and query performance
    - LLM provider switching events
    - RAGFlow service health and Docker container performance
    - Memory usage patterns and optimization metrics
    - Command usage statistics and user workflow patterns
    - LaTeX rendering performance and accuracy
    - Advanced retrieval technique effectiveness (hybrid, semantic+keyword fusion)
  - [ ] Export metrics in structured format

#### Task 3.3: Implement Health Monitoring
- [ ] Create `src/observability/health.py`
  - [ ] Add health check endpoints for all services:
    - LLM provider connectivity and response quality
    - RAGFlow service status and Docker container health
    - RAGFlow knowledge base accessibility and indexing status
    - GraphRAG entity graph connectivity and traversal capability
    - RAPTOR hierarchical processing pipeline status
    - DeepDoc layout processing (OCR, TSR, figure extraction) capability
    - Memory service status and conversation persistence
    - LaTeX rendering capability and math expression accuracy
  - [ ] Implement service degradation detection
  - [ ] Add automatic service recovery attempts

### Phase 4: Enhance Maintainability (Medium Priority)

#### Task 4.1: Improve Type Safety
- [ ] Add comprehensive type hints to all modules
- [ ] Create `src/core/types.py` with common type definitions
- [ ] Use dataclasses for configuration objects
- [ ] Define Protocol interfaces for service contracts

#### Task 4.2: Enhanced Configuration Management
- [ ] Enhance `src/core/config.py`:
  - [ ] Add configuration validation with Pydantic
  - [ ] Implement environment-specific configs
  - [ ] Add configuration hot-reloading
  - [ ] Create configuration schema documentation

#### Task 4.3: Error Handling & Custom Exceptions
- [ ] Create `src/utils/exceptions.py`
  - [ ] Define custom exception hierarchy:
    - `LearningAgentError` (base)
    - `LLMServiceError`, `VectorServiceError`
    - `ConfigurationError`, `AuthenticationError`
  - [ ] Add error context and recovery suggestions
  - [ ] Implement error aggregation and reporting

### Phase 5: Testing & Documentation (Low Priority)

#### Task 5.1: Unit Testing Infrastructure
- [ ] Create comprehensive test suite:
  - [ ] `tests/unit/test_latex_renderer.py`
  - [ ] `tests/unit/test_rag_pipeline.py`
  - [ ] `tests/unit/test_llm_service.py`
  - [ ] `tests/unit/test_vector_service.py`
  - [ ] `tests/unit/test_retrievers.py`
  - [ ] `tests/unit/test_commands.py`
  - [ ] `tests/integration/test_agent_workflow.py`
  - [ ] `tests/integration/test_rag_retrieval.py`

#### Task 5.2: Documentation
- [ ] Add docstrings to all public methods
- [ ] Create API documentation
- [ ] Write architecture decision records (ADRs)
- [ ] Update README with new structure

---

## 🔄 Migration Strategy

### Step-by-Step Migration Plan

1. **Week 1**: Foundation & RAGFlow Setup (Tasks 1.1-1.3)
   - Create directory structure with advanced RAG components
   - Set up RAGFlow Docker infrastructure with GPU support
   - Extract RAG pipeline with RAGFlow, GraphRAG, and RAPTOR integration
   - Extract LaTeX renderer (immediate UX improvement)
   - Extract markdown renderer and layout-aware processing

2. **Week 2**: Advanced RAG Implementation (Tasks 1.4, 3.1)
   - Extract LLM and memory services
   - Create RAGFlow service layer with DeepDoc integration
   - Implement GraphRAG for knowledge graph-enhanced retrieval
   - Implement RAPTOR for hierarchical document processing
   - Implement basic structured logging for all advanced features

3. **Week 3**: Migration & Core Simplification (Tasks 2.1-2.2)
   - Complete Qdrant → RAGFlow data migration (one-time)
   - Simplify main agent class to use RAGFlow exclusively
   - Extract command system with GraphRAG and RAPTOR controls
   - Remove all Qdrant dependencies and clean up codebase
   - Create new entry point with advanced RAG capabilities

4. **Week 4**: Observability & Advanced Features (Tasks 3.2-3.3)
   - Add comprehensive metrics for GraphRAG, RAPTOR, and layout processing
   - Implement health monitoring for all RAGFlow services
   - Performance optimization and tuning for advanced retrieval
   - Add citation tracking and layout analysis monitoring

5. **Week 5**: Polish & Advanced Documentation (Tasks 4.1-4.2)
   - Add type hints for all new RAG components
   - Enhance configuration for GraphRAG and RAPTOR
   - Error handling improvements for complex pipelines
   - Update documentation with advanced RAG techniques and examples

### Validation Criteria

Each task must meet these criteria before being considered complete:

✅ **Maintainability**:
- Code is self-documenting with clear intent
- Functions/classes have single responsibility
- Dependencies are explicit and minimal

✅ **Modularity**:
- Components can be tested independently
- Clear interfaces between modules
- No circular dependencies

✅ **Simplicity**:
- Complex operations are broken into simple steps
- No premature optimization
- Straightforward data flow

✅ **Observability**:
- All operations are logged with context
- Performance metrics are captured
- Errors include actionable information

---

## 🎯 Success Metrics

### Code Quality Metrics
- [ ] Main agent class reduced from 1,272 to <200 lines
- [ ] No single file exceeds 300 lines
- [ ] Test coverage >80% for core modules
- [ ] Zero circular dependencies

### Performance Metrics
- [ ] Startup time <5 seconds
- [ ] Response time <2 seconds (95th percentile)
- [ ] Memory usage stable over time
- [ ] Error recovery success rate >90%

### Developer Experience
- [ ] New features can be added in <1 day
- [ ] Bugs can be isolated to specific modules
- [ ] Configuration changes don't require code changes
- [ ] Logs provide clear debugging information

---

## 🚫 Breaking Changes

### Minimal External Impact
- Main entry point remains `python learning_agent.py`
- Configuration file format enhanced (RAGFlow, GraphRAG, RAPTOR settings added)
- All existing commands continue to work (significantly enhanced with advanced RAG features)
- User experience dramatically improved:
  - Better LaTeX/math display with enhanced rendering
  - Automatic granular citations with precise source tracking
  - Layout-aware document understanding (tables, figures, equations)
  - Multi-hop reasoning through knowledge graphs
  - Hierarchical document summarization and retrieval

### Internal Changes Only  
- Import paths will change (internal only)
- Module organization restructured for advanced RAG techniques
- Logging format enhanced (GraphRAG, RAPTOR, layout processing data)
- Error messages improved (more helpful, context-aware)
- Vector storage backend: Complete migration from Qdrant → RAGFlow
- Advanced retrieval pipeline: Simple vector search → Sophisticated multi-modal RAG

---

## 🛡️ Risk Mitigation

### High-Risk Areas
1. **LaTeX Rendering**: Complex regex patterns for math expressions
   - Mitigation: Comprehensive test suite with edge cases
   - Rollback: Keep original code as fallback
   - Special focus: Ensure beautiful math display for user experience

2. **Qdrant → RAGFlow Migration**: Data loss or retrieval quality degradation
   - Mitigation: Comprehensive data export/validation before migration
   - Rollback: Maintain Qdrant as fallback during migration period
   - Validation: Side-by-side comparison of retrieval results

3. **LLM Service Changes**: Provider switching logic
   - Mitigation: Gradual migration with feature flags
   - Rollback: Maintain backward compatibility

4. **Configuration Changes**: Enhanced validation
   - Mitigation: Default values for all new fields
   - Rollback: Support legacy configuration format

### Testing Strategy
- Unit tests for each extracted module
- Integration tests for service interactions
- End-to-end tests for user workflows
- Performance benchmarks for critical paths

---

*This refactoring plan adheres to our core principles of **Maintainability**, **Modularity**, **Simplicity**, and **Observability** while ensuring minimal disruption to existing functionality.* 