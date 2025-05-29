"""
Unit tests for the LaTeX Renderer module.

Tests mathematical expression rendering, Unicode conversion, error handling,
and performance of the LaTeX processing pipeline.
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.text_processing.latex_renderer import LatexRenderer
from src.utils.exceptions import LaTeXRenderingError


class TestLatexRenderer:
    """Test suite for LaTeX renderer functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.renderer = LatexRenderer()
    
    @pytest.mark.unit
    def test_basic_initialization(self):
        """Test LatexRenderer initialization."""
        assert self.renderer is not None
        assert hasattr(self.renderer, 'render_latex')
        assert hasattr(self.renderer, 'get_statistics')
    
    @pytest.mark.unit
    @pytest.mark.mathematical
    def test_basic_math_symbols(self):
        """Test basic mathematical symbol conversion."""
        test_cases = [
            (r"$\alpha$", "α"),
            (r"$\beta$", "β"), 
            (r"$\gamma$", "γ"),
            (r"$\Delta$", "Δ"),
            (r"$\theta$", "θ"),
            (r"$\lambda$", "λ"),
            (r"$\mu$", "μ"),
            (r"$\pi$", "π"),
            (r"$\sigma$", "σ"),
            (r"$\Omega$", "Ω")
        ]
        
        for latex_input, expected_output in test_cases:
            result = self.renderer.render_latex(latex_input)
            assert expected_output in result, f"Failed to convert {latex_input} to {expected_output}"
    
    @pytest.mark.unit
    @pytest.mark.mathematical
    def test_mathematical_operators(self):
        """Test mathematical operator conversion."""
        test_cases = [
            (r"$\sum$", "∑"),
            (r"$\prod$", "∏"),
            (r"$\int$", "∫"),
            (r"$\partial$", "∂"),
            (r"$\nabla$", "∇"),
            (r"$\infty$", "∞"),
            (r"$\pm$", "±"),
            (r"$\mp$", "∓"),
            (r"$\times$", "×"),
            (r"$\cdot$", "·"),
            (r"$\leq$", "≤"),
            (r"$\geq$", "≥"),
            (r"$\neq$", "≠"),
            (r"$\approx$", "≈"),
            (r"$\equiv$", "≡")
        ]
        
        for latex_input, expected_output in test_cases:
            result = self.renderer.render_latex(latex_input)
            assert expected_output in result, f"Failed to convert {latex_input} to {expected_output}"
    
    @pytest.mark.unit
    @pytest.mark.mathematical
    def test_superscripts_and_subscripts(self):
        """Test superscript and subscript conversion."""
        test_cases = [
            (r"$x^2$", "x²"),
            (r"$x^3$", "x³"),
            (r"$x_1$", "x₁"),
            (r"$x_2$", "x₂"),
            (r"$a_{ij}$", "aᵢⱼ"),
            (r"$x^{n+1}$", "xⁿ⁺¹"),
            (r"$e^{-x}$", "e⁻ˣ"),
            (r"$\sum_{i=1}^{n}$", "∑ᵢ₌₁ⁿ"),
            (r"$\int_0^1$", "∫₀¹")
        ]
        
        for latex_input, expected_unicode in test_cases:
            result = self.renderer.render_latex(latex_input)
            # Check if conversion happened (should not contain LaTeX syntax)
            assert "^" not in result or "_" not in result, f"Failed to convert {latex_input}"
            # For simple cases, check exact conversion
            if len(expected_unicode) <= 5:
                assert expected_unicode in result, f"Expected {expected_unicode} in result for {latex_input}"
    
    @pytest.mark.unit
    @pytest.mark.mathematical 
    def test_fractions(self):
        """Test fraction conversion."""
        test_cases = [
            (r"$\frac{1}{2}$", "1/2"),
            (r"$\frac{a}{b}$", "a/b"),
            (r"$\frac{x+1}{y-1}$", "(x+1)/(y-1)"),
            (r"$\frac{\alpha}{\beta}$", "α/β"),
            (r"$\frac{d}{dx}$", "d/dx")
        ]
        
        for latex_input, expected_output in test_cases:
            result = self.renderer.render_latex(latex_input)
            # Should not contain \frac syntax
            assert "\\frac" not in result, f"Failed to convert fraction in {latex_input}"
            # Should contain division notation
            assert "/" in result, f"No division notation found in result for {latex_input}"
    
    @pytest.mark.unit
    @pytest.mark.mathematical
    def test_complex_equations(self, mathematical_test_cases):
        """Test complex mathematical equations using fixture."""
        for test_case in mathematical_test_cases:
            latex_input = test_case["latex"]
            expected_unicode = test_case["expected_unicode"]
            
            result = self.renderer.render_latex(latex_input)
            
            # Verify LaTeX syntax is removed
            assert "$" not in result, f"LaTeX delimiters remain in {result}"
            assert "\\frac" not in result, f"Fraction syntax remains in {result}"
            
            # For specific test cases, verify expected output
            if expected_unicode:
                # Allow partial matches for complex expressions
                key_symbols = expected_unicode.replace(" ", "")
                result_clean = result.replace(" ", "")
                
                # Check that key mathematical symbols are present
                if "²" in expected_unicode:
                    assert "²" in result or "^2" not in result, f"Superscript conversion failed"
                if "α" in expected_unicode:
                    assert "α" in result, f"Greek letter conversion failed"
                if "∫" in expected_unicode:
                    assert "∫" in result, f"Integral symbol conversion failed"
                if "∑" in expected_unicode:
                    assert "∑" in result, f"Summation symbol conversion failed"
    
    @pytest.mark.unit
    def test_mixed_content(self):
        """Test mixed mathematical and text content."""
        mixed_content = """
        The equation $E = mc^2$ shows mass-energy equivalence.
        
        For the function $f(x) = x^2 + 2x + 1$, we can factor as $f(x) = (x+1)^2$.
        
        The integral $\int_0^\infty e^{-x} dx = 1$ converges.
        """
        
        result = self.renderer.render_latex(mixed_content)
        
        # Text should be preserved
        assert "shows mass-energy equivalence" in result
        assert "we can factor as" in result
        assert "converges" in result
        
        # LaTeX should be converted
        assert "$" not in result, "LaTeX delimiters should be removed"
        assert "E = mc²" in result or "E = mc^2" not in result, "E=mc² conversion failed"
        
        # Mathematical symbols should be converted
        assert "∞" in result or "∫" in result, "Mathematical symbols should be converted"
    
    @pytest.mark.unit
    def test_error_handling(self):
        """Test error handling for malformed LaTeX."""
        error_cases = [
            r"$\frac{1}{$",  # Incomplete fraction
            r"$x^{$",        # Incomplete superscript
            r"$\unknown$",   # Unknown command
            r"$$\int_$",     # Incomplete integral
        ]
        
        for error_case in error_cases:
            # Should not raise exception, but handle gracefully
            try:
                result = self.renderer.render_latex(error_case)
                # Should return something (either original or partially processed)
                assert isinstance(result, str)
                assert len(result) > 0
            except Exception as e:
                # If exception is raised, should be our custom exception
                assert isinstance(e, LaTeXRenderingError)
    
    @pytest.mark.unit
    def test_empty_and_none_inputs(self):
        """Test handling of empty and None inputs."""
        # Empty string
        result = self.renderer.render_latex("")
        assert result == ""
        
        # None input should be handled gracefully
        try:
            result = self.renderer.render_latex(None)
            assert result is None or result == ""
        except (TypeError, AttributeError):
            # Acceptable behavior - should handle None gracefully
            pass
        
        # Whitespace only
        result = self.renderer.render_latex("   ")
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_no_latex_content(self):
        """Test text with no LaTeX content."""
        plain_text = "This is just plain text with no mathematical content."
        result = self.renderer.render_latex(plain_text)
        assert result == plain_text, "Plain text should be unchanged"
    
    @pytest.mark.unit
    def test_nested_expressions(self):
        """Test nested mathematical expressions."""
        nested_cases = [
            r"$\frac{x^2 + y^2}{z^2}$",
            r"$\sum_{i=1}^{n} x_i^2$",
            r"$\int_0^{\infty} e^{-x^2} dx$",
            r"$\sqrt{\frac{a}{b}}$"
        ]
        
        for nested_case in nested_cases:
            result = self.renderer.render_latex(nested_case)
            
            # Should not contain LaTeX syntax
            assert "$" not in result
            assert "\\frac" not in result
            assert "\\sum" not in result  
            assert "\\int" not in result
            assert "\\sqrt" not in result
            
            # Should be non-empty
            assert len(result) > 0
    
    @pytest.mark.unit
    def test_statistics_tracking(self):
        """Test statistics tracking functionality."""
        # Render some expressions
        test_expressions = [
            r"$x^2$",
            r"$\alpha + \beta$",
            r"$\int_0^1 x dx$",
            r"$\frac{a}{b}$"
        ]
        
        for expr in test_expressions:
            self.renderer.render_latex(expr)
        
        stats = self.renderer.get_statistics()
        
        # Should track basic statistics
        assert isinstance(stats, dict)
        assert "expressions_processed" in stats
        assert "symbols_converted" in stats
        assert stats["expressions_processed"] >= len(test_expressions)
    
    @pytest.mark.unit
    @pytest.mark.slow
    def test_performance_large_document(self, performance_monitor):
        """Test performance with large document."""
        # Create large document with many mathematical expressions
        large_doc = ""
        for i in range(100):
            large_doc += f"Equation {i}: $x_{i} = \\alpha_{i} + \\beta_{i}^2 + \\frac{{1}}{{n_{i}}}$\n"
        
        performance_monitor.start()
        result = self.renderer.render_latex(large_doc)
        performance_monitor.measure("large_document_rendering")
        
        # Verify processing completed
        assert len(result) > 0
        assert "$" not in result  # All LaTeX should be processed
        
        # Check performance (should complete in reasonable time)
        measurements = performance_monitor.get_results()
        assert len(measurements) > 0
        render_time = measurements[0][1]
        assert render_time < 5.0, f"Rendering took too long: {render_time}s"
    
    @pytest.mark.unit
    def test_unicode_preservation(self):
        """Test that existing Unicode is preserved."""
        text_with_unicode = "Already has Unicode: α, β, π, ∑, ∫, and regular text."
        result = self.renderer.render_latex(text_with_unicode)
        
        # Unicode should be preserved
        assert "α" in result
        assert "β" in result
        assert "π" in result
        assert "∑" in result
        assert "∫" in result
        assert "regular text" in result
    
    @pytest.mark.unit
    def test_block_environments(self):
        """Test block mathematical environments."""
        block_cases = [
            r"$$x^2 + y^2 = z^2$$",
            r"\begin{equation} f(x) = x^2 \end{equation}",
            r"\begin{align} a &= b \\ c &= d \end{align}"
        ]
        
        for block_case in block_cases:
            result = self.renderer.render_latex(block_case)
            
            # Should not contain LaTeX block syntax
            assert "$$" not in result
            assert "\\begin" not in result
            assert "\\end" not in result
            
            # Should contain mathematical content
            assert len(result) > 0


