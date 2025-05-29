"""
RAGFlow Client Module

Advanced RAGFlow API client with BGE-M3 multi-vector retrieval integration
optimized for mathematical content processing and academic research.

This module focuses on:
- BGE-M3 multi-vector retrieval (dense + sparse + ColBERT)
- Mathematical content optimization with LaTeX preservation
- Automatic citation extraction with sentence-level source tracking
- Quality-first exhaustive search for small datasets (<10K pages)
- Advanced reranking with mathematical content prioritization
"""

import logging
import time
import requests
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import json
import re
from pathlib import Path
import hashlib

from src.core.config import ConfigManager
from src.rag.models.bge_m3_config import BGE_M3ModelConfig

logger = logging.getLogger(__name__)

@dataclass
class RetrievalResult:
    """Individual retrieval result structure"""
    content: str
    score: float
    source: str
    chunk_id: str
    page_number: Optional[int] = None
    sentence_indices: List[int] = None
    mathematical_content: bool = False
    latex_expressions: List[str] = None
    citation_context: str = ""
    rerank_score: Optional[float] = None
    
    def __post_init__(self):
        if self.sentence_indices is None:
            self.sentence_indices = []
        if self.latex_expressions is None:
            self.latex_expressions = []

@dataclass
class RetrievalResponse:
    """Complete retrieval response structure"""
    query: str
    results: List[RetrievalResult]
    total_results: int
    retrieval_time: float
    mathematical_query: bool = False
    reranking_applied: bool = False
    citation_count: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class RAGFlowClientError(Exception):
    """Custom exception for RAGFlow client errors"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)

class RAGFlowClient:
    """
    Advanced RAGFlow client with BGE-M3 integration and mathematical optimization.
    
    Features:
    - BGE-M3 multi-vector retrieval (dense + sparse + ColBERT reranking)
    - Mathematical content processing with LaTeX preservation
    - Automatic citation extraction with sentence-level granular tracking
    - Quality-first exhaustive search optimized for <10K pages
    - Advanced reranking with mathematical content prioritization
    - Comprehensive retrieval metrics and performance monitoring
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize RAGFlow client.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.base_url = self.config.get("ragflow.api.base_url", "http://localhost:9380")
        self.api_key = self.config.get("ragflow.api.key", "")
        self.timeout = self.config.get("ragflow.api.timeout", 60)
        
        # BGE-M3 configuration
        self.bge_config = BGE_M3ModelConfig(**config.get('bge_m3', {}))
        
        # Mathematical content processing
        self.enable_math_processing = self.config.get("ragflow.mathematical.enabled", True)
        self.latex_preservation = self.config.get("ragflow.mathematical.latex_preservation", True)
        self.math_symbol_extraction = self.config.get("ragflow.mathematical.symbol_extraction", True)
        
        # Retrieval configuration
        self.max_results = self.config.get("ragflow.retrieval.max_results", 50)
        self.reranking_enabled = self.config.get("ragflow.retrieval.reranking_enabled", True)
        self.exhaustive_search = self.config.get("ragflow.retrieval.exhaustive_search", True)
        self.citation_enabled = self.config.get("ragflow.retrieval.citation_enabled", True)
        
        # Quality optimization for small datasets
        self.quality_mode = self.config.get("ragflow.quality.enabled", True)
        self.chunk_overlap = self.config.get("ragflow.quality.chunk_overlap", 0.4)
        self.min_chunk_score = self.config.get("ragflow.quality.min_chunk_score", 0.1)
        
        # Mathematical content patterns for detection
        self._math_patterns = self._compile_math_patterns()
        
        logger.info("RAGFlow client initialized", extra={
            "base_url": self.base_url,
            "mathematical_processing": self.enable_math_processing,
            "reranking_enabled": self.reranking_enabled,
            "quality_mode": self.quality_mode,
            "max_results": self.max_results
        })
    
    def _compile_math_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for mathematical content detection"""
        patterns = [
            # LaTeX expressions
            re.compile(r'\$[^$]+\$'),  # Inline math
            re.compile(r'\$\$[^$]+\$\$'),  # Display math
            re.compile(r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}', re.DOTALL),  # Environments
            
            # Mathematical symbols and notation
            re.compile(r'[α-ωΑ-Ω]'),  # Greek letters
            re.compile(r'[∀∃∈∉⊂⊃∪∩∧∨¬→↔≡≠≤≥±×÷∫∑∏∂∞]'),  # Math symbols
            re.compile(r'\b(?:theorem|lemma|proof|definition|corollary|proposition)\b', re.IGNORECASE),
            
            # Mathematical expressions
            re.compile(r'\b\d+\s*[+\-*/=]\s*\d+'),  # Simple equations
            re.compile(r'\b[a-zA-Z]\s*[+\-*/=]\s*[a-zA-Z0-9]+'),  # Variables
            re.compile(r'\b(?:sin|cos|tan|log|ln|exp|sqrt)\s*\('),  # Functions
        ]
        return patterns
    
    def _detect_mathematical_content(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect mathematical content and extract LaTeX expressions.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple[bool, List[str]]: (has_math_content, latex_expressions)
        """
        latex_expressions = []
        has_math = False
        
        for pattern in self._math_patterns:
            matches = pattern.findall(text)
            if matches:
                has_math = True
                latex_expressions.extend(matches)
        
        return has_math, list(set(latex_expressions))  # Remove duplicates
    
    def retrieve(
        self, 
        query: str, 
        kb_id: str,
        top_k: int = None,
        enable_reranking: bool = None,
        mathematical_focus: bool = None
    ) -> RetrievalResponse:
        """
        Perform BGE-M3 multi-vector retrieval with mathematical optimization.
        
        Args:
            query: Search query
            kb_id: Knowledge base ID
            top_k: Number of results to return
            enable_reranking: Whether to apply reranking
            mathematical_focus: Whether to prioritize mathematical content
            
        Returns:
            RetrievalResponse: Complete retrieval results with metadata
        """
        start_time = time.time()
        
        # Auto-detect mathematical content if not specified
        if mathematical_focus is None:
            mathematical_focus, _ = self._detect_mathematical_content(query)
        
        # Use defaults if not specified
        top_k = top_k or self.max_results
        enable_reranking = enable_reranking if enable_reranking is not None else self.reranking_enabled
        
        try:
            # Phase 1: BGE-M3 Multi-Vector Retrieval
            retrieval_results = self._bge_m3_retrieval(
                query=query,
                kb_id=kb_id,
                top_k=top_k * 2 if enable_reranking else top_k,  # Get more for reranking
                mathematical_focus=mathematical_focus
            )
            
            # Phase 2: Mathematical Content Processing
            if self.enable_math_processing:
                retrieval_results = self._process_mathematical_content(retrieval_results)
            
            # Phase 3: Citation Extraction
            if self.citation_enabled:
                retrieval_results = self._extract_citations(retrieval_results, query)
            
            # Phase 4: Advanced Reranking
            if enable_reranking:
                retrieval_results = self._rerank_results(
                    results=retrieval_results,
                    query=query,
                    mathematical_focus=mathematical_focus,
                    target_count=top_k
                )
            
            # Phase 5: Quality Filtering
            if self.quality_mode:
                retrieval_results = self._apply_quality_filtering(retrieval_results)
            
            retrieval_time = time.time() - start_time
            
            # Count citations
            citation_count = sum(1 for r in retrieval_results if r.citation_context)
            
            response = RetrievalResponse(
                query=query,
                results=retrieval_results[:top_k],
                total_results=len(retrieval_results),
                retrieval_time=retrieval_time,
                mathematical_query=mathematical_focus,
                reranking_applied=enable_reranking,
                citation_count=citation_count,
                metadata={
                    "kb_id": kb_id,
                    "bge_m3_config": self.bge_config.get_config_summary(),
                    "quality_mode": self.quality_mode,
                    "exhaustive_search": self.exhaustive_search
                }
            )
            
            logger.info(
                "BGE-M3 retrieval completed",
                extra={
                    "query_length": len(query),
                    "mathematical_focus": mathematical_focus,
                    "results_count": len(retrieval_results),
                    "citations_found": citation_count,
                    "retrieval_time": retrieval_time,
                    "reranking_applied": enable_reranking
                }
            )
            
            return response
            
        except Exception as e:
            logger.error("BGE-M3 retrieval failed", extra={"error": str(e), "query": query[:100]})
            raise RAGFlowClientError(f"Retrieval failed: {str(e)}")
    
    def _bge_m3_retrieval(
        self, 
        query: str, 
        kb_id: str, 
        top_k: int,
        mathematical_focus: bool
    ) -> List[RetrievalResult]:
        """
        Perform BGE-M3 multi-vector retrieval (dense + sparse + ColBERT).
        
        Args:
            query: Search query
            kb_id: Knowledge base ID
            top_k: Number of results
            mathematical_focus: Mathematical content focus
            
        Returns:
            List[RetrievalResult]: Raw retrieval results
        """
        # Configure BGE-M3 retrieval parameters
        retrieval_params = {
            "query": query,
            "kb_id": kb_id,
            "top_k": top_k,
            
            # BGE-M3 multi-vector configuration
            "embedding_model": "bge-m3",
            "retrieval_mode": "hybrid",  # dense + sparse + ColBERT
            "dense_weight": 0.4,
            "sparse_weight": 0.3,
            "colbert_weight": 0.3,
            
            # Mathematical optimization
            "mathematical_focus": mathematical_focus,
            "preserve_latex": self.latex_preservation,
            "extract_math_symbols": self.math_symbol_extraction,
            
            # Quality settings for small datasets
            "exhaustive_search": self.exhaustive_search,
            "chunk_overlap_handling": True,
            "min_score_threshold": self.min_chunk_score,
            
            # Advanced features
            "include_metadata": True,
            "include_page_numbers": True,
            "sentence_level_retrieval": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/retrieval/bge-m3",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=retrieval_params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Convert to RetrievalResult objects
            results = []
            for item in data.get("results", []):
                # Detect mathematical content in chunk
                has_math, latex_exprs = self._detect_mathematical_content(item.get("content", ""))
                
                result = RetrievalResult(
                    content=item.get("content", ""),
                    score=item.get("score", 0.0),
                    source=item.get("source", ""),
                    chunk_id=item.get("chunk_id", ""),
                    page_number=item.get("page_number"),
                    sentence_indices=item.get("sentence_indices", []),
                    mathematical_content=has_math,
                    latex_expressions=latex_exprs
                )
                results.append(result)
            
            return results
            
        except requests.RequestException as e:
            logger.error("BGE-M3 API request failed", extra={"error": str(e)})
            raise RAGFlowClientError(f"BGE-M3 retrieval request failed: {str(e)}")
        except Exception as e:
            logger.error("BGE-M3 retrieval processing failed", extra={"error": str(e)})
            raise RAGFlowClientError(f"BGE-M3 retrieval processing failed: {str(e)}")
    
    def _process_mathematical_content(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """
        Enhanced mathematical content processing for retrieval results.
        
        Args:
            results: Raw retrieval results
            
        Returns:
            List[RetrievalResult]: Processed results with enhanced mathematical metadata
        """
        processed_results = []
        
        for result in results:
            # Enhanced mathematical content detection
            has_math, latex_exprs = self._detect_mathematical_content(result.content)
            
            # Update mathematical metadata
            result.mathematical_content = has_math
            result.latex_expressions = latex_exprs
            
            # Mathematical content scoring boost
            if has_math and result.mathematical_content:
                # Boost score for mathematical content (quality-first approach)
                math_boost = 0.1 * len(latex_exprs)  # More math = higher boost
                result.score = min(1.0, result.score + math_boost)
            
            processed_results.append(result)
        
        return processed_results
    
    def _extract_citations(self, results: List[RetrievalResult], query: str) -> List[RetrievalResult]:
        """
        Extract automatic citations with sentence-level granular source tracking.
        
        Args:
            results: Retrieval results
            query: Original query
            
        Returns:
            List[RetrievalResult]: Results with citation information
        """
        for result in results:
            try:
                # Generate citation context
                citation_parts = []
                
                # Source information
                if result.source:
                    citation_parts.append(f"Source: {result.source}")
                
                # Page number if available
                if result.page_number:
                    citation_parts.append(f"Page: {result.page_number}")
                
                # Sentence-level tracking
                if result.sentence_indices:
                    sentence_refs = ", ".join(map(str, result.sentence_indices))
                    citation_parts.append(f"Sentences: {sentence_refs}")
                
                # Mathematical content indicators
                if result.mathematical_content and result.latex_expressions:
                    math_count = len(result.latex_expressions)
                    citation_parts.append(f"Mathematical expressions: {math_count}")
                
                result.citation_context = " | ".join(citation_parts)
                
            except Exception as e:
                logger.warning(
                    "Citation extraction failed for result",
                    extra={"chunk_id": result.chunk_id, "error": str(e)}
                )
                result.citation_context = f"Source: {result.source}" if result.source else ""
        
        return results
    
    def _rerank_results(
        self,
        results: List[RetrievalResult],
        query: str,
        mathematical_focus: bool,
        target_count: int
    ) -> List[RetrievalResult]:
        """
        Advanced reranking with mathematical content prioritization.
        
        Args:
            results: Initial retrieval results
            query: Original query
            mathematical_focus: Whether to prioritize mathematical content
            target_count: Target number of results
            
        Returns:
            List[RetrievalResult]: Reranked results
        """
        if not results:
            return results
        
        # Reranking factors
        for result in results:
            rerank_score = result.score
            
            # Mathematical content boost
            if mathematical_focus and result.mathematical_content:
                math_factor = 1.0 + (0.2 * len(result.latex_expressions))
                rerank_score *= math_factor
            
            # Source diversity factor
            # Prefer results from different sources for comprehensive coverage
            
            # Content length factor (prefer substantial content)
            length_factor = min(1.2, len(result.content) / 1000)  # Normalize to 1000 chars
            rerank_score *= length_factor
            
            # Citation quality factor
            if result.citation_context:
                rerank_score *= 1.1  # Boost for good citation info
            
            result.rerank_score = rerank_score
        
        # Sort by rerank score
        reranked_results = sorted(results, key=lambda r: r.rerank_score or r.score, reverse=True)
        
        logger.debug(
            "Results reranked",
            extra={
                "mathematical_focus": mathematical_focus,
                "original_count": len(results),
                "target_count": target_count
            }
        )
        
        return reranked_results[:target_count]
    
    def _apply_quality_filtering(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """
        Apply quality filtering for optimal results in small datasets.
        
        Args:
            results: Retrieval results
            
        Returns:
            List[RetrievalResult]: Quality-filtered results
        """
        if not self.quality_mode:
            return results
        
        filtered_results = []
        
        for result in results:
            # Score threshold
            score = result.rerank_score or result.score
            if score < self.min_chunk_score:
                continue
            
            # Content length threshold (avoid very short chunks)
            if len(result.content.strip()) < 50:
                continue
            
            # Mathematical content quality (if mathematical query)
            if result.mathematical_content and not result.latex_expressions:
                # Has mathematical markers but no LaTeX - might be false positive
                continue
            
            filtered_results.append(result)
        
        logger.debug(
            "Quality filtering applied",
            extra={
                "original_count": len(results),
                "filtered_count": len(filtered_results),
                "min_score": self.min_chunk_score
            }
        )
        
        return filtered_results
    
    def get_knowledge_base_info(self, kb_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            Dict[str, Any]: Knowledge base information
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/knowledge_bases/{kb_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error("Failed to get knowledge base info", extra={"kb_id": kb_id, "error": str(e)})
            raise RAGFlowClientError(f"Failed to get knowledge base info: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test connection to RAGFlow service.
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/health",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error("RAGFlow connection test failed", extra={"error": str(e)})
            return False
    
    def get_retrieval_statistics(self, kb_id: str) -> Dict[str, Any]:
        """
        Get retrieval statistics for a knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            Dict[str, Any]: Retrieval statistics
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/knowledge_bases/{kb_id}/statistics",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout
            )
            
            response.raise_for_status()
            stats = response.json()
            
            # Add BGE-M3 specific statistics
            stats["bge_m3_config"] = self.bge_config.get_config_summary()
            stats["mathematical_processing"] = self.enable_math_processing
            stats["quality_mode"] = self.quality_mode
            
            return stats
            
        except Exception as e:
            logger.error("Failed to get retrieval statistics", extra={"kb_id": kb_id, "error": str(e)})
            raise RAGFlowClientError(f"Failed to get retrieval statistics: {str(e)}")

# Convenience functions for common operations

def create_ragflow_client(config: ConfigManager) -> RAGFlowClient:
    """
    Create and configure RAGFlow client.
    
    Args:
        config: Configuration manager
        
    Returns:
        RAGFlowClient: Configured client instance
    """
    return RAGFlowClient(config)

def test_ragflow_connection(config: ConfigManager) -> bool:
    """
    Test RAGFlow service connection.
    
    Args:
        config: Configuration manager
        
    Returns:
        bool: True if connection successful
    """
    client = RAGFlowClient(config)
    return client.test_connection() 