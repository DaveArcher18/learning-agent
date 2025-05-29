"""
Mathematical Content Enhancement for Academic Papers.

This module provides advanced mathematical content processing including:
- Mathematical equation indexing and search capabilities
- Mathematical concept graph construction 
- Mathematical similarity scoring for retrievals
- Enhanced LaTeX notation handling

Designed for maintainability, modularity, simplicity, and observability.
"""

import re
import logging
from typing import Dict, List, Optional, Set, Tuple, NamedTuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import json
from pathlib import Path
import hashlib
import networkx as nx
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class MathematicalEquation:
    """Represents a mathematical equation with metadata."""
    equation_id: str  # Unique identifier
    latex_content: str  # Original LaTeX
    normalized_content: str  # Normalized form
    variables: Set[str] = field(default_factory=set)
    functions: Set[str] = field(default_factory=set)
    operators: Set[str] = field(default_factory=set)
    constants: Set[str] = field(default_factory=set)
    equation_type: str = "unknown"  # linear, quadratic, differential, etc.
    complexity_score: float = 0.0
    context: Optional[str] = None  # Surrounding text context
    labels: List[str] = field(default_factory=list)  # LaTeX labels
    references: List[str] = field(default_factory=list)  # Other equations referenced


@dataclass
class MathematicalConcept:
    """Represents a mathematical concept extracted from content."""
    concept_id: str
    name: str
    concept_type: str  # theorem, definition, function, operator, etc.
    latex_notation: List[str] = field(default_factory=list)
    related_concepts: Set[str] = field(default_factory=set)
    equations: List[str] = field(default_factory=list)  # Associated equation IDs
    frequency: int = 0
    importance_score: float = 0.0
    context_examples: List[str] = field(default_factory=list)