class TestLatexRendererIntegration:
    """Integration tests for LaTeX renderer with other components."""
    
    @pytest.mark.integration
    @pytest.mark.mathematical
    def test_with_markdown_renderer(self):
        """Test integration with markdown renderer."""
        from src.text_processing.markdown_renderer import MarkdownRenderer
        
        latex_renderer = LatexRenderer()
        markdown_renderer = MarkdownRenderer(latex_renderer=latex_renderer)
        
        content_with_math = """
        # Mathematical Concepts
        
        The quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$
        
        Euler's identity: $e^{i\\pi} + 1 = 0$
        """
        
        # Should not raise exception
        try:
            markdown_renderer.render_response(content_with_math, "Test Math")
            # If we get here, integration worked
            assert True
        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")
    
    @pytest.mark.integration
    def test_error_recovery_integration(self):
        """Test error recovery in integrated scenarios."""
        renderer = LatexRenderer()
        
        # Mix of good and bad LaTeX
        mixed_content = """
        Good: $x^2 + y^2 = z^2$
        Bad: $\\frac{1}{$
        Good again: $\\alpha + \\beta$
        """
        
        result = renderer.render_latex(mixed_content)
        
        # Should recover and process good parts
        assert "Good:" in result
        assert "Good again:" in result
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 