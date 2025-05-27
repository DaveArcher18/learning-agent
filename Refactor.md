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
  - [ ] Implement RAGFlow API client with BGE-M3 embedding model integration
  - [ ] Create RAGFlowRetriever class with BGE-M3 multi-functionality support
  - [ ] Add knowledge base management methods optimized for mathematical content
  - [ ] Include automatic citation extraction with sentence-level granular source tracking
  - [ ] Implement BGE-M3 ensemble retrieval (dense + sparse + ColBERT multi-vector)
  - [ ] Add multi-stage reranking with mathematical content prioritization
  - [ ] Small dataset optimization: 40% chunk overlap, 1000-token chunks, exhaustive processing

- [ ] Create `src/rag/retrieval/graphrag.py`
  - [ ] Implement GraphRAG integration for knowledge graph-enhanced retrieval
  - [ ] Add exhaustive entity-relationship extraction and N-hop traversal (up to 4 hops)
  - [ ] Include high-resolution community detection and PageRank-based relevance scoring
  - [ ] Support multi-hop reasoning for complex queries with deep relationship exploration
  - [ ] Optimize for small datasets: comprehensive entity linking, detailed relationship typing

- [ ] Create `src/rag/retrieval/raptor.py`
  - [ ] Implement RAPTOR for mathematical content hierarchical organization
  - [ ] BGE-M3 optimized clustering with mathematical concept grouping
  - [ ] Support 6-level abstraction trees: theorem→proof→lemma→definition→example→application
  - [ ] Quality-first configuration: mathematical concept preservation, theorem dependency tracking
  - [ ] Pre-build complete hierarchical trees for <10K pages (batch processing approach)
  - [ ] Mathematical notation aware summarization with LaTeX preservation

- [ ] Create `src/rag/pipeline.py`
  - [ ] Extract `RetrievalService` class and rename to `MathematicalRAGPipeline`
  - [ ] Set RAGFlow with BGE-M3 as the sole retriever (M1 optimized, no Qdrant fallback)
  - [ ] Integrate GraphRAG (mathematical concept mapping) and RAPTOR (theorem hierarchies)
  - [ ] Implement BGE-M3 multi-vector retrieval: dense + sparse + ColBERT reranking
  - [ ] Target 5-10 second response times with quality-first batch preprocessing
  - [ ] Include comprehensive logging and metrics for mathematical content analysis

- [ ] Create `src/rag/migration.py`
  - [ ] Export existing Qdrant data to BGE-M3 compatible format for RAGFlow
  - [ ] Batch document upload to RAGFlow knowledge base with mathematical notation preservation
  - [ ] Validation tools comparing old vs new retrieval quality with mathematical accuracy metrics

- [ ] Create `src/rag/models/bge_m3_config.py`
  - [ ] BGE-M3 model configuration optimized for M1 MacBook Air (16GB RAM)
  - [ ] CPU-only inference settings with optimal batch sizes for mathematical content
  - [ ] Multi-vector configuration: dense embeddings (512 dim) + sparse retrieval + ColBERT reranking
  - [ ] Token limit optimization (8192 tokens) for complete mathematical proofs and theorems
  - [ ] Mathematical notation and LaTeX expression handling
  - [ ] Small dataset optimization: aggressive caching, pre-computed embeddings, exhaustive search

- [ ] Create `src/rag/processing/documents.py`
  - [ ] Extract document preprocessing logic optimized for mathematical content
  - [ ] Native support for markdown documents from academic papers (LaTeX-derived)
  - [ ] Integration with RAGFlow's DeepDoc for mathematical notation processing
  - [ ] Advanced mathematical equation and formula recognition
  - [ ] Comprehensive Table Structure Recognition for mathematical tables and proofs
  - [ ] Mathematical figure and diagram extraction with LaTeX expression analysis
  - [ ] Quality-first chunking: 1000-token chunks with 40% overlap for mathematical context preservation
  - [ ] Sentence-level citation tracking optimized for academic paper source attribution
  - [ ] BGE-M3 token limit optimization (up to 8192 tokens) for complete mathematical proofs

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

## 📐 Mathematical Content Architecture

### BGE-M3 Optimization for Academic Papers

