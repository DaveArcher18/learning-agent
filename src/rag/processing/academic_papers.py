"""
Academic Paper Processing Pipeline for Learning Agent.

This module provides specialized processing for academic papers including:
- Citation network analysis and reference extraction
- Theorem/proof/definition semantic classification  
- Bibliography and cross-reference management
- Academic content structure recognition

Designed for maintainability, modularity, simplicity, and observability.
"""

import re
import logging
from typing import Dict, List, Optional, Set, Tuple, NamedTuple
from dataclasses import dataclass, field
from pathlib import Path
import json
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


@dataclass
class Citation:
    """Represents a single citation in an academic paper."""
    key: str  # Citation key (e.g., "Smith2023")
    text: str  # Full citation text
    authors: List[str] = field(default_factory=list)
    title: Optional[str] = None
    venue: Optional[str] = None  # Journal/conference
    year: Optional[int] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citation_type: str = "unknown"  # paper, book, website, etc.


@dataclass
class CrossReference:
    """Represents a cross-reference within the document."""
    ref_type: str  # theorem, definition, figure, table, section, equation
    label: str  # LaTeX label
    number: Optional[str] = None  # Display number (e.g., "3.1")
    title: Optional[str] = None
    content: Optional[str] = None


@dataclass
class MathematicalElement:
    """Represents a mathematical element (theorem, proof, definition, etc.)."""
    element_type: str  # theorem, proof, definition, lemma, corollary, example
    label: Optional[str] = None
    number: Optional[str] = None
    title: Optional[str] = None
    content: str = ""
    dependencies: List[str] = field(default_factory=list)  # Referenced elements
    mathematical_notation: List[str] = field(default_factory=list)


@dataclass 
class AcademicPaperStructure:
    """Complete structure of an academic paper."""
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    sections: Dict[str, str] = field(default_factory=dict)
    citations: Dict[str, Citation] = field(default_factory=dict)
    cross_references: Dict[str, CrossReference] = field(default_factory=dict)
    mathematical_elements: List[MathematicalElement] = field(default_factory=list)
    figures: List[Dict] = field(default_factory=list)
    tables: List[Dict] = field(default_factory=list)
    bibliography: List[Citation] = field(default_factory=list)


