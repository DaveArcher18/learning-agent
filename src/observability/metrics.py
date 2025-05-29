"""
Performance metrics collection and reporting for Learning Agent.

This module provides comprehensive metrics tracking for all services including
response times, success rates, service health, and system resource monitoring.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from contextlib import contextmanager
from statistics import mean, median

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class MetricSnapshot:
    """
    Snapshot of metrics at a specific point in time.
    
    Contains metric values, timestamps, and metadata for analysis.
    """
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceMetrics:
    """
    Metrics for a specific service.
    
    Tracks performance, health, and usage statistics.
    """
    service_name: str
    request_count: int = 0
    success_count: int = 0
    error_count: int = 0
    total_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    last_success: Optional[datetime] = None
    last_error: Optional[datetime] = None
    recent_response_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.request_count == 0:
            return 0.0
        return (self.success_count / self.request_count) * 100
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate percentage."""
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100
    
    @property
    def avg_response_time(self) -> float:
        """Calculate average response time."""
        if self.success_count == 0:
            return 0.0
        return self.total_response_time / self.success_count
    
    @property
    def recent_avg_response_time(self) -> float:
        """Calculate recent average response time (last 100 requests)."""
        if not self.recent_response_times:
            return 0.0
        return mean(self.recent_response_times)
    
    @property
    def recent_median_response_time(self) -> float:
        """Calculate recent median response time (last 100 requests)."""
        if not self.recent_response_times:
            return 0.0
        return median(self.recent_response_times)