**Hardware Configuration (M1 MacBook Air 16GB)**:
- CPU-only inference with optimized batch sizes (4-8 documents)
- Memory-efficient chunking: 1000 tokens with 40% overlap
- Pre-computed embeddings for <10K pages with aggressive caching
- Multi-vector retrieval: dense (512 dim) + sparse + ColBERT reranking

**Mathematical Content Pipeline**:
```
Academic PDF → Mistral OCR → Markdown → BGE-M3 Processing → RAGFlow Storage
                                    ↓
                        Mathematical Notation Preservation
                                    ↓
                    LaTeX Expression Recognition & Indexing
                                    ↓
                Theorem/Proof/Definition Classification
                                    ↓
                    Citation & Source Tracking (Sentence-level)
```

**Quality-First Retrieval Strategy**:
1. **Exhaustive Search**: Retrieve top-50 candidates using BGE-M3 multi-vector
2. **Mathematical Reranking**: Prioritize mathematical content relevance
3. **Context Preservation**: Ensure theorem dependencies and proof chains intact
4. **Source Attribution**: Maintain granular citation tracking for verification
5. **Final Selection**: Return top-15 highest quality, mathematically coherent results

**Target Performance**:
- Response Time: 5-10 seconds (acceptable for academic research quality)
- Accuracy: Prioritize mathematical correctness over speed
- Source Traceability: 100% sentence-level citation accuracy
- Mathematical Notation: Preserve LaTeX formatting and mathematical symbols

---

## 🔄 Migration Strategy

### Step-by-Step Migration Plan

1. **Week 1**: Foundation & BGE-M3 Mathematical RAG Setup (Tasks 1.1-1.3)
   - Create directory structure optimized for mathematical content processing
   - Set up RAGFlow Docker infrastructure with BGE-M3 integration and M1 CPU optimization
   - Configure BGE-M3 multi-vector setup: dense + sparse + ColBERT (CPU-only, 16GB RAM)
   - Extract RAG pipeline with quality-first approach for <10K pages mathematical content
   - Extract LaTeX renderer (critical for mathematical expression display)
   - Extract markdown renderer with academic paper formatting support

2. **Week 2**: BGE-M3 Integration & Mathematical Content Pipeline (Tasks 1.4, 3.1)
   - Implement BGE-M3 model configuration with mathematical notation handling (8192 tokens)
   - Extract LLM and memory services optimized for mathematical reasoning (DeepSeek integration)
   - Implement RAGFlow service layer with mathematical layout processing (equations, proofs, theorems)
   - Complete Qdrant → RAGFlow migration with BGE-M3 embedding conversion
   - Set up mathematical content aware GraphRAG (theorem/proof relationship mapping)
   - Implement RAPTOR hierarchical processing for mathematical concept organization

3. **Week 3**: Quality-First Optimization & Mathematical Pipelines (Tasks 2.1-2.2)
   - Optimize MathematicalRAGPipeline for 5-10 second response times with batch preprocessing
   - Extract command system with mathematical knowledge base management
   - Fine-tune BGE-M3 multi-vector retrieval with 40% chunk overlap for mathematical context
   - Implement mathematical content validation and granular source tracking for accuracy
   - Remove all Qdrant dependencies and create one-time migration tools
   - Create new entry point with mathematical content health checks

4. **Week 4**: Mathematical Content Observability & M1 Performance Tuning (Tasks 3.2-3.3)
   - Add mathematical accuracy metrics and citation traceability monitoring
   - Implement health monitoring for BGE-M3 performance and mathematical notation processing
   - Performance tuning for M1 hardware: memory optimization, CPU utilization, optimal batch sizing
   - Quality validation comparing mathematical content retrieval accuracy vs baseline
   - Add mathematical theorem/proof dependency tracking and reasoning chain validation

5. **Week 5**: Academic Paper Pipeline & Documentation (Tasks 4.1-4.2)
   - Finalize academic paper processing pipeline (Mistral OCR → Markdown → BGE-M3 → RAGFlow)
   - Add comprehensive type hints for all mathematical content processing components
   - Enhance configuration for mathematical content: theorem hierarchies, proof structures, citation networks
   - Document mathematical content pipeline and BGE-M3 configuration for academic research use
   - Create validation tools for mathematical accuracy and source attribution

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