class CitationExtractor:
    """Extracts and analyzes citations from academic papers."""
    
    def __init__(self):
        """Initialize citation extractor with regex patterns."""
        self._setup_patterns()
    
    def _setup_patterns(self) -> None:
        """Set up regex patterns for citation recognition."""
        
        # Common citation patterns
        self.citation_patterns = {
            # Author-year style: (Smith, 2023) or (Smith et al., 2023)
            'author_year': re.compile(
                r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?),?\s+(\d{4})\)'
            ),
            
            # Numbered citations: [1], [2,3], [1-5]
            'numbered': re.compile(r'\[(\d+(?:\s*[-,]\s*\d+)*)\]'),
            
            # LaTeX cite commands: \cite{key}, \citep{key}, \citet{key}
            'latex_cite': re.compile(
                r'\\(?:cite[pt]?|ref)\{([^}]+)\}'
            ),
            
            # DOI patterns
            'doi': re.compile(
                r'(?:doi:|DOI:|\bdoi\b)\s*([0-9a-zA-Z\./\-_\(\)]+)',
                re.IGNORECASE
            ),
            
            # URL patterns for citations
            'url': re.compile(
                r'https?://[^\s<>"\'()]+',
                re.IGNORECASE
            ),
        }
        
        # Bibliography entry patterns
        self.bib_patterns = {
            # Author, Title, Venue, Year pattern
            'standard': re.compile(
                r'([A-Z][^.]+)\.\s+([^.]+)\.\s+([^,]+),?\s+(\d{4})',
                re.MULTILINE
            ),
            
            # LaTeX bibliography entries
            'latex_bib': re.compile(
                r'\\bibitem\{([^}]+)\}\s*(.+?)(?=\\bibitem|\Z)',
                re.DOTALL
            ),
        }
    
    def extract_citations(self, text: str) -> List[Citation]:
        """
        Extract all citations from text.
        
        Args:
            text: Input text containing citations
            
        Returns:
            List of Citation objects found in text
        """
        citations = []
        
        try:
            # Extract different types of citations
            citations.extend(self._extract_author_year_citations(text))
            citations.extend(self._extract_numbered_citations(text))
            citations.extend(self._extract_latex_citations(text))
            
            logger.info(f"Extracted {len(citations)} citations from text")
            
        except Exception as e:
            logger.error(f"Error extracting citations: {e}")
        
        return citations
    
    def _extract_author_year_citations(self, text: str) -> List[Citation]:
        """Extract author-year style citations."""
        citations = []
        
        for match in self.citation_patterns['author_year'].finditer(text):
            author = match.group(1).strip()
            year = int(match.group(2))
            
            citation = Citation(
                key=f"{author}{year}",
                text=match.group(0),
                authors=[author],
                year=year,
                citation_type="author_year"
            )
            citations.append(citation)
        
        return citations
    
    def _extract_numbered_citations(self, text: str) -> List[Citation]:
        """Extract numbered citations like [1], [2,3]."""
        citations = []
        
        for match in self.citation_patterns['numbered'].finditer(text):
            numbers = match.group(1)
            citation = Citation(
                key=f"ref_{numbers}",
                text=match.group(0),
                citation_type="numbered"
            )
            citations.append(citation)
        
        return citations
    
    def _extract_latex_citations(self, text: str) -> List[Citation]:
        """Extract LaTeX citation commands."""
        citations = []
        
        for match in self.citation_patterns['latex_cite'].finditer(text):
            keys = match.group(1).split(',')
            
            for key in keys:
                key = key.strip()
                citation = Citation(
                    key=key,
                    text=match.group(0),
                    citation_type="latex"
                )
                citations.append(citation)
        
        return citations
    
    def build_citation_network(self, citations: List[Citation]) -> Dict[str, Set[str]]:
        """
        Build a citation network showing relationships between papers.
        
        Args:
            citations: List of citations to analyze
            
        Returns:
            Dict mapping citation keys to sets of related citations
        """
        network = defaultdict(set)
        
        # Group citations by proximity in text (simple heuristic)
        citation_groups = self._group_nearby_citations(citations)
        
        for group in citation_groups:
            # Add bidirectional connections within each group
            for i, cite1 in enumerate(group):
                for cite2 in group[i+1:]:
                    network[cite1.key].add(cite2.key)
                    network[cite2.key].add(cite1.key)
        
        logger.info(f"Built citation network with {len(network)} nodes")
        return dict(network)
    
    def _group_nearby_citations(self, citations: List[Citation]) -> List[List[Citation]]:
        """Group citations that appear close to each other in text."""
        # Simplified grouping - in practice, would use text positions
        groups = []
        current_group = []
        
        for citation in citations:
            if not current_group:
                current_group = [citation]
            else:
                # Simple heuristic: group if same citation type
                if citation.citation_type == current_group[-1].citation_type:
                    current_group.append(citation)
                else:
                    if len(current_group) > 1:
                        groups.append(current_group)
                    current_group = [citation]
        
        if len(current_group) > 1:
            groups.append(current_group)
        
        return groups


class MathematicalElementClassifier:
    """Classifies and extracts mathematical elements from academic papers."""
    
    def __init__(self):
        """Initialize classifier with mathematical element patterns."""
        self._setup_patterns()
    
    def _setup_patterns(self) -> None:
        """Set up patterns for recognizing mathematical elements."""
        
        # LaTeX theorem-like environments
        self.theorem_patterns = {
            'theorem': re.compile(
                r'\\begin\{theorem\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{theorem\}',
                re.DOTALL | re.IGNORECASE
            ),
            'proof': re.compile(
                r'\\begin\{proof\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{proof\}',
                re.DOTALL | re.IGNORECASE
            ),
            'definition': re.compile(
                r'\\begin\{definition\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{definition\}',
                re.DOTALL | re.IGNORECASE
            ),
            'lemma': re.compile(
                r'\\begin\{lemma\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{lemma\}',
                re.DOTALL | re.IGNORECASE
            ),
            'corollary': re.compile(
                r'\\begin\{corollary\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{corollary\}',
                re.DOTALL | re.IGNORECASE
            ),
            'example': re.compile(
                r'\\begin\{example\}(?:\[([^\]]+)\])?\s*(.*?)\\end\{example\}',
                re.DOTALL | re.IGNORECASE
            ),
        }
        
        # Patterns for mathematical notation extraction
        self.notation_patterns = {
            'equations': re.compile(r'\$\$?([^$]+)\$\$?'),
            'labels': re.compile(r'\\label\{([^}]+)\}'),
            'references': re.compile(r'\\(?:ref|eqref)\{([^}]+)\}'),
        }
    
    def classify_mathematical_elements(self, text: str) -> List[MathematicalElement]:
        """
        Extract and classify mathematical elements from text.
        
        Args:
            text: Input text containing mathematical elements
            
        Returns:
            List of classified mathematical elements
        """
        elements = []
        
        try:
            for element_type, pattern in self.theorem_patterns.items():
                elements.extend(self._extract_elements(text, element_type, pattern))
            
            logger.info(f"Classified {len(elements)} mathematical elements")
            
        except Exception as e:
            logger.error(f"Error classifying mathematical elements: {e}")
        
        return elements
    
    def _extract_elements(self, text: str, element_type: str, pattern: re.Pattern) -> List[MathematicalElement]:
        """Extract elements of a specific type using the given pattern."""
        elements = []
        
        for match in pattern.finditer(text):
            title = match.group(1) if match.lastindex > 1 else None
            content = match.group(2) if match.lastindex > 1 else match.group(1)
            
            # Extract mathematical notation from content
            notation = self._extract_mathematical_notation(content)
            
            # Extract dependencies (referenced elements)
            dependencies = self._extract_dependencies(content)
            
            element = MathematicalElement(
                element_type=element_type,
                title=title,
                content=content.strip(),
                mathematical_notation=notation,
                dependencies=dependencies
            )
            elements.append(element)
        
        return elements
    
    def _extract_mathematical_notation(self, text: str) -> List[str]:
        """Extract mathematical notation from text."""
        notation = []
        
        for match in self.notation_patterns['equations'].finditer(text):
            notation.append(match.group(1).strip())
        
        return notation
    
    def _extract_dependencies(self, text: str) -> List[str]:
        """Extract references to other mathematical elements."""
        dependencies = []
        
        for match in self.notation_patterns['references'].finditer(text):
            dependencies.append(match.group(1))
        
        return dependencies