class MetricsCollector:
    """
    Comprehensive metrics collector for Learning Agent services.
    
    Collects, aggregates, and provides access to performance metrics
    for all system components.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.service_metrics: Dict[str, ServiceMetrics] = defaultdict(
            lambda: ServiceMetrics(service_name="unknown")
        )
        self.system_metrics: Dict[str, deque] = {
            "cpu_usage": deque(maxlen=100),
            "memory_usage": deque(maxlen=100),
            "disk_usage": deque(maxlen=100),
        }
        self.custom_metrics: Dict[str, List[MetricSnapshot]] = defaultdict(list)
        self.start_time = datetime.now()
        self._lock = threading.Lock()
        
        # Initialize system monitoring
        self._start_system_monitoring()
        
        logger.info("Metrics collector initialized")
    
    def _start_system_monitoring(self):
        """Start background system resource monitoring."""
        def monitor_system():
            while True:
                try:
                    # Collect system metrics
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    with self._lock:
                        self.system_metrics["cpu_usage"].append(cpu_percent)
                        self.system_metrics["memory_usage"].append(memory.percent)
                        self.system_metrics["disk_usage"].append(disk.percent)
                    
                    time.sleep(30)  # Collect every 30 seconds
                    
                except Exception as e:
                    logger.error(f"System monitoring error: {e}")
                    time.sleep(60)  # Retry after error
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
    
    @contextmanager
    def time_operation(self, service: str, operation: str = "request"):
        """
        Context manager for timing service operations.
        
        Args:
            service: Service name
            operation: Operation name
            
        Yields:
            Dict[str, Any]: Operation context
        """
        start_time = time.time()
        operation_context = {
            "service": service,
            "operation": operation,
            "start_time": start_time
        }
        
        try:
            yield operation_context
            
            # Record success
            response_time = time.time() - start_time
            self.record_success(service, response_time)
            
        except Exception as e:
            # Record error
            response_time = time.time() - start_time
            self.record_error(service, str(e), response_time)
            raise
    
    def record_success(self, service: str, response_time: float, metadata: Optional[Dict[str, Any]] = None):
        """
        Record a successful operation.
        
        Args:
            service: Service name
            response_time: Operation response time in seconds
            metadata: Optional metadata
        """
        with self._lock:
            metrics = self.service_metrics[service]
            metrics.service_name = service
            metrics.request_count += 1
            metrics.success_count += 1
            metrics.total_response_time += response_time
            metrics.min_response_time = min(metrics.min_response_time, response_time)
            metrics.max_response_time = max(metrics.max_response_time, response_time)
            metrics.last_success = datetime.now()
            metrics.recent_response_times.append(response_time)
        
        # Log the success
        logger.info(
            "Operation success recorded",
            extra={
                "event_type": "metrics.success",
                "service": service,
                "response_time": response_time,
                "metadata": metadata or {}
            }
        )
    
    def record_error(self, service: str, error: str, response_time: Optional[float] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Record a failed operation.
        
        Args:
            service: Service name
            error: Error message
            response_time: Optional response time in seconds
            metadata: Optional metadata
        """
        with self._lock:
            metrics = self.service_metrics[service]
            metrics.service_name = service
            metrics.request_count += 1
            metrics.error_count += 1
            metrics.last_error = datetime.now()
        
        # Log the error
        logger.error(
            "Operation error recorded",
            extra={
                "event_type": "metrics.error",
                "service": service,
                "error": error,
                "response_time": response_time,
                "metadata": metadata or {}
            }
        )
    
    def record_custom_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Record a custom metric.
        
        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for categorization
            metadata: Optional metadata
        """
        snapshot = MetricSnapshot(
            timestamp=datetime.now(),
            metric_name=name,
            value=value,
            tags=tags or {},
            metadata=metadata or {}
        )
        
        with self._lock:
            self.custom_metrics[name].append(snapshot)
            
            # Keep only last 1000 snapshots per metric
            if len(self.custom_metrics[name]) > 1000:
                self.custom_metrics[name] = self.custom_metrics[name][-1000:]
        
        logger.info(
            "Custom metric recorded",
            extra={
                "event_type": "metrics.custom",
                "metric_name": name,
                "value": value,
                "tags": tags or {},
                "metadata": metadata or {}
            }
        )
    
    def get_service_summary(self, service: str) -> Dict[str, Any]:
        """
        Get comprehensive summary for a service.
        
        Args:
            service: Service name
            
        Returns:
            Dict[str, Any]: Service metrics summary
        """
        with self._lock:
            metrics = self.service_metrics.get(service)
            if not metrics:
                return {"error": f"No metrics found for service: {service}"}
            
            return {
                "service": service,
                "uptime": str(datetime.now() - self.start_time),
                "requests": {
                    "total": metrics.request_count,
                    "successful": metrics.success_count,
                    "failed": metrics.error_count,
                    "success_rate": round(metrics.success_rate, 2),
                    "error_rate": round(metrics.error_rate, 2)
                },
                "response_times": {
                    "average": round(metrics.avg_response_time, 3),
                    "recent_average": round(metrics.recent_avg_response_time, 3),
                    "recent_median": round(metrics.recent_median_response_time, 3),
                    "min": round(metrics.min_response_time, 3) if metrics.min_response_time != float('inf') else 0,
                    "max": round(metrics.max_response_time, 3)
                },
                "last_activity": {
                    "last_success": metrics.last_success.isoformat() if metrics.last_success else None,
                    "last_error": metrics.last_error.isoformat() if metrics.last_error else None
                }
            }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """
        Get system resource summary.
        
        Returns:
            Dict[str, Any]: System metrics summary
        """
        with self._lock:
            return {
                "uptime": str(datetime.now() - self.start_time),
                "cpu": {
                    "current": psutil.cpu_percent(),
                    "average": round(mean(self.system_metrics["cpu_usage"]) if self.system_metrics["cpu_usage"] else 0, 2),
                    "samples": len(self.system_metrics["cpu_usage"])
                },
                "memory": {
                    "current": psutil.virtual_memory().percent,
                    "average": round(mean(self.system_metrics["memory_usage"]) if self.system_metrics["memory_usage"] else 0, 2),
                    "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                    "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                    "samples": len(self.system_metrics["memory_usage"])
                },
                "disk": {
                    "current": psutil.disk_usage('/').percent,
                    "average": round(mean(self.system_metrics["disk_usage"]) if self.system_metrics["disk_usage"] else 0, 2),
                    "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                    "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
                    "samples": len(self.system_metrics["disk_usage"])
                }
            }
    
    def get_all_services_summary(self) -> Dict[str, Any]:
        """
        Get summary for all services.
        
        Returns:
            Dict[str, Any]: All services metrics summary
        """
        with self._lock:
            services_summary = {}
            for service_name in self.service_metrics.keys():
                services_summary[service_name] = self.get_service_summary(service_name)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "system": self.get_system_summary(),
                "services": services_summary,
                "custom_metrics_count": len(self.custom_metrics)
            }
    
    def get_custom_metrics_summary(self, metric_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get custom metrics summary.
        
        Args:
            metric_name: Optional specific metric name
            
        Returns:
            Dict[str, Any]: Custom metrics summary
        """
        with self._lock:
            if metric_name:
                if metric_name not in self.custom_metrics:
                    return {"error": f"Metric not found: {metric_name}"}
                
                snapshots = self.custom_metrics[metric_name]
                if not snapshots:
                    return {"metric": metric_name, "snapshots": 0}
                
                values = [s.value for s in snapshots]
                return {
                    "metric": metric_name,
                    "snapshots": len(snapshots),
                    "latest_value": snapshots[-1].value,
                    "latest_timestamp": snapshots[-1].timestamp.isoformat(),
                    "statistics": {
                        "min": min(values),
                        "max": max(values),
                        "average": mean(values),
                        "median": median(values)
                    }
                }
            else:
                # Summary of all custom metrics
                summary = {}
                for name, snapshots in self.custom_metrics.items():
                    if snapshots:
                        values = [s.value for s in snapshots]
                        summary[name] = {
                            "snapshots": len(snapshots),
                            "latest_value": snapshots[-1].value,
                            "latest_timestamp": snapshots[-1].timestamp.isoformat(),
                            "average": round(mean(values), 3)
                        }
                
                return summary
    
    def export_metrics(self, format_type: str = "json") -> Dict[str, Any]:
        """
        Export all metrics in structured format.
        
        Args:
            format_type: Export format (currently only 'json')
            
        Returns:
            Dict[str, Any]: Exported metrics data
        """
        return {
            "export_timestamp": datetime.now().isoformat(),
            "format": format_type,
            "data": self.get_all_services_summary(),
            "custom_metrics": self.get_custom_metrics_summary()
        }
    
    def reset_metrics(self, service: Optional[str] = None):
        """
        Reset metrics for a service or all services.
        
        Args:
            service: Optional service name to reset (resets all if None)
        """
        with self._lock:
            if service:
                if service in self.service_metrics:
                    del self.service_metrics[service]
                    logger.info(f"Metrics reset for service: {service}")
            else:
                self.service_metrics.clear()
                self.custom_metrics.clear()
                self.start_time = datetime.now()
                logger.info("All metrics reset")


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """
    Get or create the global metrics collector instance.
    
    Returns:
        MetricsCollector: Global metrics collector
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


# Convenience functions for common operations
def record_llm_request(provider: str, model: str, response_time: float, success: bool, token_count: Optional[int] = None):
    """Record LLM request metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success(f"llm.{provider}", response_time, {"model": model, "tokens": token_count})
    else:
        collector.record_error(f"llm.{provider}", "Request failed", response_time, {"model": model})
    
    # Custom metrics
    if token_count:
        collector.record_custom_metric("llm.tokens_processed", token_count, {"provider": provider, "model": model})


