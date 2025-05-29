"""
Markdown Renderer for Academic Papers and Mathematical Content.

This module provides enhanced markdown rendering with support for 
mathematical expressions, academic formatting, and beautiful console display.
Integrates with the LaTeX renderer for comprehensive mathematical content.
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .latex_renderer import LatexRenderer, LatexRenderingConfig


logger = logging.getLogger(__name__)


@dataclass
class MarkdownRenderingConfig:
    """Configuration for markdown rendering behavior."""
    enable_latex_processing: bool = True
    enable_rich_panels: bool = True
    enable_syntax_highlighting: bool = True
    panel_title: str = "🤖 Agent"
    panel_expand: bool = False
    fallback_to_plain: bool = True
    academic_formatting: bool = True


class MarkdownRenderer:
    """
    Enhanced markdown renderer for academic papers and mathematical content.
    
    This class handles the rendering of markdown text with LaTeX mathematical
    expressions, optimized for console display with Rich formatting.
    Designed for beautiful presentation of mathematical and academic content.
    """
    
    def __init__(
        self, 
        config: Optional[MarkdownRenderingConfig] = None,
        latex_config: Optional[LatexRenderingConfig] = None
    ):
        """
        Initialize the markdown renderer.
        
        Args:
            config: Optional configuration for markdown rendering
            latex_config: Optional configuration for LaTeX rendering
        """
        self.config = config or MarkdownRenderingConfig()
        self.latex_renderer = LatexRenderer(latex_config) if self.config.enable_latex_processing else None
        self._check_rich_availability()
    
    def _check_rich_availability(self) -> None:
        """Check if Rich library is available for enhanced rendering."""
        try:
            from rich.markdown import Markdown
            from rich.console import Console
            from rich.panel import Panel
            from rich.syntax import Syntax
            
            self.rich_available = True
            self._markdown_cls = Markdown
            self._console_cls = Console
            self._panel_cls = Panel
            self._syntax_cls = Syntax
            
            logger.info("Rich library available - enhanced rendering enabled")
            
        except ImportError as e:
            self.rich_available = False
            logger.warning(f"Rich library not available: {e}. Falling back to plain text rendering.")
            if self.config.fallback_to_plain:
                print("Rich library not available. Falling back to plain text rendering.")
    
    def render_response(self, text: str, title: Optional[str] = None) -> None:
        """
        Render a response with markdown and LaTeX processing.
        
        Args:
            text: Text content to render (may contain markdown and LaTeX)
            title: Optional panel title (defaults to config value)
        """
        panel_title = title or self.config.panel_title
        
        # Process LaTeX first if enabled
        if self.config.enable_latex_processing and self.latex_renderer:
            try:
                text = self.latex_renderer.render_latex(text)
            except Exception as e:
                logger.error(f"LaTeX rendering failed: {e}")
                # Continue with original text
        
        # Enhance for academic formatting
        if self.config.academic_formatting:
            text = self._enhance_academic_formatting(text)
        
        # Render with Rich if available
        if self.rich_available and self.config.enable_rich_panels:
            self._render_with_rich(text, panel_title)
        else:
            self._render_plain_text(text, panel_title)
    
    def render_panel(self, text: str, title: str, expand: Optional[bool] = None) -> None:
        """
        Render text in a panel with specified title.
        
        Args:
            text: Text content to render
            title: Panel title
            expand: Whether to expand panel (defaults to config value)
        """
        expand_panel = expand if expand is not None else self.config.panel_expand
        
        # Process LaTeX if enabled
        if self.config.enable_latex_processing and self.latex_renderer:
            try:
                text = self.latex_renderer.render_latex(text)
            except Exception as e:
                logger.error(f"LaTeX rendering failed: {e}")
        
        # Academic formatting
        if self.config.academic_formatting:
            text = self._enhance_academic_formatting(text)
        
        if self.rich_available:
            self._render_panel_rich(text, title, expand_panel)
        else:
            self._render_panel_plain(text, title)
    
    def render_code(self, code: str, language: str = "python", title: Optional[str] = None) -> None:
        """
        Render code with syntax highlighting.
        
        Args:
            code: Code content
            language: Programming language for syntax highlighting
            title: Optional title for the code block
        """
        if self.rich_available and self.config.enable_syntax_highlighting:
            self._render_code_rich(code, language, title)
        else:
            self._render_code_plain(code, title)
    
    def _enhance_academic_formatting(self, text: str) -> str:
        """
        Enhance text with academic formatting patterns.
        
        Args:
            text: Input text
            
        Returns:
            Enhanced text with academic formatting
        """
        # Add spacing around mathematical expressions
        import re
        
        # Add spacing around display math
        text = re.sub(r'\n\n\[b\]\[([^\]]+)\]\[/b\]\n\n', r'\n\n---\n**\1**\n---\n\n', text)
        
        # Enhance theorem-like environments
        theorem_patterns = [
            (r'\*\*Theorem\*\*', '🔷 **Theorem**'),
            (r'\*\*Lemma\*\*', '🔸 **Lemma**'),
            (r'\*\*Proof\*\*', '📝 **Proof**'),
            (r'\*\*Definition\*\*', '📚 **Definition**'),
            (r'\*\*Corollary\*\*', '⭐ **Corollary**'),
            (r'\*\*Example\*\*', '💡 **Example**'),
            (r'\*\*Remark\*\*', '💭 **Remark**'),
        ]
        
        for pattern, replacement in theorem_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Enhance citations and references
        text = re.sub(r'\[(\d+)\]', r'[[cyan]\1[/cyan]]', text)  # Numeric citations
        text = re.sub(r'\(([A-Za-z]+\s+\d{4})\)', r'([cyan]\1[/cyan])', text)  # Author year citations
        
        # Enhance section headers
        text = re.sub(r'^## (.+)$', r'## 📖 \1', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'### 📑 \1', text, flags=re.MULTILINE)
        
        return text
    
    def _render_with_rich(self, text: str, title: str) -> None:
        """Render text using Rich markdown with panel."""
        try:
            console = self._console_cls()
            markdown = self._markdown_cls(text)
            panel = self._panel_cls(
                markdown, 
                title=title, 
                expand=self.config.panel_expand
            )
            console.print(panel)
            
        except Exception as e:
            logger.error(f"Rich rendering failed: {e}")
            if self.config.fallback_to_plain:
                self._render_plain_text(text, title)
            else:
                raise
    
    def _render_panel_rich(self, text: str, title: str, expand: bool) -> None:
        """Render panel using Rich."""
        try:
            console = self._console_cls()
            markdown = self._markdown_cls(text)
            panel = self._panel_cls(markdown, title=title, expand=expand)
            console.print(panel)
            
        except Exception as e:
            logger.error(f"Rich panel rendering failed: {e}")
            if self.config.fallback_to_plain:
                self._render_panel_plain(text, title)
            else:
                raise
    
    def _render_code_rich(self, code: str, language: str, title: Optional[str]) -> None:
        """Render code with Rich syntax highlighting."""
        try:
            console = self._console_cls()
            syntax = self._syntax_cls(code, language, theme="monokai", line_numbers=True)
            
            if title:
                panel = self._panel_cls(syntax, title=title, expand=False)
                console.print(panel)
            else:
                console.print(syntax)
                
        except Exception as e:
            logger.error(f"Rich code rendering failed: {e}")
            if self.config.fallback_to_plain:
                self._render_code_plain(code, title)
            else:
                raise
    
    def _render_plain_text(self, text: str, title: str) -> None:
        """Fallback plain text rendering."""
        print(f"\n{'='*60}")
        print(f" {title}")
        print('='*60)
        print(text)
        print('='*60)
    
    def _render_panel_plain(self, text: str, title: str) -> None:
        """Fallback plain panel rendering."""
        print(f"\n┌─ {title} " + "─" * (50 - len(title)))
        for line in text.split('\n'):
            print(f"│ {line}")
        print("└" + "─" * 50)
    
    def _render_code_plain(self, code: str, title: Optional[str]) -> None:
        """Fallback plain code rendering."""
        if title:
            print(f"\n--- {title} ---")
        print("```")
        print(code)
        print("```")
    
    def get_rendering_capabilities(self) -> Dict[str, bool]:
        """
        Get information about available rendering capabilities.
        
        Returns:
            Dict containing capability flags
        """
        return {
            "rich_available": self.rich_available,
            "latex_processing": self.config.enable_latex_processing,
            "syntax_highlighting": self.config.enable_syntax_highlighting,
            "academic_formatting": self.config.academic_formatting,
            "panel_rendering": self.config.enable_rich_panels,
        }
    
    def validate_markdown(self, text: str) -> Dict[str, Any]:
        """
        Validate markdown content and provide statistics.
        
        Args:
            text: Markdown text to validate
            
        Returns:
            Dict containing validation results and statistics
        """
        import re
        
        stats = {
            "total_lines": len(text.split('\n')),
            "headers": len(re.findall(r'^#+\s', text, re.MULTILINE)),
            "code_blocks": len(re.findall(r'```', text)) // 2,
            "links": len(re.findall(r'\[([^\]]+)\]\([^)]+\)', text)),
            "bold_text": len(re.findall(r'\*\*([^*]+)\*\*', text)),
            "italic_text": len(re.findall(r'\*([^*]+)\*', text)),
            "list_items": len(re.findall(r'^\s*[-*+]\s', text, re.MULTILINE)),
        }
        
        # LaTeX validation if enabled
        latex_stats = {}
        if self.config.enable_latex_processing and self.latex_renderer:
            latex_stats = self.latex_renderer.get_rendering_stats(text)
        
        return {
            "markdown_stats": stats,
            "latex_stats": latex_stats,
            "has_mathematical_content": latex_stats.get('total_commands', 0) > 0,
            "is_academic_content": any(pattern in text.lower() for pattern in 
                                      ['theorem', 'proof', 'lemma', 'definition', 'corollary'])
        }


# Default renderer instance
default_renderer = MarkdownRenderer()


def render_response(text: str, title: Optional[str] = None) -> None:
    """
    Convenience function for rendering responses.
    
    Args:
        text: Text to render
        title: Optional panel title
    """
    default_renderer.render_response(text, title)


def render_panel(text: str, title: str, expand: Optional[bool] = None) -> None:
    """
    Convenience function for rendering panels.
    
    Args:
        text: Text to render
        title: Panel title
        expand: Whether to expand panel
    """
    default_renderer.render_panel(text, title, expand)


def render_code(code: str, language: str = "python", title: Optional[str] = None) -> None:
    """
    Convenience function for rendering code.
    
    Args:
        code: Code to render
        language: Programming language
        title: Optional title
    """
    default_renderer.render_code(code, language, title)


if __name__ == "__main__":
    """Test suite for markdown renderer."""
    print("🧪 Testing Markdown Renderer...")
    
    # Test 1: Basic markdown with LaTeX
    print("\n📋 Basic Markdown + LaTeX Test:")
    test_content = """