@dataclass
class MathematicalIndex:
    """Complete mathematical index for a document or collection."""
    equations: Dict[str, MathematicalEquation] = field(default_factory=dict)
    concepts: Dict[str, MathematicalConcept] = field(default_factory=dict)
    concept_graph: Optional['nx.Graph'] = None
    equation_similarity_matrix: Dict[Tuple[str, str], float] = field(default_factory=dict)
    document_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class MathematicalEquationExtractor:
    """Extracts and analyzes mathematical equations from text."""
    
    def __init__(self):
        """Initialize equation extractor with patterns."""
        self._setup_patterns()
        self._setup_classification_rules()
    
    def _setup_patterns(self) -> None:
        """Set up regex patterns for mathematical content recognition."""
        
        # Equation environment patterns
        self.equation_patterns = {
            'display_math': re.compile(r'\$\$(.+?)\$\$', re.DOTALL),
            'inline_math': re.compile(r'\$([^\$]+)\$'),
            'equation_env': re.compile(
                r'\\begin\{(equation|align|gather|multline)\*?\}(.*?)\\end\{\1\*?\}',
                re.DOTALL
            ),
            'eqnarray': re.compile(
                r'\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}',
                re.DOTALL
            ),
        }
        
        # Mathematical element patterns
        self.math_element_patterns = {
            'variables': re.compile(r'([a-zA-Z](?:[_^]\{[^}]+\}|[_^][a-zA-Z0-9])?)'),
            'functions': re.compile(r'\\?(?:sin|cos|tan|log|ln|exp|sqrt|frac|sum|int|prod|lim)'),
            'operators': re.compile(r'[+\-*/=<>≤≥≠≈∈∉⊂⊃∩∪∀∃∂∇∫∑∏]|\\(?:pm|mp|times|div|leq|geq|neq|approx|in|notin|subset|supset|cap|cup|forall|exists|partial|nabla|int|sum|prod)'),
            'constants': re.compile(r'\\?(?:pi|e|infty|emptyset|varnothing)|[πe∞∅]|\b(?:\d+(?:\.\d+)?)\b'),
            'greek_letters': re.compile(r'\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|omicron|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega)'),
        }
        
        # LaTeX structure patterns
        self.structure_patterns = {
            'labels': re.compile(r'\\label\{([^}]+)\}'),
            'references': re.compile(r'\\(?:eq)?ref\{([^}]+)\}'),
            'fractions': re.compile(r'\\frac\{([^}]+)\}\{([^}]+)\}'),
            'roots': re.compile(r'\\sqrt(?:\[([^\]]+)\])?\{([^}]+)\}'),
            'subscripts': re.compile(r'_\{([^}]+)\}|_([a-zA-Z0-9])'),
            'superscripts': re.compile(r'\^\{([^}]+)\}|\^([a-zA-Z0-9])'),
        }
    
    def _setup_classification_rules(self) -> None:
        """Set up rules for classifying equation types."""
        
        self.classification_rules = {
            'linear': {
                'patterns': [r'[a-z]\s*[+\-]\s*[a-z]\s*=', r'[a-z]\s*=\s*[a-z]\s*[+\-]'],
                'keywords': ['linear', 'first order'],
            },
            'quadratic': {
                'patterns': [r'[a-z]\^2', r'[a-z]\^\{2\}', r'\\frac\{.*\}\{.*\}.*[a-z]\^2'],
                'keywords': ['quadratic', 'second order'],
            },
            'differential': {
                'patterns': [r'\\frac\{d[a-z]\}\{d[a-z]\}', r'\\partial', r"[a-z]'", r"[a-z]''"],
                'keywords': ['derivative', 'differential', 'ode', 'pde'],
            },
            'integral': {
                'patterns': [r'\\int', r'∫'],
                'keywords': ['integral', 'integration'],
            },
            'summation': {
                'patterns': [r'\\sum', r'∑'],
                'keywords': ['sum', 'summation', 'series'],
            },
            'matrix': {
                'patterns': [r'\\begin\{(?:matrix|pmatrix|bmatrix|vmatrix|Vmatrix)\}'],
                'keywords': ['matrix', 'vector', 'linear algebra'],
            },
            'probability': {
                'patterns': [r'P\(', r'E\[', r'\\mathbb\{P\}', r'\\mathbb\{E\}'],
                'keywords': ['probability', 'expectation', 'variance'],
            },
        }
    
    def extract_equations(self, text: str, context: Optional[str] = None) -> List[MathematicalEquation]:
        """
        Extract mathematical equations from text.
        
        Args:
            text: Input text containing equations
            context: Optional context information
            
        Returns:
            List of MathematicalEquation objects
        """
        equations = []
        
        try:
            # Extract from different equation environments
            for env_type, pattern in self.equation_patterns.items():
                equations.extend(self._extract_from_pattern(text, pattern, env_type, context))
            
            logger.info(f"Extracted {len(equations)} equations from text")
            
        except Exception as e:
            logger.error(f"Error extracting equations: {e}")
        
        return equations
    
    def _extract_from_pattern(self, text: str, pattern: re.Pattern, 
                            env_type: str, context: Optional[str]) -> List[MathematicalEquation]:
        """Extract equations from a specific pattern."""
        equations = []
        
        for match in pattern.finditer(text):
            latex_content = match.group(1) if match.lastindex >= 1 else match.group(0)
            
            # Generate unique ID
            equation_id = self._generate_equation_id(latex_content)
            
            # Normalize content
            normalized_content = self._normalize_equation(latex_content)
            
            # Extract mathematical elements
            variables = self._extract_variables(latex_content)
            functions = self._extract_functions(latex_content)
            operators = self._extract_operators(latex_content)
            constants = self._extract_constants(latex_content)
            
            # Classify equation type
            equation_type = self._classify_equation(latex_content, context)
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity(latex_content)
            
            # Extract labels and references
            labels = self._extract_labels(latex_content)
            references = self._extract_references(latex_content)
            
            equation = MathematicalEquation(
                equation_id=equation_id,
                latex_content=latex_content.strip(),
                normalized_content=normalized_content,
                variables=variables,
                functions=functions,
                operators=operators,
                constants=constants,
                equation_type=equation_type,
                complexity_score=complexity_score,
                context=context,
                labels=labels,
                references=references
            )
            
            equations.append(equation)
        
        return equations
    
    def _generate_equation_id(self, latex_content: str) -> str:
        """Generate unique ID for equation."""
        content_hash = hashlib.md5(latex_content.encode()).hexdigest()[:8]
        return f"eq_{content_hash}"
    
    def _normalize_equation(self, latex_content: str) -> str:
        """Normalize equation for comparison."""
        # Remove whitespace and standardize formatting
        normalized = re.sub(r'\s+', ' ', latex_content.strip())
        
        # Standardize common patterns
        normalized = re.sub(r'\\left\(', '(', normalized)
        normalized = re.sub(r'\\right\)', ')', normalized)
        normalized = re.sub(r'\\left\[', '[', normalized)
        normalized = re.sub(r'\\right\]', ']', normalized)
        
        return normalized
    
    def _extract_variables(self, latex_content: str) -> Set[str]:
        """Extract variable names from equation."""
        variables = set()
        
        # Find single letters that aren't part of functions
        for match in self.math_element_patterns['variables'].finditer(latex_content):
            var = match.group(1)
            # Skip if it's part of a known function
            if not any(func in latex_content[max(0, match.start()-10):match.end()+10] 
                      for func in ['sin', 'cos', 'tan', 'log', 'ln']):
                variables.add(var)
        
        return variables
    
    def _extract_functions(self, latex_content: str) -> Set[str]:
        """Extract function names from equation."""
        functions = set()
        
        for match in self.math_element_patterns['functions'].finditer(latex_content):
            functions.add(match.group(0))
        
        return functions
    
    def _extract_operators(self, latex_content: str) -> Set[str]:
        """Extract operators from equation."""
        operators = set()
        
        for match in self.math_element_patterns['operators'].finditer(latex_content):
            operators.add(match.group(0))
        
        return operators
    
    def _extract_constants(self, latex_content: str) -> Set[str]:
        """Extract mathematical constants from equation."""
        constants = set()
        
        for match in self.math_element_patterns['constants'].finditer(latex_content):
            constants.add(match.group(0))
        
        return constants
    
    def _extract_labels(self, latex_content: str) -> List[str]:
        """Extract LaTeX labels from equation."""
        labels = []
        
        for match in self.structure_patterns['labels'].finditer(latex_content):
            labels.append(match.group(1))
        
        return labels
    
    def _extract_references(self, latex_content: str) -> List[str]:
        """Extract equation references from content."""
        references = []
        
        for match in self.structure_patterns['references'].finditer(latex_content):
            references.append(match.group(1))
        
        return references
    
    def _classify_equation(self, latex_content: str, context: Optional[str]) -> str:
        """Classify the type of equation."""
        content_to_check = latex_content.lower()
        if context:
            content_to_check += " " + context.lower()
        
        # Check against classification rules
        for eq_type, rules in self.classification_rules.items():
            # Check patterns
            for pattern in rules['patterns']:
                if re.search(pattern, content_to_check):
                    return eq_type
            
            # Check keywords
            for keyword in rules['keywords']:
                if keyword in content_to_check:
                    return eq_type
        
        return "unknown"
    
    def _calculate_complexity(self, latex_content: str) -> float:
        """Calculate complexity score for equation."""
        score = 0.0
        
        # Count different types of mathematical elements
        score += len(self.math_element_patterns['functions'].findall(latex_content)) * 2
        score += len(self.math_element_patterns['operators'].findall(latex_content))
        score += len(self.structure_patterns['fractions'].findall(latex_content)) * 3
        score += len(self.structure_patterns['roots'].findall(latex_content)) * 2
        score += len(self.structure_patterns['subscripts'].findall(latex_content))
        score += len(self.structure_patterns['superscripts'].findall(latex_content))
        
        # Normalize by length
        if latex_content:
            score = score / len(latex_content) * 100
        
        return min(score, 10.0)  # Cap at 10