def record_rag_retrieval(response_time: float, results_count: int, success: bool, mode: str = "hybrid"):
    """Record RAG retrieval metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success("rag.retrieval", response_time, {"mode": mode, "results": results_count})
        collector.record_custom_metric("rag.results_count", results_count, {"mode": mode})
    else:
        collector.record_error("rag.retrieval", "Retrieval failed", response_time, {"mode": mode})


def record_ragflow_operation(operation: str, response_time: float, success: bool, metadata: Optional[Dict[str, Any]] = None):
    """Record RAGFlow operation metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success(f"ragflow.{operation}", response_time, metadata)
    else:
        collector.record_error(f"ragflow.{operation}", "Operation failed", response_time, metadata)


def record_knowledge_processing(file_size: int, chunks_created: int, processing_time: float, success: bool):
    """Record knowledge processing metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success("knowledge.processing", processing_time, {"file_size": file_size, "chunks": chunks_created})
        collector.record_custom_metric("knowledge.chunks_created", chunks_created, {"file_size_mb": file_size / (1024*1024)})
        collector.record_custom_metric("knowledge.processing_speed", file_size / processing_time, {"unit": "bytes_per_second"})
    else:
        collector.record_error("knowledge.processing", "Processing failed", processing_time, {"file_size": file_size})


def record_command_execution(command: str, duration: float, success: bool, args: Optional[str] = None):
    """Record command execution metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success(f"command.{command}", duration, {"args": args})
    else:
        collector.record_error(f"command.{command}", "Command failed", duration, {"args": args})


def record_mathematical_content(latex_expressions: int, rendering_time: float, success: bool):
    """Record mathematical content processing metrics."""
    collector = get_metrics_collector()
    
    if success:
        collector.record_success("math.rendering", rendering_time, {"expressions": latex_expressions})
        collector.record_custom_metric("math.expressions_processed", latex_expressions)
    else:
        collector.record_error("math.rendering", "Rendering failed", rendering_time, {"expressions": latex_expressions}) 