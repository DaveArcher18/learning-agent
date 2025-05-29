"""
Academic Paper Processing Commands for Learning Agent.

This module provides commands for the Week 7 academic paper processing pipeline:
- Academic paper analysis and structure extraction
- Mathematical content indexing and search
- Citation validation and quality assurance
- Comprehensive quality assurance reporting

Designed for maintainability, modularity, simplicity, and observability.
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from .base import Command, CommandResult
from ...rag.processing.academic_papers import (
    AcademicPaperProcessor, 
    process_academic_paper,
    AcademicPaperStructure
)
from ...text_processing.math_indexer import (
    MathematicalIndexer,
    build_mathematical_index,
    calculate_mathematical_similarity
)
from ...rag.processing.quality_assurance import (
    QualityAssurancePipeline,
    run_quality_assurance,
    validate_citations
)

logger = logging.getLogger(__name__)


class AcademicAnalyzeCommand(Command):
    """Command for analyzing academic papers with comprehensive structure extraction."""
    
    def __init__(self):
        super().__init__()
        self.name = "academic"
        self.description = "Analyze academic papers with citation and mathematical content extraction"
        self.aliases = ["paper", "analyze"]
        self.console = Console()
        
        # Initialize processors
        self.paper_processor = AcademicPaperProcessor()
        self.math_indexer = MathematicalIndexer()
        self.qa_pipeline = QualityAssurancePipeline()
    
    def execute(self, agent, args: List[str]) -> CommandResult:
        """Execute academic paper analysis."""
        try:
            if not args:
                return self._show_help()
            
            subcommand = args[0].lower()
            
            if subcommand == "process":
                return self._process_paper(args[1:])
            elif subcommand == "index":
                return self._build_mathematical_index(args[1:])
            elif subcommand == "validate":
                return self._validate_citations(args[1:])
            elif subcommand == "quality":
                return self._run_quality_assurance(args[1:])
            elif subcommand == "search":
                return self._search_equations(args[1:])
            elif subcommand == "stats":
                return self._show_statistics()
            else:
                return self._show_help()
        
        except Exception as e:
            logger.error(f"Error in academic command: {e}")
            return CommandResult(
                success=False,
                message=f"Academic analysis error: {e}",
                data={"error": str(e)}
            )
    
    def _show_help(self) -> CommandResult:
        """Show help for academic commands."""
        help_table = Table(title="📚 Academic Paper Processing Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        help_table.add_column("Usage", style="green")
        
        commands = [
            ("process", "Process academic paper with structure extraction", "academic process <file_path>"),
            ("index", "Build mathematical index for paper", "academic index <file_path>"),
            ("validate", "Validate citations in processed paper", "academic validate <paper_json>"),
            ("quality", "Run comprehensive quality assurance", "academic quality <paper_json>"),
            ("search", "Search similar equations", "academic search <equation_latex>"),
            ("stats", "Show processing statistics", "academic stats"),
        ]
        
        for cmd, desc, usage in commands:
            help_table.add_row(cmd, desc, usage)
        
        self.console.print(help_table)
        
        return CommandResult(
            success=True,
            message="Academic paper processing commands",
            data={"commands": [cmd[0] for cmd in commands]}
        )
    
    def _process_paper(self, args: List[str]) -> CommandResult:
        """Process an academic paper file."""
        if not args:
            return CommandResult(
                success=False,
                message="Usage: academic process <file_path>",
                data={}
            )
        
        file_path = Path(args[0])
        
        if not file_path.exists():
            return CommandResult(
                success=False,
                message=f"File not found: {file_path}",
                data={}
            )
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                
                # Read file content
                task1 = progress.add_task("Reading paper content...", total=None)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                progress.update(task1, completed=100)
                
                # Process paper
                task2 = progress.add_task("Processing academic paper...", total=None)
                paper_structure = self.paper_processor.process_paper(
                    content, 
                    metadata={"file_path": str(file_path)}
                )
                progress.update(task2, completed=100)
                
                # Build mathematical index
                task3 = progress.add_task("Building mathematical index...", total=None)
                math_index = self.math_indexer.build_mathematical_index(
                    content, 
                    document_id=file_path.stem
                )
                progress.update(task3, completed=100)
                
                # Run quality assurance
                task4 = progress.add_task("Running quality assurance...", total=None)
                qa_report = self.qa_pipeline.run_comprehensive_qa(
                    paper_structure,
                    mathematical_index=math_index
                )
                progress.update(task4, completed=100)
            
            # Display results
            self._display_processing_results(paper_structure, math_index, qa_report)
            
            # Save results
            output_dir = Path("output/academic_processing")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save paper structure
            structure_file = output_dir / f"{file_path.stem}_structure.json"
            self.paper_processor.export_structure(paper_structure, structure_file)
            
            # Save mathematical index
            index_file = output_dir / f"{file_path.stem}_math_index.json"
            self.math_indexer.export_index(math_index, index_file)
            
            # Save QA report
            qa_file = output_dir / f"{file_path.stem}_qa_report.json"
            self.qa_pipeline.export_qa_report(qa_report, qa_file)
            
            return CommandResult(
                success=True,
                message=f"Successfully processed academic paper: {file_path.name}",
                data={
                    "paper_structure": paper_structure,
                    "mathematical_index": math_index,
                    "qa_report": qa_report,
                    "output_files": {
                        "structure": str(structure_file),
                        "math_index": str(index_file),
                        "qa_report": str(qa_file),
                    }
                }
            )
        
        except Exception as e:
            logger.error(f"Error processing paper: {e}")
            return CommandResult(
                success=False,
                message=f"Error processing paper: {e}",
                data={"error": str(e)}
            )
    
    def _build_mathematical_index(self, args: List[str]) -> CommandResult:
        """Build mathematical index for a paper."""
        if not args:
            return CommandResult(
                success=False,
                message="Usage: academic index <file_path>",
                data={}
            )
        
        file_path = Path(args[0])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with self.console.status("Building mathematical index..."):
                math_index = build_mathematical_index(content, file_path.stem)
            
            # Display index summary
            self._display_mathematical_index_summary(math_index)
            
            # Save index
            output_file = Path(f"output/{file_path.stem}_math_index.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            self.math_indexer.export_index(math_index, output_file)
            
            return CommandResult(
                success=True,
                message=f"Mathematical index built for {file_path.name}",
                data={
                    "math_index": math_index,
                    "output_file": str(output_file)
                }
            )
        
        except Exception as e:
            logger.error(f"Error building mathematical index: {e}")
            return CommandResult(
                success=False,
                message=f"Error building mathematical index: {e}",
                data={"error": str(e)}
            )
    
    def _validate_citations(self, args: List[str]) -> CommandResult:
        """Validate citations in a processed paper."""
        if not args:
            return CommandResult(
                success=False,
                message="Usage: academic validate <paper_structure.json>",
                data={}
            )
        
        json_path = Path(args[0])
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract citations from JSON data
            citations = []
            for cite_data in data.get('citations', {}).values():
                from ...rag.processing.academic_papers import Citation
                citation = Citation(
                    key=cite_data['key'],
                    text=cite_data['text'],
                    authors=cite_data.get('authors', []),
                    title=cite_data.get('title'),
                    venue=cite_data.get('venue'),
                    year=cite_data.get('year'),
                    citation_type=cite_data.get('citation_type', 'unknown')
                )
                citations.append(citation)
            
            if not citations:
                return CommandResult(
                    success=False,
                    message="No citations found in the paper structure",
                    data={}
                )
            
            with self.console.status("Validating citations..."):
                validation_results = validate_citations(citations)
            
            # Display validation results
            self._display_citation_validation(validation_results)
            
            return CommandResult(
                success=True,
                message=f"Validated {len(citations)} citations",
                data={"validation_results": validation_results}
            )
        
        except Exception as e:
            logger.error(f"Error validating citations: {e}")
            return CommandResult(
                success=False,
                message=f"Error validating citations: {e}",
                data={"error": str(e)}
            )
    
    def _run_quality_assurance(self, args: List[str]) -> CommandResult:
        """Run comprehensive quality assurance."""
        if not args:
            return CommandResult(
                success=False,
                message="Usage: academic quality <paper_structure.json>",
                data={}
            )
        
        json_path = Path(args[0])
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Reconstruct paper structure from JSON
            from ...rag.processing.academic_papers import AcademicPaperStructure, Citation
            
            paper_structure = AcademicPaperStructure(
                title=data.get('title'),
                authors=data.get('authors', []),
                abstract=data.get('abstract'),
                sections=data.get('sections', {})
            )
            
            # Add citations
            for cite_key, cite_data in data.get('citations', {}).items():
                citation = Citation(
                    key=cite_data['key'],
                    text=cite_data['text'],
                    authors=cite_data.get('authors', []),
                    title=cite_data.get('title'),
                    venue=cite_data.get('venue'),
                    year=cite_data.get('year'),
                    citation_type=cite_data.get('citation_type', 'unknown')
                )
                paper_structure.citations[cite_key] = citation
            
            with self.console.status("Running quality assurance..."):
                qa_report = run_quality_assurance(paper_structure)
            
            # Display QA results
            self._display_qa_results(qa_report)
            
            # Save QA report
            output_file = Path(f"output/{json_path.stem}_qa_report.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            self.qa_pipeline.export_qa_report(qa_report, output_file)
            
            return CommandResult(
                success=True,
                message="Quality assurance completed",
                data={
                    "qa_report": qa_report,
                    "output_file": str(output_file)
                }
            )
        
        except Exception as e:
            logger.error(f"Error running quality assurance: {e}")
            return CommandResult(
                success=False,
                message=f"Error running quality assurance: {e}",
                data={"error": str(e)}
            )
    
    def _search_equations(self, args: List[str]) -> CommandResult:
        """Search for similar equations."""
        if not args:
            return CommandResult(
                success=False,
                message="Usage: academic search <equation_latex>",
                data={}
            )
        
        equation_latex = " ".join(args)
        
        try:
            # This is a simplified version - in practice would search against indexed equations
            self.console.print(f"🔍 Searching for equations similar to: {equation_latex}")
            
            # For demonstration, show similarity calculation between sample equations
            sample_equations = [
                "x^2 + y^2 = r^2",
                "\\frac{df}{dx} = f'(x)",
                "E = mc^2",
                "\\sum_{i=1}^n i = \\frac{n(n+1)}{2}",
                "\\int_a^b f(x)dx"
            ]
            
            results_table = Table(title="Similar Equations")
            results_table.add_column("Equation", style="cyan")
            results_table.add_column("Similarity", style="green")
            results_table.add_column("Type", style="yellow")
            
            for eq in sample_equations:
                similarity = calculate_mathematical_similarity(equation_latex, eq)
                eq_type = "algebraic" if "^" in eq else "calculus" if any(op in eq for op in ["\\int", "\\frac{d"]) else "geometric"
                results_table.add_row(eq, f"{similarity:.3f}", eq_type)
            
            self.console.print(results_table)
            
            return CommandResult(
                success=True,
                message=f"Found similar equations for: {equation_latex}",
                data={"query": equation_latex, "results": sample_equations}
            )
        
        except Exception as e:
            logger.error(f"Error searching equations: {e}")
            return CommandResult(
                success=False,
                message=f"Error searching equations: {e}",
                data={"error": str(e)}
            )
    
    def _show_statistics(self) -> CommandResult:
        """Show academic processing statistics."""
        try:
            # Get statistics from processors
            paper_stats = self.paper_processor.get_processing_statistics()
            qa_stats = self.qa_pipeline.get_qa_statistics()
            
            # Display statistics
            stats_table = Table(title="📊 Academic Processing Statistics")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green")
            
            stats_table.add_row("Papers Processed", str(paper_stats.get('papers_processed', 0)))
            stats_table.add_row("Total Citations Extracted", str(paper_stats.get('total_citations_extracted', 0)))
            stats_table.add_row("Total Math Elements", str(paper_stats.get('total_math_elements_classified', 0)))
            stats_table.add_row("Avg Citations per Paper", f"{paper_stats.get('avg_citations_per_paper', 0):.1f}")
            stats_table.add_row("Avg Math Elements per Paper", f"{paper_stats.get('avg_math_elements_per_paper', 0):.1f}")
            stats_table.add_row("Average Quality Score", f"{qa_stats.get('average_quality_score', 0):.3f}")
            stats_table.add_row("Citation Validation Rate", f"{qa_stats.get('citation_validation_rate', 0):.1%}")
            
            self.console.print(stats_table)
            
            return CommandResult(
                success=True,
                message="Academic processing statistics",
                data={"paper_stats": paper_stats, "qa_stats": qa_stats}
            )
        
        except Exception as e:
            logger.error(f"Error showing statistics: {e}")
            return CommandResult(
                success=False,
                message=f"Error showing statistics: {e}",
                data={"error": str(e)}
            )
    
    def _display_processing_results(self, structure: AcademicPaperStructure, 
                                  math_index, qa_report: Dict[str, Any]) -> None:
        """Display comprehensive processing results."""
        
        # Paper overview
        overview_table = Table(title="📄 Paper Processing Results")
        overview_table.add_column("Aspect", style="cyan")
        overview_table.add_column("Details", style="white")
        
        overview_table.add_row("Title", structure.title or "Unknown")
        overview_table.add_row("Authors", ", ".join(structure.authors) if structure.authors else "None")
        overview_table.add_row("Sections", str(len(structure.sections)))
        overview_table.add_row("Citations", str(len(structure.citations)))
        overview_table.add_row("Math Elements", str(len(structure.mathematical_elements)))
        overview_table.add_row("Equations Indexed", str(len(math_index.equations)))
        overview_table.add_row("Concepts Extracted", str(len(math_index.concepts)))
        
        self.console.print(overview_table)
        
        # Quality assessment
        if qa_report.get('overall_assessment'):
            assessment = qa_report['overall_assessment']
            quality_level = assessment['quality_level']
            overall_score = assessment['overall_score']
            
            # Color code quality level
            color = "green" if quality_level in ["excellent", "good"] else "yellow" if quality_level == "acceptable" else "red"
            
            quality_panel = Panel(
                f"Overall Score: {overall_score:.3f}\n"
                f"Quality Level: {quality_level.upper()}\n"
                f"Components Assessed: {assessment['total_components_assessed']}",
                title="🎯 Quality Assessment",
                border_style=color
            )
            self.console.print(quality_panel)
            
            # Show issues and recommendations
            if assessment.get('issues_identified'):
                issues_text = "\n".join(f"• {issue}" for issue in assessment['issues_identified'])
                self.console.print(Panel(issues_text, title="⚠️ Issues Identified", border_style="yellow"))
            
            if assessment.get('recommendations'):
                rec_text = "\n".join(f"• {rec}" for rec in assessment['recommendations'])
                self.console.print(Panel(rec_text, title="💡 Recommendations", border_style="blue"))
    
    def _display_mathematical_index_summary(self, math_index) -> None:
        """Display mathematical index summary."""
        
        summary_table = Table(title="🔢 Mathematical Index Summary")
        summary_table.add_column("Component", style="cyan")
        summary_table.add_column("Count", style="green")
        summary_table.add_column("Details", style="white")
        
        # Equations by type
        eq_types = {}
        for eq in math_index.equations.values():
            eq_types[eq.equation_type] = eq_types.get(eq.equation_type, 0) + 1
        
        summary_table.add_row("Total Equations", str(len(math_index.equations)), 
                             ", ".join(f"{k}: {v}" for k, v in eq_types.items()))
        
        # Concepts by type
        concept_types = {}
        for concept in math_index.concepts.values():
            concept_types[concept.concept_type] = concept_types.get(concept.concept_type, 0) + 1
        
        summary_table.add_row("Total Concepts", str(len(math_index.concepts)),
                             ", ".join(f"{k}: {v}" for k, v in concept_types.items()))
        
        # Graph statistics
        if math_index.concept_graph:
            summary_table.add_row("Concept Graph Nodes", str(math_index.concept_graph.number_of_nodes()), "")
            summary_table.add_row("Concept Graph Edges", str(math_index.concept_graph.number_of_edges()), "")
        
        self.console.print(summary_table)
    
    def _display_citation_validation(self, validation_results) -> None:
        """Display citation validation results."""
        
        validation_table = Table(title="📚 Citation Validation Results")
        validation_table.add_column("Citation", style="cyan")
        validation_table.add_column("Valid", style="green")
        validation_table.add_column("Confidence", style="yellow")
        validation_table.add_column("Issues", style="red")
        
        for result in validation_results:
            citation = result.citation
            valid_icon = "✅" if result.is_valid else "❌"
            confidence = f"{result.confidence_score:.2f}"
            issues = ", ".join(result.validation_errors) if result.validation_errors else "None"
            
            validation_table.add_row(
                citation.key,
                valid_icon,
                confidence,
                issues[:50] + "..." if len(issues) > 50 else issues
            )
        
        self.console.print(validation_table)
        
        # Summary
        valid_count = sum(1 for r in validation_results if r.is_valid)
        total_count = len(validation_results)
        
        summary_text = f"Validation Summary: {valid_count}/{total_count} citations valid ({valid_count/total_count:.1%})"
        color = "green" if valid_count/total_count >= 0.8 else "yellow" if valid_count/total_count >= 0.6 else "red"
        
        self.console.print(Panel(summary_text, border_style=color))
    
    def _display_qa_results(self, qa_report: Dict[str, Any]) -> None:
        """Display quality assurance results."""
        
        qa_table = Table(title="🛡️ Quality Assurance Results")
        qa_table.add_column("Component", style="cyan")
        qa_table.add_column("Score", style="green")
        qa_table.add_column("Status", style="white")
        
        # Content quality
        content_quality = qa_report.get('content_quality')
        if content_quality:
            score = f"{content_quality.overall_score:.3f}"
            status = content_quality.quality_level.value
            qa_table.add_row("Content Quality", score, status)
        
        # Citation validation
        citation_results = qa_report.get('citation_validation', [])
        if citation_results:
            valid_count = sum(1 for r in citation_results if r.is_valid)
            score = f"{valid_count/len(citation_results):.3f}"
            status = f"{valid_count}/{len(citation_results)} valid"
            qa_table.add_row("Citation Quality", score, status)
        
        # Overall assessment
        overall = qa_report.get('overall_assessment')
        if overall:
            score = f"{overall['overall_score']:.3f}"
            status = overall['quality_level']
            qa_table.add_row("Overall Quality", score, status.upper())
        
        self.console.print(qa_table) 