class AcademicPaperProcessor:
    """Main processor for academic papers combining all analysis components."""
    
    def __init__(self):
        """Initialize academic paper processor."""
        self.citation_extractor = CitationExtractor()
        self.math_classifier = MathematicalElementClassifier()
        self._processed_papers = 0
        self._total_citations = 0
        self._total_math_elements = 0
    
    def process_paper(self, text: str, metadata: Optional[Dict] = None) -> AcademicPaperStructure:
        """
        Process a complete academic paper.
        
        Args:
            text: Full text of the academic paper
            metadata: Optional metadata about the paper
            
        Returns:
            AcademicPaperStructure with complete analysis
        """
        logger.info("Processing academic paper...")
        
        try:
            structure = AcademicPaperStructure()
            
            # Extract basic structure
            structure.title = self._extract_title(text)
            structure.authors = self._extract_authors(text)
            structure.abstract = self._extract_abstract(text)
            structure.sections = self._extract_sections(text)
            
            # Extract citations and build network
            citations = self.citation_extractor.extract_citations(text)
            structure.citations = {cite.key: cite for cite in citations}
            
            # Extract mathematical elements
            structure.mathematical_elements = self.math_classifier.classify_mathematical_elements(text)
            
            # Extract cross-references
            structure.cross_references = self._extract_cross_references(text)
            
            # Update statistics
            self._processed_papers += 1
            self._total_citations += len(citations)
            self._total_math_elements += len(structure.mathematical_elements)
            
            logger.info(f"Processed paper with {len(citations)} citations and "
                       f"{len(structure.mathematical_elements)} mathematical elements")
            
            return structure
            
        except Exception as e:
            logger.error(f"Error processing academic paper: {e}")
            return AcademicPaperStructure()
    
    def _extract_title(self, text: str) -> Optional[str]:
        """Extract paper title from text."""
        # Look for LaTeX title command
        title_match = re.search(r'\\title\{([^}]+)\}', text)
        if title_match:
            return title_match.group(1).strip()
        
        # Look for markdown title
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('# '):
                return line[2:].strip()
        
        return None
    
    def _extract_authors(self, text: str) -> List[str]:
        """Extract authors from text."""
        authors = []
        
        # Look for LaTeX author command
        author_match = re.search(r'\\author\{([^}]+)\}', text)
        if author_match:
            # Split by common separators
            author_text = author_match.group(1)
            authors = [name.strip() for name in re.split(r'[,&]|\\and', author_text)]
        
        return authors
    
    def _extract_abstract(self, text: str) -> Optional[str]:
        """Extract abstract from text."""
        # Look for LaTeX abstract environment
        abstract_match = re.search(
            r'\\begin\{abstract\}(.*?)\\end\{abstract\}',
            text, re.DOTALL
        )
        if abstract_match:
            return abstract_match.group(1).strip()
        
        # Look for markdown abstract
        lines = text.split('\n')
        in_abstract = False
        abstract_lines = []
        
        for line in lines:
            if 'abstract' in line.lower() and len(line) < 50:
                in_abstract = True
                continue
            if in_abstract:
                if line.strip() == '' and abstract_lines:
                    break
                if line.strip():
                    abstract_lines.append(line.strip())
        
        return ' '.join(abstract_lines) if abstract_lines else None
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract sections from text."""
        sections = {}
        
        # Look for LaTeX sections
        section_pattern = re.compile(
            r'\\(sub)*section\{([^}]+)\}(.*?)(?=\\(sub)*section|\Z)',
            re.DOTALL
        )
        
        for match in section_pattern.finditer(text):
            section_title = match.group(2)
            section_content = match.group(3).strip()
            sections[section_title] = section_content
        
        return sections
    
    def _extract_cross_references(self, text: str) -> Dict[str, CrossReference]:
        """Extract cross-references from text."""
        cross_refs = {}
        
        # Extract labels
        label_pattern = re.compile(r'\\label\{([^}]+)\}')
        ref_pattern = re.compile(r'\\(?:ref|eqref)\{([^}]+)\}')
        
        # Find all labels
        for match in label_pattern.finditer(text):
            label = match.group(1)
            # Determine type from context or label prefix
            ref_type = self._determine_ref_type(label)
            
            cross_ref = CrossReference(
                ref_type=ref_type,
                label=label
            )
            cross_refs[label] = cross_ref
        
        return cross_refs
    
    def _determine_ref_type(self, label: str) -> str:
        """Determine reference type from label."""
        label_lower = label.lower()
        
        if label_lower.startswith('eq:'):
            return 'equation'
        elif label_lower.startswith('fig:'):
            return 'figure'
        elif label_lower.startswith('tab:'):
            return 'table'
        elif label_lower.startswith('sec:'):
            return 'section'
        elif label_lower.startswith('thm:'):
            return 'theorem'
        elif label_lower.startswith('def:'):
            return 'definition'
        else:
            return 'unknown'
    
    def get_processing_statistics(self) -> Dict[str, int]:
        """Get statistics about processed papers."""
        return {
            'papers_processed': self._processed_papers,
            'total_citations_extracted': self._total_citations,
            'total_math_elements_classified': self._total_math_elements,
            'avg_citations_per_paper': (
                self._total_citations / max(1, self._processed_papers)
            ),
            'avg_math_elements_per_paper': (
                self._total_math_elements / max(1, self._processed_papers)
            ),
        }
    
    def export_structure(self, structure: AcademicPaperStructure, 
                        output_path: Path) -> None:
        """Export paper structure to JSON file."""
        try:
            # Convert to serializable format
            data = {
                'title': structure.title,
                'authors': structure.authors,
                'abstract': structure.abstract,
                'sections': structure.sections,
                'citations': {
                    key: {
                        'key': cite.key,
                        'text': cite.text,
                        'authors': cite.authors,
                        'title': cite.title,
                        'venue': cite.venue,
                        'year': cite.year,
                        'citation_type': cite.citation_type,
                    }
                    for key, cite in structure.citations.items()
                },
                'mathematical_elements': [
                    {
                        'element_type': elem.element_type,
                        'label': elem.label,
                        'title': elem.title,
                        'content': elem.content[:500],  # Truncate for readability
                        'dependencies': elem.dependencies,
                        'notation_count': len(elem.mathematical_notation),
                    }
                    for elem in structure.mathematical_elements
                ],
                'cross_references': {
                    label: {
                        'ref_type': ref.ref_type,
                        'label': ref.label,
                        'number': ref.number,
                        'title': ref.title,
                    }
                    for label, ref in structure.cross_references.items()
                },
                'statistics': {
                    'total_citations': len(structure.citations),
                    'total_mathematical_elements': len(structure.mathematical_elements),
                    'total_cross_references': len(structure.cross_references),
                    'sections_count': len(structure.sections),
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported paper structure to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting paper structure: {e}")


# Convenience function for quick processing
def process_academic_paper(text: str, metadata: Optional[Dict] = None) -> AcademicPaperStructure:
    """
    Quick function to process an academic paper.
    
    Args:
        text: Full text of the academic paper
        metadata: Optional metadata about the paper
        
    Returns:
        AcademicPaperStructure with complete analysis
    """
    processor = AcademicPaperProcessor()
    return processor.process_paper(text, metadata) 