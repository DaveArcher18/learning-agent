"""
LaTeX/Math Expression Renderer for Mathematical Content.

This module provides comprehensive LaTeX-to-Unicode conversion and 
mathematical expression rendering optimized for console display.
Extracted from the main agent to ensure maintainability and modularity.
"""

import re
import logging
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class LatexRenderingConfig:
    """Configuration for LaTeX rendering behavior."""
    enable_advanced_rendering: bool = True
    enable_unicode_symbols: bool = True
    enable_rich_formatting: bool = True
    preserve_math_delimiters: bool = False
    debug_mode: bool = False


class LatexRenderer:
    """
    Comprehensive LaTeX-to-Unicode renderer for mathematical expressions.
    
    This class handles the conversion of LaTeX mathematical notation to 
    Unicode symbols and formatted text suitable for console display.
    Optimized for mathematical content with proper error handling.
    """
    
    def __init__(self, config: Optional[LatexRenderingConfig] = None):
        """
        Initialize the LaTeX renderer.
        
        Args:
            config: Optional configuration for rendering behavior
        """
        self.config = config or LatexRenderingConfig()
        self._expressions_rendered = 0
        self._symbols_converted = 0
        self._errors_encountered = 0
        self._setup_symbol_mappings()
        self._compile_regex_patterns()
    
    def _setup_symbol_mappings(self) -> None:
        """Set up comprehensive symbol mappings for LaTeX to Unicode."""
        
        # Greek letters (lowercase and uppercase)
        self.greek_letters = {
            # Lowercase
            '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
            '\\epsilon': 'ε', '\\varepsilon': 'ɛ', '\\zeta': 'ζ', '\\eta': 'η',
            '\\theta': 'θ', '\\iota': 'ι', '\\kappa': 'κ', '\\lambda': 'λ',
            '\\mu': 'μ', '\\nu': 'ν', '\\xi': 'ξ', '\\rho': 'ρ',
            '\\sigma': 'σ', '\\tau': 'τ', '\\upsilon': 'υ', '\\phi': 'φ',
            '\\varphi': 'ϕ', '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
            
            # Uppercase
            '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ',
            '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Upsilon': 'Υ',
            '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω',
        }
        
        # Mathematical symbols
        self.math_symbols = {
            '\\infty': '∞', '\\pi': 'π',
            '\\sum': '∑', '\\prod': '∏', '\\int': '∫',
            '\\partial': '∂', '\\nabla': '∇',
            '\\pm': '±', '\\mp': '∓',
            '\\times': '×', '\\cdot': '·', '\\div': '÷',
            '\\approx': '≈', '\\neq': '≠', '\\equiv': '≡',
            '\\leq': '≤', '\\geq': '≥', '\\ll': '≪', '\\gg': '≫',
            '\\subset': '⊂', '\\supset': '⊃', '\\subseteq': '⊆', '\\supseteq': '⊇',
            '\\in': '∈', '\\notin': '∉', '\\ni': '∋',
            '\\cap': '∩', '\\cup': '∪',
            '\\leftarrow': '←', '\\rightarrow': '→', '\\leftrightarrow': '↔',
            '\\Leftarrow': '⇐', '\\Rightarrow': '⇒', '\\Leftrightarrow': '⇔',
            '\\uparrow': '↑', '\\downarrow': '↓', '\\updownarrow': '↕',
            '\\forall': '∀', '\\exists': '∃', '\\nexists': '∄',
            '\\emptyset': '∅', '\\varnothing': '∅',
            '\\ldots': '...', '\\cdots': '⋯', '\\vdots': '⋮', '\\ddots': '⋱',
            '\\angle': '∠', '\\degree': '°',
            '\\hbar': 'ħ', '\\prime': '′',
        }
        
        # Mathematical blackboard bold (number sets)
        self.mathbb_symbols = {
            '\\mathbb{R}': 'ℝ', '\\mathbb{Z}': 'ℤ', '\\mathbb{N}': 'ℕ',
            '\\mathbb{Q}': 'ℚ', '\\mathbb{C}': 'ℂ', '\\mathbb{H}': 'ℍ',
            '\\mathbb{P}': 'ℙ', '\\mathbb{F}': '𝔽',
        }
        
        # Mathematical functions
        self.math_functions = [
            'sin', 'cos', 'tan', 'csc', 'sec', 'cot',
            'sinh', 'cosh', 'tanh', 'csch', 'sech', 'coth',
            'arcsin', 'arccos', 'arctan', 'arccsc', 'arcsec', 'arccot',
            'log', 'ln', 'lg', 'exp',
            'lim', 'liminf', 'limsup', 'sup', 'inf',
            'det', 'dim', 'deg', 'gcd', 'lcm', 'ker', 'im',
            'min', 'max', 'arg', 'mod'
        ]
        
        # Combining characters for accents
        self.accents = {
            '\\hat': '\u0302',    # Combining circumflex
            '\\bar': '\u0304',    # Combining macron
            '\\tilde': '\u0303',  # Combining tilde
            '\\vec': '\u20D7',    # Combining right arrow above
            '\\dot': '\u0307',    # Combining dot above
            '\\ddot': '\u0308',   # Combining diaeresis
        }
        
        # Unicode superscripts and subscripts
        self.superscripts = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
            'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ',
            'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ',
            'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ',
            'p': 'ᵖ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ',
            'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ',
        }
        
        self.subscripts = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
            '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
            'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
            'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
            'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
            'v': 'ᵥ', 'x': 'ₓ',
        }
    
    def _compile_regex_patterns(self) -> None:
        """Compile frequently used regex patterns for performance."""
        
        # Complex patterns that need compilation
        self.patterns = {
            'matrix': re.compile(
                r'\\begin\{(matrix|pmatrix|bmatrix|vmatrix|Vmatrix|array)\}.*?\\end\{\1\}',
                re.DOTALL
            ),
            'fraction': re.compile(r'\\frac\{([^}]+)\}\{([^}]+)\}'),
            'binomial': re.compile(r'\\binom\{([^}]+)\}\{([^}]+)\}'),
            'sqrt_nth': re.compile(r'\\sqrt\[([^]]+)\]\{([^}]+)\}'),
            'sqrt_simple': re.compile(r'\\sqrt\{([^}]+)\}'),
            'subscript_multi': re.compile(r'_\{([^}]+)\}'),
            'superscript_multi': re.compile(r'\^\{([^}]+)\}'),
            'subscript_single': re.compile(r'([a-zA-Z0-9])_([a-zA-Z0-9])'),
            'superscript_single': re.compile(r'([a-zA-Z0-9])\^([a-zA-Z0-9])'),
            'inline_math': re.compile(r'\\\((.+?)\\\)'),
            'display_math': re.compile(r'\\\[(.+?)\\\]'),
            'dollar_inline': re.compile(r'\$([^\$]+)\$'),
            'dollar_display': re.compile(r'\$\$(.+?)\$\$', re.DOTALL),
            'font_bold': re.compile(r'\\mathbf\{([^}]+)\}'),
            'font_italic': re.compile(r'\\textit\{([^}]+)\}'),
            'font_mono': re.compile(r'\\texttt\{([^}]+)\}'),
            'font_roman': re.compile(r'\\mathrm\{([^}]+)\}'),
            'mathcal': re.compile(r'\\mathcal\{([A-Z])\}'),
            'mathbb_generic': re.compile(r'\\mathbb\{([a-zA-Z])\}'),
        }
    
    def render_latex(self, text: str) -> str:
        """
        Main method to render LaTeX expressions to Unicode.
        
        Args:
            text: Input text containing LaTeX expressions
            
        Returns:
            str: Text with LaTeX converted to Unicode symbols
        """
        if not text or not self.config.enable_advanced_rendering:
            return text
        
        try:
            self._expressions_rendered += 1
            
            # Process in order of complexity to avoid conflicts
            result = self._process_block_environments(text)
            result = self._process_fractions_and_roots(result)
            result = self._process_accents(result)
            result = self._process_subscripts_superscripts(result)
            result = self._process_fonts(result)
            result = self._process_math_symbols(result)
            result = self._process_greek_letters(result)
            result = self._process_math_functions(result)
            result = self._process_math_delimiters(result)
            result = self._unescape_characters(result)
            
            # Count symbols converted
            if result != text:
                self._symbols_converted += 1
            
            if self.config.debug_mode:
                logger.debug(f"LaTeX rendering: '{text[:50]}...' -> '{result[:50]}...'")
                
            return result
            
        except Exception as e:
            self._errors_encountered += 1
            logger.error(f"LaTeX rendering error: {e}")
            if self.config.debug_mode:
                logger.exception("Full LaTeX rendering traceback")
            return text  # Return original text on error
    
    def _process_block_environments(self, text: str) -> str:
        """Process complex block environments like matrices."""
        # Replace complex environments with simplified placeholders
        text = self.patterns['matrix'].sub(r'[matrix]', text)
        text = re.sub(r'\\displaystyle', '', text)
        return text
    
    def _process_fractions_and_roots(self, text: str) -> str:
        """Process fractions, binomials, and roots."""
        # Fractions
        text = self.patterns['fraction'].sub(r'(\1/\2)', text)
        
        # Binomials
        text = self.patterns['binomial'].sub(r'C(\1, \2)', text)
        
        # Roots
        text = self.patterns['sqrt_nth'].sub(r'\1th_root(\2)', text)
        text = self.patterns['sqrt_simple'].sub(r'sqrt(\1)', text)
        
        return text
    
    def _process_accents(self, text: str) -> str:
        """Process accent marks and combining characters."""
        for latex_accent, unicode_accent in self.accents.items():
            pattern = rf'{re.escape(latex_accent)}\{{([a-zA-Z0-9])\}}'
            text = re.sub(pattern, rf'\1{unicode_accent}', text)
        
        return text
    
    def _process_subscripts_superscripts(self, text: str) -> str:
        """Process subscripts and superscripts with Unicode or Rich formatting."""
        
        def convert_to_unicode_super(match):
            content = match.group(1)
            result = ""
            for char in content:
                result += self.superscripts.get(char, char)
            return result
        
        def convert_to_unicode_sub(match):
            content = match.group(1)
            result = ""
            for char in content:
                result += self.subscripts.get(char, char)
            return result
        
        if self.config.enable_unicode_symbols:
            # Unicode superscripts and subscripts
            text = self.patterns['superscript_multi'].sub(convert_to_unicode_super, text)
            text = self.patterns['subscript_multi'].sub(convert_to_unicode_sub, text)
            # Handle single characters - now with two capture groups (base, script)
            text = self.patterns['superscript_single'].sub(lambda m: m.group(1) + self.superscripts.get(m.group(2), m.group(2)), text)
            text = self.patterns['subscript_single'].sub(lambda m: m.group(1) + self.subscripts.get(m.group(2), m.group(2)), text)
        elif not self.config.enable_rich_formatting:
            # Simple text representation
            text = self.patterns['subscript_multi'].sub(r'_(\1)', text)
            text = self.patterns['superscript_multi'].sub(r'^(\1)', text)
            text = self.patterns['subscript_single'].sub(r'\1_\2', text)
            text = self.patterns['superscript_single'].sub(r'\1^\2', text)
        else:
            # Rich markup tags
            text = self.patterns['subscript_multi'].sub(r'[sub]\1[/sub]', text)
            text = self.patterns['superscript_multi'].sub(r'[sup]\1[/sup]', text)
            text = self.patterns['subscript_single'].sub(r'\1[sub]\2[/sub]', text)
            text = self.patterns['superscript_single'].sub(r'\1[sup]\2[/sup]', text)
        
        return text
    
    def _process_fonts(self, text: str) -> str:
        """Process font styles and formatting."""
        if self.config.enable_rich_formatting:
            # Rich markup
            text = self.patterns['font_bold'].sub(r'[b]\1[/b]', text)
            text = self.patterns['font_italic'].sub(r'[i]\1[/i]', text)
            text = self.patterns['font_mono'].sub(r'[code]\1[/code]', text)
        else:
            # Plain text
            text = self.patterns['font_bold'].sub(r'\1', text)
            text = self.patterns['font_italic'].sub(r'\1', text)
            text = self.patterns['font_mono'].sub(r'\1', text)
        
        # Roman font (always plain)
        text = self.patterns['font_roman'].sub(r'\1', text)
        
        # Mathcal (calligraphic) - simplified to plain
        text = self.patterns['mathcal'].sub(r'\1', text)
        
        return text
    
    def _process_math_symbols(self, text: str) -> str:
        """Process mathematical symbols and convert to Unicode."""
        if not self.config.enable_unicode_symbols:
            return text
        
        # Process specific mathbb symbols first
        for latex_symbol, unicode_symbol in self.mathbb_symbols.items():
            text = text.replace(latex_symbol, unicode_symbol)
        
        # Process generic mathbb
        text = self.patterns['mathbb_generic'].sub(r'\1', text)
        
        # Process general math symbols
        for latex_symbol, unicode_symbol in self.math_symbols.items():
            text = text.replace(latex_symbol, unicode_symbol)
        
        return text
    
    def _process_greek_letters(self, text: str) -> str:
        """Process Greek letters and convert to Unicode."""
        if not self.config.enable_unicode_symbols:
            return text
        
        for latex_letter, unicode_letter in self.greek_letters.items():
            text = text.replace(latex_letter, unicode_letter)
        
        return text
    
    def _process_math_functions(self, text: str) -> str:
        """Process mathematical function names."""
        for func_name in self.math_functions:
            # Remove backslash, ensure word boundary
            pattern = rf'\\{re.escape(func_name)}(?!\w)'
            text = re.sub(pattern, func_name, text)
        
        return text
    
    def _process_math_delimiters(self, text: str) -> str:
        """Process inline and display math delimiters."""
        if not self.config.preserve_math_delimiters:
            # Remove delimiters entirely - process dollar signs first (display math)
            text = self.patterns['dollar_display'].sub(r'\1', text)
            text = self.patterns['dollar_inline'].sub(r'\1', text)
            text = self.patterns['inline_math'].sub(r'\1', text)
            text = self.patterns['display_math'].sub(r'\1', text)
        elif self.config.enable_rich_formatting:
            # Use Rich markup for emphasis
            text = self.patterns['dollar_display'].sub(r'\n\n[b][ \1 ][/b]\n\n', text)
            text = self.patterns['dollar_inline'].sub(r'[i] \1 [/i]', text)
            text = self.patterns['inline_math'].sub(r'[i] \1 [/i]', text)
            text = self.patterns['display_math'].sub(r'\n\n[b][ \1 ][/b]\n\n', text)
        else:
            # Plain text emphasis
            text = self.patterns['dollar_display'].sub(r'\n\n[ \1 ]\n\n', text)
            text = self.patterns['dollar_inline'].sub(r' \1 ', text)
            text = self.patterns['inline_math'].sub(r' \1 ', text)
            text = self.patterns['display_math'].sub(r'\n\n[ \1 ]\n\n', text)
        
        return text
    
    def _unescape_characters(self, text: str) -> str:
        """Unescape LaTeX escaped characters."""
        escape_mappings = {
            '\\{': '{', '\\}': '}', '\\%': '%',
            '\\&': '&', '\\#': '#', '\\_': '_',
            '\\$': '$', '\\\\': '\n',  # Double backslash to newline
        }
        
        for escaped, unescaped in escape_mappings.items():
            text = text.replace(escaped, unescaped)
        
        return text
    
    def validate_latex(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validate LaTeX syntax and report potential issues.
        
        Args:
            text: Text containing LaTeX expressions
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for unmatched braces
        brace_count = 0
        for char in text:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count < 0:
                    issues.append("Unmatched closing brace }")
                    break
        
        if brace_count > 0:
            issues.append(f"Unmatched opening braces: {brace_count}")
        
        # Check for malformed commands
        malformed_commands = re.findall(r'\\[a-zA-Z]*\{[^}]*$', text)
        if malformed_commands:
            issues.append(f"Potentially malformed commands: {malformed_commands}")
        
        # Check for unknown commands (basic check)
        all_commands = set(self.greek_letters.keys()) | set(self.math_symbols.keys())
        all_commands.update(f'\\{func}' for func in self.math_functions)
        
        found_commands = re.findall(r'\\[a-zA-Z]+', text)
        unknown_commands = [cmd for cmd in found_commands if cmd not in all_commands]
        
        # Filter out some common but not implemented commands
        common_safe = ['\\text', '\\left', '\\right', '\\big', '\\Big']
        unknown_commands = [cmd for cmd in unknown_commands 
                          if not any(cmd.startswith(safe) for safe in common_safe)]
        
        if unknown_commands:
            issues.append(f"Unknown commands (may not render): {list(set(unknown_commands))}")
        
        return len(issues) == 0, issues
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics tracking for rendered expressions.
        
        Returns:
            Dict containing statistics from previous render operations
        """
        # For test compatibility - add basic statistics tracking
        return {
            'expressions_rendered': getattr(self, '_expressions_rendered', 0),
            'symbols_converted': getattr(self, '_symbols_converted', 0),
            'errors_encountered': getattr(self, '_errors_encountered', 0),
        }
    
    def get_rendering_stats(self, text: str) -> Dict[str, int]:
        """
        Get statistics about LaTeX content in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dict containing rendering statistics
        """
        stats = {
            'total_commands': len(re.findall(r'\\[a-zA-Z]+', text)),
            'greek_letters': 0,
            'math_symbols': 0,
            'fractions': len(self.patterns['fraction'].findall(text)),
            'matrices': len(self.patterns['matrix'].findall(text)),
            'subscripts': len(self.patterns['subscript_multi'].findall(text)) + 
                         len(self.patterns['subscript_single'].findall(text)),
            'superscripts': len(self.patterns['superscript_multi'].findall(text)) + 
                           len(self.patterns['superscript_single'].findall(text)),
            'inline_math': len(self.patterns['inline_math'].findall(text)) + 
                          len(self.patterns['dollar_inline'].findall(text)),
            'display_math': len(self.patterns['display_math'].findall(text)) + 
                           len(self.patterns['dollar_display'].findall(text)),
        }
        
        # Count Greek letters and math symbols
        for symbol in self.greek_letters:
            stats['greek_letters'] += text.count(symbol)
        
        for symbol in self.math_symbols:
            stats['math_symbols'] += text.count(symbol)
        
        return stats


# Default renderer instance
default_renderer = LatexRenderer()


def render_latex(text: str, config: Optional[LatexRenderingConfig] = None) -> str:
    """
    Convenience function for rendering LaTeX expressions.
    
    Args:
        text: Text containing LaTeX expressions
        config: Optional rendering configuration
        
    Returns:
        str: Rendered text with Unicode symbols
    """
    if config:
        renderer = LatexRenderer(config)
        return renderer.render_latex(text)
    else:
        return default_renderer.render_latex(text)


if __name__ == "__main__":
    """Test suite for LaTeX renderer."""
    print("🧪 Testing LaTeX Renderer...")
    
    # Test cases for mathematical expressions
    test_cases = [
        # Basic symbols
        "The equation \\alpha + \\beta = \\gamma is fundamental",
        "We have \\sum_{i=1}^{n} x_i = \\int_0^\\infty f(x) dx",
        
        # Fractions and roots
        "The fraction \\frac{a}{b} and root \\sqrt{x^2 + y^2}",
        "Binomial coefficient \\binom{n}{k} = \\frac{n!}{k!(n-k)!}",
        
        # Set notation
        "Real numbers \\mathbb{R} and complex numbers \\mathbb{C}",
        
        # Accents and formatting
        "Vector \\vec{v} with components \\hat{x} and \\tilde{y}",
        "Bold \\mathbf{A} and italic \\textit{text}",
        
        # Complex expressions
        "\\lim_{x \\to \\infty} \\frac{\\sin(x)}{x} = 0 for all x \\in \\mathbb{R}",
        
        # Inline and display math
        "Inline \\(E = mc^2\\) and display \\[\\nabla \\cdot \\vec{E} = \\frac{\\rho}{\\epsilon_0}\\]",
    ]
    
    # Test 1: Basic rendering
    print("\n📋 Basic Rendering Tests:")
    renderer = LatexRenderer()
    
    for i, test_case in enumerate(test_cases, 1):
        result = renderer.render_latex(test_case)
        print(f"Test {i}:")
        print(f"  Input:  {test_case}")
        print(f"  Output: {result}")
        print()
    
    # Test 2: Configuration options
    print("\n⚙️ Configuration Tests:")
    configs = [
        ("No Unicode", LatexRenderingConfig(enable_unicode_symbols=False)),
        ("No Rich", LatexRenderingConfig(enable_rich_formatting=False)),
        ("Plain Math", LatexRenderingConfig(preserve_math_delimiters=False)),
    ]
    
    test_expr = "\\alpha^2 + \\beta_1 = \\mathbb{R} with \\(x \\in \\mathbb{N}\\)"
    
    for name, config in configs:
        renderer_config = LatexRenderer(config)
        result = renderer_config.render_latex(test_expr)
        print(f"{name}: {result}")
    
    # Test 3: Validation
    print("\n✅ Validation Tests:")
    validation_tests = [
        ("Valid: \\alpha + \\beta", True),
        ("Invalid: \\alpha + \\beta}", False),
        ("Invalid: \\unknown{command}", False),
    ]
    
    for test_text, expected_valid in validation_tests:
        is_valid, issues = renderer.validate_latex(test_text)
        status = "✅" if is_valid == expected_valid else "❌"
        print(f"{status} {test_text}: valid={is_valid}, issues={issues}")
    
    # Test 4: Statistics
    print("\n📊 Statistics Test:")
    complex_expr = "\\sum_{i=1}^{n} \\alpha_i \\cdot \\beta^2 = \\frac{\\pi}{\\sqrt{2}} \\in \\mathbb{R}"
    stats = renderer.get_rendering_stats(complex_expr)
    print(f"Expression: {complex_expr}")
    print(f"Statistics: {stats}")
    
    print("\n✅ LaTeX Renderer Test Complete") 