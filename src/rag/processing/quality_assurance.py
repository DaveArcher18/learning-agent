"""
Quality Assurance Pipeline for Academic Paper Processing.

This module provides comprehensive quality assurance including:
- Retrieval quality validation with mathematical accuracy metrics
- Citation verification and source validation  
- Content quality scoring for academic papers
- Automated testing for mathematical content preservation

Designed for maintainability, modularity, simplicity, and observability.
"""

import re
import logging
from typing import Dict, List, Optional, Set, Tuple, NamedTuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import json
from collections import defaultdict, Counter
import hashlib
from datetime import datetime
import statistics
from enum import Enum

from ..retrieval.ragflow_client import RAGFlowClient
from ..processing.academic_papers import AcademicPaperStructure, Citation
from ...text_processing.latex_renderer import LatexRenderer
from ...text_processing.math_indexer import MathematicalIndex, MathematicalEquation

logger = logging.getLogger(__name__)


class QualityLevel(Enum):
    """Quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    FAILED = "failed"


@dataclass
class QualityMetric:
    """Represents a single quality metric measurement."""
    metric_name: str
    value: float  # Normalized 0-1 score
    weight: float = 1.0
    description: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalQualityAssessment:
    """Assessment of retrieval quality for a query."""
    query: str
    retrieved_documents: List[Dict[str, Any]]
    relevance_scores: List[float] = field(default_factory=list)
    precision_at_k: Dict[int, float] = field(default_factory=dict)
    mathematical_accuracy: float = 0.0
    citation_coverage: float = 0.0
    content_coherence: float = 0.0
    overall_quality: QualityLevel = QualityLevel.POOR
    assessment_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CitationValidationResult:
    """Result of citation validation process."""
    citation: Citation
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    source_accessibility: bool = False
    metadata_completeness: float = 0.0
    format_compliance: bool = False


@dataclass
class ContentQualityScore:
    """Comprehensive content quality assessment."""
    document_id: str
    overall_score: float = 0.0  # 0-1 scale
    quality_level: QualityLevel = QualityLevel.POOR
    individual_metrics: List[QualityMetric] = field(default_factory=list)
    mathematical_preservation: float = 0.0
    citation_quality: float = 0.0
    structural_integrity: float = 0.0
    readability_score: float = 0.0
    academic_rigor: float = 0.0
    assessment_details: Dict[str, Any] = field(default_factory=dict)


class RetrievalQualityValidator:
    """Validates the quality of retrieval results for academic content."""
    
    def __init__(self, ragflow_client: Optional[RAGFlowClient] = None):
        """Initialize retrieval quality validator."""
        self.ragflow_client = ragflow_client
        self._setup_quality_thresholds()
        self._mathematical_keywords = self._setup_mathematical_keywords()
    
    def _setup_quality_thresholds(self) -> None:
        """Set up quality assessment thresholds."""
        self.thresholds = {
            'relevance': {
                'excellent': 0.9,
                'good': 0.75,
                'acceptable': 0.6,
                'poor': 0.4,
            },
            'mathematical_accuracy': {
                'excellent': 0.95,
                'good': 0.85,
                'acceptable': 0.7,
                'poor': 0.5,
            },
            'citation_coverage': {
                'excellent': 0.9,
                'good': 0.75,
                'acceptable': 0.6,
                'poor': 0.4,
            },
            'content_coherence': {
                'excellent': 0.85,
                'good': 0.7,
                'acceptable': 0.55,
                'poor': 0.4,
            }
        }
    
    def _setup_mathematical_keywords(self) -> Set[str]:
        """Set up mathematical keywords for accuracy assessment."""
        return {
            'theorem', 'proof', 'lemma', 'corollary', 'definition', 'proposition',
            'equation', 'formula', 'function', 'derivative', 'integral', 'matrix',
            'probability', 'statistics', 'algebra', 'calculus', 'geometry',
            'topology', 'analysis', 'optimization', 'algorithm', 'complexity'
        }
    
    def assess_retrieval_quality(self, query: str, 
                               retrieved_documents: List[Dict[str, Any]],
                               ground_truth: Optional[List[str]] = None) -> RetrievalQualityAssessment:
        """
        Assess the quality of retrieval results.
        
        Args:
            query: Original query
            retrieved_documents: List of retrieved documents with metadata
            ground_truth: Optional list of known relevant document IDs
            
        Returns:
            Comprehensive quality assessment
        """
        logger.info(f"Assessing retrieval quality for query: {query[:50]}...")
        
        try:
            assessment = RetrievalQualityAssessment(
                query=query,
                retrieved_documents=retrieved_documents
            )
            
            # Calculate relevance scores
            assessment.relevance_scores = self._calculate_relevance_scores(
                query, retrieved_documents
            )
            
            # Calculate precision at different k values
            assessment.precision_at_k = self._calculate_precision_at_k(
                retrieved_documents, ground_truth
            )
            
            # Assess mathematical accuracy
            assessment.mathematical_accuracy = self._assess_mathematical_accuracy(
                query, retrieved_documents
            )
            
            # Assess citation coverage
            assessment.citation_coverage = self._assess_citation_coverage(
                query, retrieved_documents
            )
            
            # Assess content coherence
            assessment.content_coherence = self._assess_content_coherence(
                retrieved_documents
            )
            
            # Determine overall quality level
            assessment.overall_quality = self._determine_overall_quality(assessment)
            
            logger.info(f"Retrieval quality assessment completed: {assessment.overall_quality.value}")
            
            return assessment
            
        except Exception as e:
            logger.error(f"Error assessing retrieval quality: {e}")
            return RetrievalQualityAssessment(query=query, retrieved_documents=[])
    
    def _calculate_relevance_scores(self, query: str, 
                                   documents: List[Dict[str, Any]]) -> List[float]:
        """Calculate relevance scores for retrieved documents."""
        relevance_scores = []
        query_terms = set(query.lower().split())
        
        for doc in documents:
            content = doc.get('content', '').lower()
            title = doc.get('title', '').lower()
            
            # Simple term overlap scoring (could be enhanced with embeddings)
            content_terms = set(content.split())
            title_terms = set(title.split())
            
            # Score based on term overlap
            content_overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
            title_overlap = len(query_terms & title_terms) / max(len(query_terms), 1)
            
            # Weight title matches higher
            relevance_score = 0.3 * title_overlap + 0.7 * content_overlap
            
            # Boost for mathematical content if query contains math terms
            if any(term in self._mathematical_keywords for term in query_terms):
                math_terms_in_doc = len(self._mathematical_keywords & content_terms)
                math_boost = min(math_terms_in_doc / 10.0, 0.2)  # Max 0.2 boost
                relevance_score += math_boost
            
            relevance_scores.append(min(relevance_score, 1.0))
        
        return relevance_scores
    
    def _calculate_precision_at_k(self, documents: List[Dict[str, Any]], 
                                 ground_truth: Optional[List[str]]) -> Dict[int, float]:
        """Calculate precision at different k values."""
        precision_at_k = {}
        
        if not ground_truth:
            # If no ground truth, use relevance threshold
            relevant_docs = len([doc for doc in documents 
                               if doc.get('score', 0) > 0.5])
            for k in [1, 5, 10, 20]:
                if k <= len(documents):
                    precision_at_k[k] = min(relevant_docs / k, 1.0)
        else:
            # Use ground truth for precision calculation
            for k in [1, 5, 10, 20]:
                if k <= len(documents):
                    top_k_docs = documents[:k]
                    relevant_in_top_k = sum(1 for doc in top_k_docs 
                                          if doc.get('id') in ground_truth)
                    precision_at_k[k] = relevant_in_top_k / k
        
        return precision_at_k
    
    def _assess_mathematical_accuracy(self, query: str, 
                                    documents: List[Dict[str, Any]]) -> float:
        """Assess mathematical accuracy of retrieved content."""
        if not any(term in self._mathematical_keywords 
                  for term in query.lower().split()):
            return 1.0  # Not a mathematical query
        
        accuracy_scores = []
        
        for doc in documents:
            content = doc.get('content', '')
            
            # Check for mathematical notation preservation
            latex_patterns = [r'\$[^$]+\$', r'\$\$[^$]+\$\$', r'\\[a-zA-Z]+\{']
            math_notation_count = sum(len(re.findall(pattern, content)) 
                                    for pattern in latex_patterns)
            
            # Score based on mathematical content density
            content_length = len(content.split())
            math_density = min(math_notation_count / max(content_length / 100, 1), 1.0)
            
            # Check for mathematical terms
            math_terms = sum(1 for word in content.lower().split() 
                           if word in self._mathematical_keywords)
            math_term_density = min(math_terms / max(content_length / 50, 1), 1.0)
            
            accuracy_score = 0.6 * math_notation_count + 0.4 * math_term_density
            accuracy_scores.append(min(accuracy_score, 1.0))
        
        return statistics.mean(accuracy_scores) if accuracy_scores else 0.0
    
    def _assess_citation_coverage(self, query: str, 
                                documents: List[Dict[str, Any]]) -> float:
        """Assess citation coverage in retrieved documents."""
        citation_scores = []
        
        for doc in documents:
            content = doc.get('content', '')
            
            # Count different citation patterns
            citation_patterns = [
                r'\([A-Z][a-z]+,?\s+\d{4}\)',  # Author-year citations
                r'\[\d+\]',  # Numbered citations
                r'\\cite\{[^}]+\}',  # LaTeX citations
            ]
            
            citation_count = sum(len(re.findall(pattern, content)) 
                               for pattern in citation_patterns)
            
            # Score based on citation density
            content_length = len(content.split())
            citation_density = min(citation_count / max(content_length / 200, 1), 1.0)
            
            citation_scores.append(citation_density)
        
        return statistics.mean(citation_scores) if citation_scores else 0.0
    
    def _assess_content_coherence(self, documents: List[Dict[str, Any]]) -> float:
        """Assess coherence of retrieved content."""
        if len(documents) < 2:
            return 1.0
        
        coherence_scores = []
        
        # Check for topic coherence across documents
        all_content = ' '.join(doc.get('content', '') for doc in documents)
        all_terms = set(all_content.lower().split())
        
        for doc in documents:
            content = doc.get('content', '')
            doc_terms = set(content.lower().split())
            
            # Calculate term overlap with overall corpus
            overlap = len(doc_terms & all_terms) / max(len(doc_terms), 1)
            coherence_scores.append(overlap)
        
        # Lower variance in overlap scores indicates better coherence
        if coherence_scores:
            mean_coherence = statistics.mean(coherence_scores)
            coherence_variance = statistics.variance(coherence_scores) if len(coherence_scores) > 1 else 0
            coherence_score = mean_coherence * (1 - min(coherence_variance, 0.5))
            return coherence_score
        
        return 0.0
    
    def _determine_overall_quality(self, assessment: RetrievalQualityAssessment) -> QualityLevel:
        """Determine overall quality level based on individual metrics."""
        
        # Calculate weighted average of quality metrics
        weights = {
            'relevance': 0.3,
            'mathematical_accuracy': 0.25,
            'citation_coverage': 0.2,
            'content_coherence': 0.25,
        }
        
        avg_relevance = statistics.mean(assessment.relevance_scores) if assessment.relevance_scores else 0
        
        overall_score = (
            weights['relevance'] * avg_relevance +
            weights['mathematical_accuracy'] * assessment.mathematical_accuracy +
            weights['citation_coverage'] * assessment.citation_coverage +
            weights['content_coherence'] * assessment.content_coherence
        )
        
        # Map to quality levels
        if overall_score >= self.thresholds['relevance']['excellent']:
            return QualityLevel.EXCELLENT
        elif overall_score >= self.thresholds['relevance']['good']:
            return QualityLevel.GOOD
        elif overall_score >= self.thresholds['relevance']['acceptable']:
            return QualityLevel.ACCEPTABLE
        elif overall_score >= self.thresholds['relevance']['poor']:
            return QualityLevel.POOR
        else:
            return QualityLevel.FAILED


class CitationValidator:
    """Validates citations in academic papers."""
    
    def __init__(self):
        """Initialize citation validator."""
        self._setup_validation_rules()
    
    def _setup_validation_rules(self) -> None:
        """Set up citation validation rules."""
        
        # Required fields for different citation types
        self.required_fields = {
            'paper': ['authors', 'title', 'year'],
            'book': ['authors', 'title', 'year'],
            'journal': ['authors', 'title', 'venue', 'year'],
            'conference': ['authors', 'title', 'venue', 'year'],
            'website': ['title', 'url'],
        }
        
        # Validation patterns
        self.validation_patterns = {
            'year': re.compile(r'^(19|20)\d{2}$'),
            'doi': re.compile(r'^10\.\d{4,}/[^\s]+$'),
            'url': re.compile(r'^https?://[^\s<>"\'()]+$'),
            'pages': re.compile(r'^\d+(-\d+)?$'),
        }
    
    def validate_citation(self, citation: Citation) -> CitationValidationResult:
        """
        Validate a single citation.
        
        Args:
            citation: Citation to validate
            
        Returns:
            Validation result with details
        """
        result = CitationValidationResult(citation=citation)
        
        try:
            # Check metadata completeness
            result.metadata_completeness = self._assess_metadata_completeness(citation)
            
            # Check format compliance
            result.format_compliance = self._check_format_compliance(citation)
            
            # Check source accessibility (if URL/DOI provided)
            result.source_accessibility = self._check_source_accessibility(citation)
            
            # Calculate overall confidence score
            result.confidence_score = self._calculate_confidence_score(citation, result)
            
            # Determine if citation is valid
            result.is_valid = (
                result.metadata_completeness >= 0.7 and
                result.format_compliance and
                result.confidence_score >= 0.6
            )
            
            if not result.is_valid:
                result.validation_errors = self._identify_validation_errors(citation, result)
            
            logger.debug(f"Validated citation {citation.key}: {result.is_valid}")
            
        except Exception as e:
            logger.error(f"Error validating citation {citation.key}: {e}")
            result.validation_errors.append(f"Validation error: {e}")
        
        return result
    
    def _assess_metadata_completeness(self, citation: Citation) -> float:
        """Assess completeness of citation metadata."""
        required_fields = self.required_fields.get(citation.citation_type, 
                                                  self.required_fields['paper'])
        
        completed_fields = 0
        total_fields = len(required_fields)
        
        for field in required_fields:
            if field == 'authors' and citation.authors:
                completed_fields += 1
            elif field == 'title' and citation.title:
                completed_fields += 1
            elif field == 'venue' and citation.venue:
                completed_fields += 1
            elif field == 'year' and citation.year:
                completed_fields += 1
            elif field == 'url' and citation.url:
                completed_fields += 1
        
        return completed_fields / total_fields if total_fields > 0 else 0.0
    
    def _check_format_compliance(self, citation: Citation) -> bool:
        """Check if citation follows format rules."""
        
        # Check year format
        if citation.year:
            if not self.validation_patterns['year'].match(str(citation.year)):
                return False
        
        # Check DOI format
        if citation.doi:
            if not self.validation_patterns['doi'].match(citation.doi):
                return False
        
        # Check URL format
        if citation.url:
            if not self.validation_patterns['url'].match(citation.url):
                return False
        
        # Check pages format
        if citation.pages:
            if not self.validation_patterns['pages'].match(citation.pages):
                return False
        
        return True
    
    def _check_source_accessibility(self, citation: Citation) -> bool:
        """Check if source is accessible (simplified check)."""
        # In a real implementation, this would make HTTP requests
        # For now, just check if URL/DOI is provided
        return bool(citation.url or citation.doi)
    
    def _calculate_confidence_score(self, citation: Citation, 
                                   result: CitationValidationResult) -> float:
        """Calculate overall confidence score for citation."""
        score = 0.0
        
        # Metadata completeness weight: 40%
        score += 0.4 * result.metadata_completeness
        
        # Format compliance weight: 30%
        score += 0.3 * (1.0 if result.format_compliance else 0.0)
        
        # Source accessibility weight: 20%
        score += 0.2 * (1.0 if result.source_accessibility else 0.0)
        
        # Additional quality indicators weight: 10%
        quality_indicators = 0.0
        if citation.title and len(citation.title) > 10:
            quality_indicators += 0.3
        if citation.authors and len(citation.authors) > 0:
            quality_indicators += 0.4
        if citation.venue:
            quality_indicators += 0.3
        
        score += 0.1 * quality_indicators
        
        return min(score, 1.0)
    
    def _identify_validation_errors(self, citation: Citation, 
                                  result: CitationValidationResult) -> List[str]:
        """Identify specific validation errors."""
        errors = []
        
        if result.metadata_completeness < 0.7:
            errors.append("Incomplete metadata: missing required fields")
        
        if not result.format_compliance:
            errors.append("Format compliance issues detected")
        
        if not result.source_accessibility:
            errors.append("Source not accessible: no valid URL or DOI")
        
        if not citation.authors:
            errors.append("Missing author information")
        
        if not citation.title:
            errors.append("Missing title")
        
        if not citation.year:
            errors.append("Missing publication year")
        
        return errors


class ContentQualityAssessor:
    """Assesses overall content quality for academic papers."""
    
    def __init__(self):
        """Initialize content quality assessor."""
        self._setup_quality_metrics()
        self.latex_renderer = LatexRenderer()
    
    def _setup_quality_metrics(self) -> None:
        """Set up quality assessment metrics."""
        
        # Metric weights for overall score calculation
        self.metric_weights = {
            'mathematical_preservation': 0.25,
            'citation_quality': 0.2,
            'structural_integrity': 0.2,
            'readability': 0.15,
            'academic_rigor': 0.2,
        }
    
    def assess_content_quality(self, paper_structure: AcademicPaperStructure,
                              mathematical_index: Optional[MathematicalIndex] = None) -> ContentQualityScore:
        """
        Assess overall content quality of an academic paper.
        
        Args:
            paper_structure: Processed paper structure
            mathematical_index: Optional mathematical index
            
        Returns:
            Comprehensive quality assessment
        """
        logger.info(f"Assessing content quality for paper: {paper_structure.title or 'Unknown'}")
        
        try:
            score = ContentQualityScore(
                document_id=paper_structure.title or "unknown",
                individual_metrics=[]
            )
            
            # Assess mathematical preservation
            math_metric = self._assess_mathematical_preservation(
                paper_structure, mathematical_index
            )
            score.individual_metrics.append(math_metric)
            score.mathematical_preservation = math_metric.value
            
            # Assess citation quality
            citation_metric = self._assess_citation_quality(paper_structure)
            score.individual_metrics.append(citation_metric)
            score.citation_quality = citation_metric.value
            
            # Assess structural integrity
            structure_metric = self._assess_structural_integrity(paper_structure)
            score.individual_metrics.append(structure_metric)
            score.structural_integrity = structure_metric.value
            
            # Assess readability
            readability_metric = self._assess_readability(paper_structure)
            score.individual_metrics.append(readability_metric)
            score.readability_score = readability_metric.value
            
            # Assess academic rigor
            rigor_metric = self._assess_academic_rigor(paper_structure)
            score.individual_metrics.append(rigor_metric)
            score.academic_rigor = rigor_metric.value
            
            # Calculate overall score
            score.overall_score = self._calculate_overall_score(score)
            score.quality_level = self._determine_quality_level(score.overall_score)
            
            logger.info(f"Content quality assessment completed: {score.quality_level.value}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error assessing content quality: {e}")
            return ContentQualityScore(document_id="error")
    
    def _assess_mathematical_preservation(self, paper_structure: AcademicPaperStructure,
                                        mathematical_index: Optional[MathematicalIndex]) -> QualityMetric:
        """Assess preservation of mathematical content."""
        
        total_math_elements = len(paper_structure.mathematical_elements)
        if total_math_elements == 0:
            return QualityMetric(
                metric_name="mathematical_preservation",
                value=1.0,  # Perfect if no math content
                description="No mathematical content to preserve"
            )
        
        # Check if mathematical notation is preserved
        preserved_notation = 0
        rendering_errors = 0
        
        for element in paper_structure.mathematical_elements:
            try:
                # Test LaTeX rendering
                rendered = self.latex_renderer.render_latex(element.content)
                if rendered != element.content:  # Some rendering happened
                    preserved_notation += 1
            except Exception:
                rendering_errors += 1
        
        preservation_score = preserved_notation / max(total_math_elements, 1)
        error_penalty = rendering_errors / max(total_math_elements, 1)
        final_score = max(0, preservation_score - 0.5 * error_penalty)
        
        return QualityMetric(
            metric_name="mathematical_preservation",
            value=final_score,
            description=f"Mathematical notation preservation score",
            details={
                'total_elements': total_math_elements,
                'preserved_notation': preserved_notation,
                'rendering_errors': rendering_errors,
            }
        )
    
    def _assess_citation_quality(self, paper_structure: AcademicPaperStructure) -> QualityMetric:
        """Assess quality of citations."""
        
        total_citations = len(paper_structure.citations)
        if total_citations == 0:
            return QualityMetric(
                metric_name="citation_quality",
                value=0.5,  # Neutral if no citations
                description="No citations found"
            )
        
        validator = CitationValidator()
        valid_citations = 0
        total_confidence = 0.0
        
        for citation in paper_structure.citations.values():
            result = validator.validate_citation(citation)
            if result.is_valid:
                valid_citations += 1
            total_confidence += result.confidence_score
        
        validity_score = valid_citations / total_citations
        avg_confidence = total_confidence / total_citations
        
        # Combine validity and confidence
        citation_score = 0.6 * validity_score + 0.4 * avg_confidence
        
        return QualityMetric(
            metric_name="citation_quality",
            value=citation_score,
            description=f"Citation quality assessment",
            details={
                'total_citations': total_citations,
                'valid_citations': valid_citations,
                'average_confidence': avg_confidence,
            }
        )
    
    def _assess_structural_integrity(self, paper_structure: AcademicPaperStructure) -> QualityMetric:
        """Assess structural integrity of the paper."""
        
        integrity_score = 0.0
        max_score = 0.0
        
        # Check for essential sections
        essential_elements = {
            'title': paper_structure.title,
            'authors': paper_structure.authors,
            'abstract': paper_structure.abstract,
            'sections': paper_structure.sections,
        }
        
        for element, value in essential_elements.items():
            max_score += 1.0
            if value:
                if element == 'sections' and len(value) > 0:
                    integrity_score += 1.0
                elif element != 'sections' and value:
                    integrity_score += 1.0
        
        # Check cross-reference integrity
        cross_refs = paper_structure.cross_references
        if cross_refs:
            max_score += 1.0
            # Simple check: do we have both labels and references?
            labels = [ref.label for ref in cross_refs.values()]
            if labels:
                integrity_score += 1.0
        
        final_score = integrity_score / max(max_score, 1.0)
        
        return QualityMetric(
            metric_name="structural_integrity",
            value=final_score,
            description="Document structural integrity",
            details={
                'has_title': bool(paper_structure.title),
                'has_authors': bool(paper_structure.authors),
                'has_abstract': bool(paper_structure.abstract),
                'section_count': len(paper_structure.sections),
                'cross_reference_count': len(paper_structure.cross_references),
            }
        )
    
    def _assess_readability(self, paper_structure: AcademicPaperStructure) -> QualityMetric:
        """Assess readability of the content."""
        
        # Combine all text content
        all_text = ""
        if paper_structure.abstract:
            all_text += paper_structure.abstract + " "
        for section_content in paper_structure.sections.values():
            all_text += section_content + " "
        
        if not all_text.strip():
            return QualityMetric(
                metric_name="readability",
                value=0.0,
                description="No readable content found"
            )
        
        # Simple readability metrics
        sentences = len(re.findall(r'[.!?]+', all_text))
        words = len(all_text.split())
        
        if sentences == 0:
            avg_sentence_length = 0
        else:
            avg_sentence_length = words / sentences
        
        # Optimal sentence length for academic writing: 15-25 words
        if 15 <= avg_sentence_length <= 25:
            sentence_score = 1.0
        elif 10 <= avg_sentence_length <= 30:
            sentence_score = 0.8
        else:
            sentence_score = 0.6
        
        # Check for academic vocabulary
        academic_terms = {'however', 'therefore', 'furthermore', 'moreover', 
                         'consequently', 'nevertheless', 'specifically', 'particularly'}
        academic_term_count = sum(1 for word in all_text.lower().split() 
                                 if word in academic_terms)
        academic_density = min(academic_term_count / max(words / 100, 1), 1.0)
        
        # Combine readability factors
        readability_score = 0.6 * sentence_score + 0.4 * academic_density
        
        return QualityMetric(
            metric_name="readability",
            value=readability_score,
            description="Content readability assessment",
            details={
                'word_count': words,
                'sentence_count': sentences,
                'avg_sentence_length': avg_sentence_length,
                'academic_term_density': academic_density,
            }
        )
    
    def _assess_academic_rigor(self, paper_structure: AcademicPaperStructure) -> QualityMetric:
        """Assess academic rigor of the paper."""
        
        rigor_score = 0.0
        max_score = 0.0
        
        # Mathematical rigor
        math_elements = len(paper_structure.mathematical_elements)
        max_score += 1.0
        if math_elements > 0:
            # Higher score for more mathematical content
            math_score = min(math_elements / 10.0, 1.0)
            rigor_score += math_score
        
        # Citation rigor
        citations = len(paper_structure.citations)
        max_score += 1.0
        if citations > 0:
            # Score based on citation density
            citation_score = min(citations / 20.0, 1.0)
            rigor_score += citation_score
        
        # Methodological rigor (based on structure)
        sections = paper_structure.sections
        max_score += 1.0
        methodological_sections = {'methodology', 'methods', 'approach', 
                                 'experimental', 'analysis', 'results'}
        method_sections_found = sum(1 for section in sections.keys() 
                                   if any(term in section.lower() 
                                        for term in methodological_sections))
        if method_sections_found > 0:
            rigor_score += min(method_sections_found / 3.0, 1.0)
        
        final_score = rigor_score / max(max_score, 1.0)
        
        return QualityMetric(
            metric_name="academic_rigor",
            value=final_score,
            description="Academic rigor assessment",
            details={
                'mathematical_elements': math_elements,
                'citation_count': citations,
                'methodological_sections': method_sections_found,
            }
        )
    
    def _calculate_overall_score(self, score: ContentQualityScore) -> float:
        """Calculate weighted overall quality score."""
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric in score.individual_metrics:
            weight = self.metric_weights.get(metric.metric_name, 0.0)
            total_score += metric.value * weight
            total_weight += weight
        
        return total_score / max(total_weight, 1.0)
    
    def _determine_quality_level(self, overall_score: float) -> QualityLevel:
        """Determine quality level from overall score."""
        
        if overall_score >= 0.9:
            return QualityLevel.EXCELLENT
        elif overall_score >= 0.75:
            return QualityLevel.GOOD
        elif overall_score >= 0.6:
            return QualityLevel.ACCEPTABLE
        elif overall_score >= 0.4:
            return QualityLevel.POOR
        else:
            return QualityLevel.FAILED


class QualityAssurancePipeline:
    """Main quality assurance pipeline combining all QA components."""
    
    def __init__(self, ragflow_client: Optional[RAGFlowClient] = None):
        """Initialize quality assurance pipeline."""
        self.retrieval_validator = RetrievalQualityValidator(ragflow_client)
        self.citation_validator = CitationValidator()
        self.content_assessor = ContentQualityAssessor()
        
        # QA statistics
        self._processed_documents = 0
        self._quality_assessments = []
        self._validation_results = []
    
    def run_comprehensive_qa(self, paper_structure: AcademicPaperStructure,
                           retrieval_results: Optional[List[Dict[str, Any]]] = None,
                           mathematical_index: Optional[MathematicalIndex] = None,
                           query: Optional[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive quality assurance on academic paper processing.
        
        Args:
            paper_structure: Processed paper structure
            retrieval_results: Optional retrieval results to validate
            mathematical_index: Optional mathematical index
            query: Optional query used for retrieval
            
        Returns:
            Comprehensive QA report
        """
        logger.info("Running comprehensive quality assurance...")
        
        qa_report = {
            'document_id': paper_structure.title or "unknown",
            'timestamp': datetime.now().isoformat(),
            'content_quality': None,
            'citation_validation': None,
            'retrieval_quality': None,
            'overall_assessment': None,
        }
        
        try:
            # Content quality assessment
            content_quality = self.content_assessor.assess_content_quality(
                paper_structure, mathematical_index
            )
            qa_report['content_quality'] = content_quality
            
            # Citation validation
            citation_results = []
            for citation in paper_structure.citations.values():
                result = self.citation_validator.validate_citation(citation)
                citation_results.append(result)
            qa_report['citation_validation'] = citation_results
            
            # Retrieval quality assessment (if applicable)
            if retrieval_results and query:
                retrieval_quality = self.retrieval_validator.assess_retrieval_quality(
                    query, retrieval_results
                )
                qa_report['retrieval_quality'] = retrieval_quality
            
            # Overall assessment
            qa_report['overall_assessment'] = self._generate_overall_assessment(qa_report)
            
            # Update statistics
            self._processed_documents += 1
            self._quality_assessments.append(content_quality)
            self._validation_results.extend(citation_results)
            
            logger.info(f"QA completed: {qa_report['overall_assessment']['quality_level']}")
            
        except Exception as e:
            logger.error(f"Error in comprehensive QA: {e}")
            qa_report['error'] = str(e)
        
        return qa_report
    
    def _generate_overall_assessment(self, qa_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment from individual QA components."""
        
        scores = []
        issues = []
        recommendations = []
        
        # Content quality contribution
        content_quality = qa_report.get('content_quality')
        if content_quality:
            scores.append(content_quality.overall_score)
            if content_quality.quality_level in [QualityLevel.POOR, QualityLevel.FAILED]:
                issues.append(f"Poor content quality: {content_quality.quality_level.value}")
                recommendations.append("Review mathematical notation and structural integrity")
        
        # Citation validation contribution
        citation_results = qa_report.get('citation_validation', [])
        if citation_results:
            valid_citations = sum(1 for result in citation_results if result.is_valid)
            citation_score = valid_citations / len(citation_results)
            scores.append(citation_score)
            
            if citation_score < 0.7:
                issues.append(f"Citation quality issues: {citation_score:.1%} valid")
                recommendations.append("Review and improve citation metadata completeness")
        
        # Retrieval quality contribution
        retrieval_quality = qa_report.get('retrieval_quality')
        if retrieval_quality:
            retrieval_score = statistics.mean(retrieval_quality.relevance_scores) if retrieval_quality.relevance_scores else 0
            scores.append(retrieval_score)
            
            if retrieval_quality.overall_quality in [QualityLevel.POOR, QualityLevel.FAILED]:
                issues.append(f"Poor retrieval quality: {retrieval_quality.overall_quality.value}")
                recommendations.append("Improve retrieval configuration and indexing")
        
        # Calculate overall score
        overall_score = statistics.mean(scores) if scores else 0.0
        
        # Determine quality level
        if overall_score >= 0.9:
            quality_level = QualityLevel.EXCELLENT
        elif overall_score >= 0.75:
            quality_level = QualityLevel.GOOD
        elif overall_score >= 0.6:
            quality_level = QualityLevel.ACCEPTABLE
        elif overall_score >= 0.4:
            quality_level = QualityLevel.POOR
        else:
            quality_level = QualityLevel.FAILED
        
        return {
            'overall_score': overall_score,
            'quality_level': quality_level.value,
            'component_scores': {
                'content_quality': content_quality.overall_score if content_quality else None,
                'citation_quality': citation_score if citation_results else None,
                'retrieval_quality': retrieval_score if retrieval_quality else None,
            },
            'issues_identified': issues,
            'recommendations': recommendations,
            'total_components_assessed': len(scores),
        }
    
    def get_qa_statistics(self) -> Dict[str, Any]:
        """Get quality assurance statistics."""
        
        if not self._quality_assessments:
            return {
                'total_documents_processed': self._processed_documents,
                'average_quality_score': 0.0,
                'quality_distribution': {},
                'common_issues': [],
            }
        
        # Calculate average scores
        avg_overall = statistics.mean([qa.overall_score for qa in self._quality_assessments])
        avg_math = statistics.mean([qa.mathematical_preservation for qa in self._quality_assessments])
        avg_citation = statistics.mean([qa.citation_quality for qa in self._quality_assessments])
        
        # Quality level distribution
        quality_distribution = Counter([qa.quality_level.value for qa in self._quality_assessments])
        
        # Identify common issues
        common_issues = []
        if avg_math < 0.7:
            common_issues.append("Mathematical content preservation issues")
        if avg_citation < 0.7:
            common_issues.append("Citation quality problems")
        
        return {
            'total_documents_processed': self._processed_documents,
            'average_quality_score': avg_overall,
            'average_mathematical_preservation': avg_math,
            'average_citation_quality': avg_citation,
            'quality_distribution': dict(quality_distribution),
            'common_issues': common_issues,
            'total_citations_validated': len(self._validation_results),
            'citation_validation_rate': sum(1 for r in self._validation_results if r.is_valid) / max(len(self._validation_results), 1),
        }
    
    def export_qa_report(self, qa_report: Dict[str, Any], output_path: Path) -> None:
        """Export QA report to JSON file."""
        try:
            # Convert dataclasses to dictionaries for JSON serialization
            serializable_report = self._make_serializable(qa_report)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported QA report to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting QA report: {e}")
    
    def _make_serializable(self, obj: Any) -> Any:
        """Convert complex objects to JSON-serializable format."""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # Convert dataclass or object to dict
            return self._make_serializable(obj.__dict__)
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj


# Convenience functions
def run_quality_assurance(paper_structure: AcademicPaperStructure,
                         retrieval_results: Optional[List[Dict[str, Any]]] = None,
                         mathematical_index: Optional[MathematicalIndex] = None,
                         query: Optional[str] = None) -> Dict[str, Any]:
    """Run comprehensive quality assurance on academic paper processing."""
    pipeline = QualityAssurancePipeline()
    return pipeline.run_comprehensive_qa(paper_structure, retrieval_results, mathematical_index, query)


def validate_citations(citations: List[Citation]) -> List[CitationValidationResult]:
    """Validate a list of citations."""
    validator = CitationValidator()
    return [validator.validate_citation(citation) for citation in citations] 