class MathematicalConceptExtractor:
    """Extracts mathematical concepts and builds concept relationships."""
    
    def __init__(self):
        """Initialize concept extractor."""
        self._setup_concept_patterns()
        self._concept_frequency = Counter()
    
    def _setup_concept_patterns(self) -> None:
        """Set up patterns for concept recognition."""
        
        self.concept_patterns = {
            'theorem_names': re.compile(
                r'\\begin\{theorem\}(?:\[([^\]]+)\])?|'
                r'Theorem\s+(?:\d+\.)*\d+\s*\(([^)]+)\)|'
                r'([A-Z][a-z]+ Theorem|[A-Z][a-z]+ Lemma)',
                re.IGNORECASE
            ),
            'definition_names': re.compile(
                r'\\begin\{definition\}(?:\[([^\]]+)\])?|'
                r'Definition\s+(?:\d+\.)*\d+\s*\(([^)]+)\)|'
                r'We define ([^.]+) as',
                re.IGNORECASE
            ),
            'function_definitions': re.compile(
                r'([a-zA-Z]\w*)\s*:\s*[A-Z]\w*\s*→\s*[A-Z]\w*|'
                r'function\s+([a-zA-Z]\w*)\s*\(',
                re.IGNORECASE
            ),
            'mathematical_objects': re.compile(
                r'\\mathbb\{([A-Z])\}|'
                r'\\mathcal\{([A-Z])\}|'
                r'\\mathrm\{([a-zA-Z]+)\}',
            ),
        }
    
    def extract_concepts(self, text: str, equations: List[MathematicalEquation]) -> List[MathematicalConcept]:
        """
        Extract mathematical concepts from text and equations.
        
        Args:
            text: Source text
            equations: List of equations to analyze
            
        Returns:
            List of mathematical concepts
        """
        concepts = []
        
        try:
            # Extract named concepts (theorems, definitions, etc.)
            concepts.extend(self._extract_named_concepts(text))
            
            # Extract function concepts
            concepts.extend(self._extract_function_concepts(text))
            
            # Extract mathematical object concepts
            concepts.extend(self._extract_mathematical_objects(text))
            
            # Link concepts to equations
            self._link_concepts_to_equations(concepts, equations)
            
            logger.info(f"Extracted {len(concepts)} mathematical concepts")
            
        except Exception as e:
            logger.error(f"Error extracting concepts: {e}")
        
        return concepts
    
    def _extract_named_concepts(self, text: str) -> List[MathematicalConcept]:
        """Extract named theorems, definitions, etc."""
        concepts = []
        
        # Extract theorems
        for match in self.concept_patterns['theorem_names'].finditer(text):
            name = next(group for group in match.groups() if group is not None)
            concept_id = self._generate_concept_id(name, "theorem")
            
            concept = MathematicalConcept(
                concept_id=concept_id,
                name=name,
                concept_type="theorem"
            )
            concepts.append(concept)
        
        # Extract definitions
        for match in self.concept_patterns['definition_names'].finditer(text):
            name = next(group for group in match.groups() if group is not None)
            concept_id = self._generate_concept_id(name, "definition")
            
            concept = MathematicalConcept(
                concept_id=concept_id,
                name=name,
                concept_type="definition"
            )
            concepts.append(concept)
        
        return concepts
    
    def _extract_function_concepts(self, text: str) -> List[MathematicalConcept]:
        """Extract function definitions and concepts."""
        concepts = []
        
        for match in self.concept_patterns['function_definitions'].finditer(text):
            func_name = next(group for group in match.groups() if group is not None)
            concept_id = self._generate_concept_id(func_name, "function")
            
            concept = MathematicalConcept(
                concept_id=concept_id,
                name=func_name,
                concept_type="function"
            )
            concepts.append(concept)
        
        return concepts
    
    def _extract_mathematical_objects(self, text: str) -> List[MathematicalConcept]:
        """Extract mathematical objects like sets, spaces, etc."""
        concepts = []
        
        for match in self.concept_patterns['mathematical_objects'].finditer(text):
            obj_name = next(group for group in match.groups() if group is not None)
            concept_id = self._generate_concept_id(obj_name, "mathematical_object")
            
            concept = MathematicalConcept(
                concept_id=concept_id,
                name=obj_name,
                concept_type="mathematical_object"
            )
            concepts.append(concept)
        
        return concepts
    
    def _generate_concept_id(self, name: str, concept_type: str) -> str:
        """Generate unique concept ID."""
        name_hash = hashlib.md5(f"{name}_{concept_type}".encode()).hexdigest()[:8]
        return f"concept_{concept_type}_{name_hash}"
    
    def _link_concepts_to_equations(self, concepts: List[MathematicalConcept], 
                                   equations: List[MathematicalEquation]) -> None:
        """Link concepts to relevant equations."""
        for concept in concepts:
            for equation in equations:
                # Simple heuristic: check if concept name appears in equation context
                if (concept.name.lower() in (equation.context or "").lower() or
                    any(concept.name.lower() in var.lower() for var in equation.variables)):
                    concept.equations.append(equation.equation_id)
    
    def build_concept_graph(self, concepts: List[MathematicalConcept]) -> nx.Graph:
        """
        Build a graph of mathematical concept relationships.
        
        Args:
            concepts: List of mathematical concepts
            
        Returns:
            NetworkX graph representing concept relationships
        """
        graph = nx.Graph()
        
        # Add nodes
        for concept in concepts:
            graph.add_node(concept.concept_id, 
                          name=concept.name,
                          concept_type=concept.concept_type,
                          importance=concept.importance_score)
        
        # Add edges based on shared equations and context
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                # Calculate relationship strength
                shared_equations = len(set(concept1.equations) & set(concept2.equations))
                
                if shared_equations > 0:
                    weight = shared_equations / max(len(concept1.equations), len(concept2.equations))
                    graph.add_edge(concept1.concept_id, concept2.concept_id, weight=weight)
        
        logger.info(f"Built concept graph with {graph.number_of_nodes()} nodes "
                   f"and {graph.number_of_edges()} edges")
        
        return graph