# Mathematical Content Example

This is a **theorem** with mathematical notation:

**Theorem 1**: For any real number \\alpha \\in \\mathbb{R}, we have:

\\[\\sum_{i=1}^{n} \\alpha_i = \\int_0^\\infty f(x) dx\\]

**Proof**: The proof follows from the fundamental theorem of calculus.

## Code Example

Here's some Python code:

```python
def calculate_sum(numbers):
    return sum(numbers)
```

## References

See [Smith 2023] for more details.
"""
    
    renderer = MarkdownRenderer()
    renderer.render_response(test_content, "📚 Mathematical Paper")
    
    # Test 2: Configuration options
    print("\n⚙️ Configuration Tests:")
    
    configs = [
        ("No LaTeX", MarkdownRenderingConfig(enable_latex_processing=False)),
        ("No Academic", MarkdownRenderingConfig(academic_formatting=False)),
        ("Plain fallback", MarkdownRenderingConfig(enable_rich_panels=False)),
    ]
    
    simple_content = "**Theorem**: \\alpha + \\beta = \\gamma for all \\alpha, \\beta \\in \\mathbb{R}"
    
    for name, config in configs:
        print(f"\n--- {name} ---")
        test_renderer = MarkdownRenderer(config)
        test_renderer.render_panel(simple_content, f"Test: {name}")
    
    # Test 3: Validation and statistics
    print("\n📊 Validation Test:")
    validation_result = renderer.validate_markdown(test_content)
    print(f"Validation results: {validation_result}")
    
    # Test 4: Capabilities
    print("\n🔧 Capabilities Test:")
    capabilities = renderer.get_rendering_capabilities()
    print(f"Renderer capabilities: {capabilities}")
    
    # Test 5: Code rendering
    print("\n💻 Code Rendering Test:")
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 10 Fibonacci numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""
    renderer.render_code(sample_code, "python", "🐍 Fibonacci Implementation")
    
    print("\n✅ Markdown Renderer Test Complete") 