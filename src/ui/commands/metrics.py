"""
Metrics command for viewing performance data and system statistics.

This module provides commands to view service performance metrics,
system resource usage, and export data for analysis.
"""

from typing import Any, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

from .base import Command, CommandResult
from ..console_interface import ConsoleInterface
from ...observability.metrics import get_metrics_collector
from ...observability.logger import get_logger

logger = get_logger(__name__)
console = Console()


class MetricsCommand(Command):
    """
    Command to view performance metrics and system statistics.
    
    Shows comprehensive metrics for all services including response times,
    success rates, and system resource usage.
    """
    
    name = "metrics"
    description = "View performance metrics and system statistics"
    aliases = ["stats", "performance", "monitor"]
    
    def execute(self, args: str, context: Dict[str, Any]) -> CommandResult:
        """
        Execute metrics command.
        
        Args:
            args: Command arguments (service name or 'export')
            context: Command execution context
            
        Returns:
            CommandResult: Command execution result
        """
        try:
            args = args.strip().lower()
            collector = get_metrics_collector()
            
            if args == "export":
                return self._export_metrics(collector)
            elif args == "system":
                return self._show_system_metrics(collector)
            elif args == "custom":
                return self._show_custom_metrics(collector)
            elif args == "reset":
                return self._reset_metrics(collector)
            elif args:
                return self._show_service_metrics(collector, args)
            else:
                return self._show_all_metrics(collector)
                
        except Exception as e:
            logger.error(f"Metrics command failed: {e}")
            return CommandResult(
                success=False,
                message=f"Failed to retrieve metrics: {str(e)}"
            )
    
    def _show_all_metrics(self, collector) -> CommandResult:
        """Show comprehensive metrics overview."""
        summary = collector.get_all_services_summary()
        
        # Create header
        header = Panel(
            Text(f"📊 Learning Agent Performance Metrics", style="bold blue"),
            subtitle=f"System Uptime: {summary['system']['uptime']}"
        )
        console.print(header)
        
        # System overview
        self._render_system_overview(summary["system"])
        
        # Services overview
        if summary["services"]:
            self._render_services_overview(summary["services"])
        else:
            console.print("\n[yellow]No service metrics available yet[/yellow]")
        
        # Custom metrics count
        if summary["custom_metrics_count"] > 0:
            console.print(f"\n[dim]📈 {summary['custom_metrics_count']} custom metric types tracked[/dim]")
        
        return CommandResult(
            success=True,
            message="Metrics displayed successfully",
            data=summary
        )
    
    def _render_system_overview(self, system_data: Dict[str, Any]):
        """Render system resource overview."""
        # CPU and Memory
        resource_table = Table(title="🖥️  System Resources", show_header=True, header_style="bold magenta")
        resource_table.add_column("Resource", style="cyan", no_wrap=True)
        resource_table.add_column("Current", style="green")
        resource_table.add_column("Average", style="yellow")
        resource_table.add_column("Details", style="dim")
        
        # CPU
        cpu_current = f"{system_data['cpu']['current']:.1f}%"
        cpu_avg = f"{system_data['cpu']['average']:.1f}%"
        cpu_samples = f"{system_data['cpu']['samples']} samples"
        resource_table.add_row("CPU Usage", cpu_current, cpu_avg, cpu_samples)
        
        # Memory
        mem_current = f"{system_data['memory']['current']:.1f}%"
        mem_avg = f"{system_data['memory']['average']:.1f}%"
        mem_details = f"{system_data['memory']['available_gb']:.1f}GB / {system_data['memory']['total_gb']:.1f}GB available"
        resource_table.add_row("Memory Usage", mem_current, mem_avg, mem_details)
        
        # Disk
        disk_current = f"{system_data['disk']['current']:.1f}%"
        disk_avg = f"{system_data['disk']['average']:.1f}%"
        disk_details = f"{system_data['disk']['free_gb']:.1f}GB / {system_data['disk']['total_gb']:.1f}GB free"
        resource_table.add_row("Disk Usage", disk_current, disk_avg, disk_details)
        
        console.print(resource_table)
    
    def _render_services_overview(self, services_data: Dict[str, Any]):
        """Render services performance overview."""
        services_table = Table(title="⚡ Service Performance", show_header=True, header_style="bold green")
        services_table.add_column("Service", style="cyan", no_wrap=True)
        services_table.add_column("Requests", style="white")
        services_table.add_column("Success Rate", style="green")
        services_table.add_column("Avg Response", style="yellow")
        services_table.add_column("Recent Avg", style="blue")
        services_table.add_column("Status", style="magenta")
        
        for service_name, data in services_data.items():
            if "error" in data:
                continue
                
            requests = f"{data['requests']['total']:,}"
            success_rate = f"{data['requests']['success_rate']:.1f}%"
            avg_response = f"{data['response_times']['average']:.3f}s"
            recent_avg = f"{data['response_times']['recent_average']:.3f}s"
            
            # Determine status
            if data['requests']['total'] == 0:
                status = "🔷 No Activity"
            elif data['requests']['error_rate'] > 10:
                status = "🔴 High Errors"
            elif data['response_times']['recent_average'] > 5.0:
                status = "🟡 Slow"
            else:
                status = "🟢 Healthy"
            
            services_table.add_row(
                service_name,
                requests,
                success_rate,
                avg_response,
                recent_avg,
                status
            )
        
        console.print(services_table)
    
    def _show_service_metrics(self, collector, service_name: str) -> CommandResult:
        """Show detailed metrics for a specific service."""
        summary = collector.get_service_summary(service_name)
        
        if "error" in summary:
            return CommandResult(
                success=False,
                message=summary["error"]
            )
        
        # Service header
        header = Panel(
            Text(f"📊 {service_name} Service Metrics", style="bold blue"),
            subtitle=f"Uptime: {summary['uptime']}"
        )
        console.print(header)
        
        # Request statistics
        req_table = Table(title="📈 Request Statistics", show_header=True)
        req_table.add_column("Metric", style="cyan")
        req_table.add_column("Value", style="white")
        req_table.add_column("Percentage", style="green")
        
        req_data = summary["requests"]
        req_table.add_row("Total Requests", f"{req_data['total']:,}", "100%")
        req_table.add_row("Successful", f"{req_data['successful']:,}", f"{req_data['success_rate']:.1f}%")
        req_table.add_row("Failed", f"{req_data['failed']:,}", f"{req_data['error_rate']:.1f}%")
        
        console.print(req_table)
        
        # Response time statistics
        resp_table = Table(title="⏱️  Response Times", show_header=True)
        resp_table.add_column("Metric", style="cyan")
        resp_table.add_column("Value", style="yellow")
        
        resp_data = summary["response_times"]
        resp_table.add_row("Average", f"{resp_data['average']:.3f}s")
        resp_table.add_row("Recent Average", f"{resp_data['recent_average']:.3f}s")
        resp_table.add_row("Recent Median", f"{resp_data['recent_median']:.3f}s")
        resp_table.add_row("Minimum", f"{resp_data['min']:.3f}s")
        resp_table.add_row("Maximum", f"{resp_data['max']:.3f}s")
        
        console.print(resp_table)
        
        # Last activity
        activity_data = summary["last_activity"]
        if activity_data["last_success"] or activity_data["last_error"]:
            activity_table = Table(title="🕐 Last Activity", show_header=True)
            activity_table.add_column("Type", style="cyan")
            activity_table.add_column("Timestamp", style="white")
            
            if activity_data["last_success"]:
                activity_table.add_row("Last Success", activity_data["last_success"])
            if activity_data["last_error"]:
                activity_table.add_row("Last Error", activity_data["last_error"])
            
            console.print(activity_table)
        
        return CommandResult(
            success=True,
            message=f"Metrics for {service_name} displayed successfully",
            data=summary
        )
    
    def _show_system_metrics(self, collector) -> CommandResult:
        """Show detailed system resource metrics."""
        system_data = collector.get_system_summary()
        
        header = Panel(
            Text("🖥️  System Resource Metrics", style="bold blue"),
            subtitle=f"Uptime: {system_data['uptime']}"
        )
        console.print(header)
        
        # Create detailed system table
        system_table = Table(title="System Resources Detail", show_header=True)
        system_table.add_column("Resource", style="cyan", no_wrap=True)
        system_table.add_column("Current", style="green")
        system_table.add_column("Average", style="yellow")
        system_table.add_column("Total/Capacity", style="blue")
        system_table.add_column("Available/Free", style="magenta")
        system_table.add_column("Samples", style="dim")
        
        # CPU row
        cpu = system_data["cpu"]
        system_table.add_row(
            "CPU Usage",
            f"{cpu['current']:.1f}%",
            f"{cpu['average']:.1f}%",
            "N/A",
            "N/A",
            str(cpu['samples'])
        )
        
        # Memory row
        mem = system_data["memory"]
        system_table.add_row(
            "Memory Usage",
            f"{mem['current']:.1f}%",
            f"{mem['average']:.1f}%",
            f"{mem['total_gb']:.1f} GB",
            f"{mem['available_gb']:.1f} GB",
            str(mem['samples'])
        )
        
        # Disk row
        disk = system_data["disk"]
        system_table.add_row(
            "Disk Usage",
            f"{disk['current']:.1f}%",
            f"{disk['average']:.1f}%",
            f"{disk['total_gb']:.1f} GB",
            f"{disk['free_gb']:.1f} GB",
            str(disk['samples'])
        )
        
        console.print(system_table)
        
        return CommandResult(
            success=True,
            message="System metrics displayed successfully",
            data=system_data
        )
    
    def _show_custom_metrics(self, collector) -> CommandResult:
        """Show custom metrics summary."""
        custom_data = collector.get_custom_metrics_summary()
        
        if not custom_data:
            console.print("[yellow]No custom metrics available[/yellow]")
            return CommandResult(
                success=True,
                message="No custom metrics found"
            )
        
        header = Panel(
            Text("📈 Custom Metrics", style="bold blue"),
            subtitle=f"{len(custom_data)} metric types"
        )
        console.print(header)
        
        custom_table = Table(title="Custom Metrics Summary", show_header=True)
        custom_table.add_column("Metric", style="cyan")
        custom_table.add_column("Latest Value", style="green")
        custom_table.add_column("Average", style="yellow")
        custom_table.add_column("Snapshots", style="blue")
        custom_table.add_column("Last Updated", style="dim")
        
        for metric_name, data in custom_data.items():
            custom_table.add_row(
                metric_name,
                f"{data['latest_value']:.3f}",
                f"{data['average']:.3f}",
                str(data['snapshots']),
                data['latest_timestamp'][:19]  # Remove timezone info for display
            )
        
        console.print(custom_table)
        
        return CommandResult(
            success=True,
            message="Custom metrics displayed successfully",
            data=custom_data
        )
    
    def _export_metrics(self, collector) -> CommandResult:
        """Export all metrics to JSON format."""
        export_data = collector.export_metrics()
        
        console.print(Panel(
            Text("📄 Metrics Export", style="bold blue"),
            subtitle=f"Exported at {export_data['export_timestamp']}"
        ))
        
        # Show summary of exported data
        summary_table = Table(title="Export Summary", show_header=True)
        summary_table.add_column("Category", style="cyan")
        summary_table.add_column("Count", style="green")
        
        services_count = len(export_data['data']['services'])
        custom_count = len(export_data['custom_metrics'])
        
        summary_table.add_row("Services", str(services_count))
        summary_table.add_row("Custom Metrics", str(custom_count))
        summary_table.add_row("System Resources", "3")
        
        console.print(summary_table)
        
        console.print("\n[dim]💾 Use this data for analysis or reporting[/dim]")
        
        return CommandResult(
            success=True,
            message="Metrics exported successfully",
            data=export_data
        )
    
    def _reset_metrics(self, collector) -> CommandResult:
        """Reset all metrics after confirmation."""
        console.print("[yellow]⚠️  This will reset all performance metrics![/yellow]")
        confirm = input("Type 'RESET' to confirm: ")
        
        if confirm == "RESET":
            collector.reset_metrics()
            console.print("[green]✅ All metrics have been reset[/green]")
            return CommandResult(
                success=True,
                message="Metrics reset successfully"
            )
        else:
            console.print("[blue]Reset cancelled[/blue]")
            return CommandResult(
                success=True,
                message="Reset cancelled"
            )
    
    def get_help(self) -> str:
        """Get help text for the metrics command."""
        return """
📊 Metrics Command - View performance metrics and system statistics

Usage:
    metrics                 - Show all metrics overview
    metrics <service>       - Show detailed metrics for specific service
    metrics system          - Show detailed system resource metrics
    metrics custom          - Show custom metrics summary
    metrics export          - Export all metrics to JSON format
    metrics reset           - Reset all metrics (requires confirmation)

Examples:
    metrics                 - Complete metrics dashboard
    metrics llm.openai      - OpenAI service metrics
    metrics system          - System resource details
    metrics custom          - Custom application metrics
    metrics export          - Export for analysis

The metrics system tracks:
• Service response times and success rates
• System resource usage (CPU, memory, disk)
• Custom application metrics
• Request patterns and error rates
• Performance trends over time
        """.strip() 