class MathematicalSimilarityCalculator:
    """Calculates similarity between mathematical expressions."""
    
    def __init__(self):
        """Initialize similarity calculator."""
        self._setup_similarity_weights()
    
    def _setup_similarity_weights(self) -> None:
        """Set up weights for different similarity components."""
        self.weights = {
            'structural': 0.4,  # LaTeX structure similarity
            'semantic': 0.3,    # Mathematical meaning similarity
            'variable': 0.2,    # Variable usage similarity
            'functional': 0.1,  # Function usage similarity
        }
    
    def calculate_equation_similarity(self, eq1: MathematicalEquation, 
                                    eq2: MathematicalEquation) -> float:
        """
        Calculate similarity between two equations.
        
        Args:
            eq1: First equation
            eq2: Second equation
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Structural similarity (normalized LaTeX)
            structural_sim = self._calculate_structural_similarity(
                eq1.normalized_content, eq2.normalized_content
            )
            
            # Semantic similarity (equation types, operators)
            semantic_sim = self._calculate_semantic_similarity(eq1, eq2)
            
            # Variable similarity
            variable_sim = self._calculate_set_similarity(eq1.variables, eq2.variables)
            
            # Function similarity
            function_sim = self._calculate_set_similarity(eq1.functions, eq2.functions)
            
            # Weighted combination
            total_similarity = (
                self.weights['structural'] * structural_sim +
                self.weights['semantic'] * semantic_sim +
                self.weights['variable'] * variable_sim +
                self.weights['functional'] * function_sim
            )
            
            return total_similarity
            
        except Exception as e:
            logger.error(f"Error calculating equation similarity: {e}")
            return 0.0
    
    def _calculate_structural_similarity(self, latex1: str, latex2: str) -> float:
        """Calculate structural similarity based on LaTeX content."""
        if not latex1 or not latex2:
            return 0.0
        
        # Simple edit distance-based similarity
        max_len = max(len(latex1), len(latex2))
        if max_len == 0:
            return 1.0
        
        # Simple character-based similarity (could be improved with sequence alignment)
        common_chars = sum(1 for c1, c2 in zip(latex1, latex2) if c1 == c2)
        return common_chars / max_len
    
    def _calculate_semantic_similarity(self, eq1: MathematicalEquation, 
                                     eq2: MathematicalEquation) -> float:
        """Calculate semantic similarity based on equation properties."""
        similarity = 0.0
        
        # Equation type similarity
        if eq1.equation_type == eq2.equation_type and eq1.equation_type != "unknown":
            similarity += 0.5
        
        # Operator similarity
        operator_sim = self._calculate_set_similarity(eq1.operators, eq2.operators)
        similarity += 0.3 * operator_sim
        
        # Complexity similarity
        if eq1.complexity_score > 0 and eq2.complexity_score > 0:
            complexity_diff = abs(eq1.complexity_score - eq2.complexity_score)
            complexity_sim = max(0, 1 - complexity_diff / 10.0)
            similarity += 0.2 * complexity_sim
        
        return similarity
    
    def _calculate_set_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def build_similarity_matrix(self, equations: List[MathematicalEquation]) -> Dict[Tuple[str, str], float]:
        """
        Build similarity matrix for all equation pairs.
        
        Args:
            equations: List of equations to compare
            
        Returns:
            Dict mapping equation ID pairs to similarity scores
        """
        similarity_matrix = {}
        
        for i, eq1 in enumerate(equations):
            for eq2 in equations[i+1:]:
                similarity = self.calculate_equation_similarity(eq1, eq2)
                similarity_matrix[(eq1.equation_id, eq2.equation_id)] = similarity
                similarity_matrix[(eq2.equation_id, eq1.equation_id)] = similarity  # Symmetric
        
        logger.info(f"Built similarity matrix for {len(equations)} equations")
        return similarity_matrix


class MathematicalIndexer:
    """Main class for building comprehensive mathematical indices."""
    
    def __init__(self):
        """Initialize mathematical indexer."""
        self.equation_extractor = MathematicalEquationExtractor()
        self.concept_extractor = MathematicalConceptExtractor()
        self.similarity_calculator = MathematicalSimilarityCalculator()
    
    def build_mathematical_index(self, text: str, document_id: Optional[str] = None) -> MathematicalIndex:
        """
        Build complete mathematical index for a document.
        
        Args:
            text: Document text
            document_id: Optional document identifier
            
        Returns:
            Complete mathematical index
        """
        logger.info("Building mathematical index...")
        
        try:
            # Extract equations
            equations = self.equation_extractor.extract_equations(text)
            equations_dict = {eq.equation_id: eq for eq in equations}
            
            # Extract concepts
            concepts = self.concept_extractor.extract_concepts(text, equations)
            concepts_dict = {concept.concept_id: concept for concept in concepts}
            
            # Build concept graph
            concept_graph = self.concept_extractor.build_concept_graph(concepts)
            
            # Build equation similarity matrix
            similarity_matrix = self.similarity_calculator.build_similarity_matrix(equations)
            
            # Create index
            index = MathematicalIndex(
                equations=equations_dict,
                concepts=concepts_dict,
                concept_graph=concept_graph,
                equation_similarity_matrix=similarity_matrix,
                document_id=document_id
            )
            
            logger.info(f"Built mathematical index with {len(equations)} equations "
                       f"and {len(concepts)} concepts")
            
            return index
            
        except Exception as e:
            logger.error(f"Error building mathematical index: {e}")
            return MathematicalIndex()
    
    def search_similar_equations(self, index: MathematicalIndex, 
                                query_equation: MathematicalEquation, 
                                top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for equations similar to query equation.
        
        Args:
            index: Mathematical index to search
            query_equation: Query equation
            top_k: Number of results to return
            
        Returns:
            List of (equation_id, similarity_score) tuples
        """
        similarities = []
        
        for eq_id, equation in index.equations.items():
            if eq_id != query_equation.equation_id:
                similarity = self.similarity_calculator.calculate_equation_similarity(
                    query_equation, equation
                )
                similarities.append((eq_id, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def export_index(self, index: MathematicalIndex, output_path: Path) -> None:
        """Export mathematical index to JSON file."""
        try:
            # Convert to serializable format
            data = {
                'document_id': index.document_id,
                'created_at': index.created_at,
                'equations': {
                    eq_id: {
                        'equation_id': eq.equation_id,
                        'latex_content': eq.latex_content,
                        'normalized_content': eq.normalized_content,
                        'variables': list(eq.variables),
                        'functions': list(eq.functions),
                        'operators': list(eq.operators),
                        'constants': list(eq.constants),
                        'equation_type': eq.equation_type,
                        'complexity_score': eq.complexity_score,
                        'labels': eq.labels,
                        'references': eq.references,
                    }
                    for eq_id, eq in index.equations.items()
                },
                'concepts': {
                    concept_id: {
                        'concept_id': concept.concept_id,
                        'name': concept.name,
                        'concept_type': concept.concept_type,
                        'latex_notation': concept.latex_notation,
                        'related_concepts': list(concept.related_concepts),
                        'equations': concept.equations,
                        'frequency': concept.frequency,
                        'importance_score': concept.importance_score,
                    }
                    for concept_id, concept in index.concepts.items()
                },
                'concept_graph': {
                    'nodes': list(index.concept_graph.nodes()) if index.concept_graph else [],
                    'edges': list(index.concept_graph.edges()) if index.concept_graph else [],
                },
                'statistics': {
                    'total_equations': len(index.equations),
                    'total_concepts': len(index.concepts),
                    'graph_nodes': index.concept_graph.number_of_nodes() if index.concept_graph else 0,
                    'graph_edges': index.concept_graph.number_of_edges() if index.concept_graph else 0,
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported mathematical index to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting mathematical index: {e}")


# Convenience functions
def build_mathematical_index(text: str, document_id: Optional[str] = None) -> MathematicalIndex:
    """Build mathematical index for a document."""
    indexer = MathematicalIndexer()
    return indexer.build_mathematical_index(text, document_id)


def calculate_mathematical_similarity(eq1_latex: str, eq2_latex: str) -> float:
    """Calculate similarity between two LaTeX equations."""
    extractor = MathematicalEquationExtractor()
    calculator = MathematicalSimilarityCalculator()
    
    # Create minimal equation objects
    eq1 = extractor.extract_equations(f"$${eq1_latex}$$")[0] if eq1_latex else None
    eq2 = extractor.extract_equations(f"$${eq2_latex}$$")[0] if eq2_latex else None
    
    if eq1 and eq2:
        return calculator.calculate_equation_similarity(eq1, eq2)
    
    return 0.0 