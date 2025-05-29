"""
Health monitoring for Learning Agent services.

This module provides health checks for all services including
LLM providers, RAGFlow, and system components.
"""

import os
import time
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque, defaultdict

from .logger import get_logger
from ..core.config import ConfigManager

logger = get_logger(__name__)


@dataclass
class HealthStatus:
    """
    Health status information for a service.
    
    Contains the health status, details, and any error information.
    """
    service: str
    healthy: bool
    details: Dict[str, Any]
    error: Optional[str] = None
    response_time: Optional[float] = None
    degraded: bool = False
    recovery_attempted: bool = False


class ServiceDegradationDetector:
    """
    Detector for service degradation patterns.
    
    Monitors service health over time and identifies degradation
    patterns that may require intervention.
    """
    
    def __init__(self, window_size: int = 10):
        """Initialize degradation detector.
        
        Args:
            window_size: Number of recent health checks to consider
        """
        self.window_size = window_size
        self.health_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.degradation_alerts: Dict[str, datetime] = {}
    
    def record_health_check(self, service: str, healthy: bool, response_time: float):
        """Record a health check result."""
        self.health_history[service].append(healthy)
        self.response_times[service].append(response_time)
    
    def is_degraded(self, service: str) -> bool:
        """Check if a service shows signs of degradation."""
        if len(self.health_history[service]) < 3:
            return False
        
        recent_checks = list(self.health_history[service])
        recent_times = list(self.response_times[service])
        
        # Check for patterns indicating degradation
        success_rate = sum(recent_checks) / len(recent_checks)
        avg_response_time = sum(recent_times) / len(recent_times) if recent_times else 0
        
        # Degradation criteria
        degraded = (
            success_rate < 0.7 or  # Less than 70% success rate
            avg_response_time > 10.0 or  # Response time > 10 seconds
            (len(recent_checks) >= 5 and not any(recent_checks[-3:]))  # Last 3 failures
        )
        
        if degraded and service not in self.degradation_alerts:
            self.degradation_alerts[service] = datetime.now()
            logger.warning(f"Service degradation detected for {service}")
        elif not degraded and service in self.degradation_alerts:
            logger.info(f"Service {service} recovered from degradation")
            del self.degradation_alerts[service]
        
        return degraded
    
    def get_degraded_services(self) -> List[str]:
        """Get list of currently degraded services."""
        return list(self.degradation_alerts.keys())


class HealthChecker:
    """
    Health checker for all Learning Agent services.
    
    Provides comprehensive health monitoring for startup checks
    and ongoing service monitoring.
    """
    
    def __init__(self, config: ConfigManager, continuous_monitoring: bool = True):
        """
        Initialize health checker.
        
        Args:
            config: Configuration manager instance
            continuous_monitoring: Enable continuous background monitoring
        """
        self.config = config
        self.continuous_monitoring = continuous_monitoring
        self.degradation_detector = ServiceDegradationDetector()
        self.recovery_attempts: Dict[str, int] = defaultdict(int)
        self.last_health_check: Dict[str, datetime] = {}
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        
        logger.info("Health checker initialized")
        
        if continuous_monitoring:
            self._start_continuous_monitoring()
    
    def _start_continuous_monitoring(self):
        """Start continuous background health monitoring."""
        def monitor():
            while not self._stop_monitoring.wait(300):  # Check every 5 minutes
                try:
                    self._perform_background_health_check()
                except Exception as e:
                    logger.error(f"Background health monitoring error: {e}")
        
        self._monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self._monitoring_thread.start()
        logger.info("Continuous health monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous health monitoring."""
        if self._monitoring_thread:
            self._stop_monitoring.set()
            self._monitoring_thread.join(timeout=10)
            logger.info("Continuous health monitoring stopped")
    
    def _perform_background_health_check(self):
        """Perform background health check and handle degradation."""
        health_results = self.check_all_services()
        
        for service_name, health_status in health_results.items():
            # Record health check
            self.degradation_detector.record_health_check(
                service_name, 
                health_status.healthy, 
                health_status.response_time or 0
            )
            
            # Check for degradation
            if self.degradation_detector.is_degraded(service_name):
                self._attempt_service_recovery(service_name, health_status)
    
    def _attempt_service_recovery(self, service: str, health_status: HealthStatus):
        """Attempt to recover a degraded service."""
        if self.recovery_attempts[service] >= 3:
            logger.warning(f"Maximum recovery attempts reached for {service}")
            return
        
        self.recovery_attempts[service] += 1
        logger.info(f"Attempting recovery for {service} (attempt {self.recovery_attempts[service]})")
        
        try:
            recovery_success = False
            
            if service == "ragflow_service":
                recovery_success = self._recover_ragflow_service()
            elif service.startswith("llm."):
                recovery_success = self._recover_llm_service()
            elif service == "memory_service":
                recovery_success = self._recover_memory_service()
            
            if recovery_success:
                logger.info(f"Recovery successful for {service}")
                self.recovery_attempts[service] = 0  # Reset counter
            else:
                logger.warning(f"Recovery failed for {service}")
                
        except Exception as e:
            logger.error(f"Recovery attempt failed for {service}: {e}")
    
    def _recover_ragflow_service(self) -> bool:
        """Attempt to recover RAGFlow service."""
        try:
            from ..services.ragflow_service import RAGFlowService
            ragflow_service = RAGFlowService(self.config)
            
            # Try restarting the service
            ragflow_service.restart()
            time.sleep(30)  # Wait for service to start
            
            return ragflow_service.is_available()
        except Exception as e:
            logger.error(f"RAGFlow recovery failed: {e}")
            return False
    
    def _recover_llm_service(self) -> bool:
        """Attempt to recover LLM service."""
        try:
            # Simple recovery: just log and let next request handle reconnection
            logger.info("LLM service recovery: will reconnect on next request")
            return True
        except Exception as e:
            logger.error(f"LLM service recovery failed: {e}")
            return False
    
    def _recover_memory_service(self) -> bool:
        """Attempt to recover memory service."""
        try:
            from ..services.memory_service import MemoryService
            # Memory service is stateless, so just test functionality
            memory_service = MemoryService(enabled=True)
            test_message = "Recovery test"
            memory_service.add_user_message(test_message)
            memory_service.clear()
            return True
        except Exception as e:
            logger.error(f"Memory service recovery failed: {e}")
            return False
    
    def check_all_services(self) -> Dict[str, HealthStatus]:
        """
        Check health of all services.
        
        Returns:
            Dict[str, HealthStatus]: Health status for each service
        """
        logger.info("Starting comprehensive health check")
        
        health_results = {}
        
        # Configuration check
        health_results["configuration"] = self._check_configuration()
        
        # LLM service check
        health_results["llm_service"] = self._check_llm_service()
        
        # RAGFlow service check
        health_results["ragflow_service"] = self._check_ragflow_service()
        
        # Memory service check
        health_results["memory_service"] = self._check_memory_service()
        
        # System resources check
        health_results["system_resources"] = self._check_system_resources()
        
        # Mathematical content processing check
        health_results["math_rendering"] = self._check_math_rendering()
        
        # Update last check times
        current_time = datetime.now()
        for service in health_results.keys():
            self.last_health_check[service] = current_time
        
        logger.info(f"Health check completed. Results: {len(health_results)} services checked")
        return health_results
    
    def _check_math_rendering(self) -> HealthStatus:
        """
        Check mathematical content rendering capability.
        
        Returns:
            HealthStatus: Math rendering health status
        """
        start_time = time.time()
        
        try:
            from ..text_processing.latex_renderer import LatexRenderer
            
            renderer = LatexRenderer()
            test_latex = r"$\sum_{i=1}^{n} x_i = \frac{\alpha}{\beta}$"
            
            # Test rendering
            rendered = renderer.render_latex(test_latex)
            
            response_time = time.time() - start_time
            
            if rendered and rendered != test_latex:
                return HealthStatus(
                    service="math_rendering",
                    healthy=True,
                    details={
                        "renderer_available": True,
                        "test_successful": True,
                        "test_input": test_latex,
                        "test_output_length": len(rendered)
                    },
                    response_time=response_time
                )
            else:
                return HealthStatus(
                    service="math_rendering",
                    healthy=False,
                    details={
                        "renderer_available": True,
                        "test_successful": False
                    },
                    error="Math rendering test failed",
                    response_time=response_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            logger.warning(f"Math rendering health check failed: {e}")
            
            return HealthStatus(
                service="math_rendering",
                healthy=False,
                details={
                    "renderer_available": False
                },
                error=str(e),
                response_time=response_time
            )
    
    def get_service_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive service status summary."""
        health_results = self.check_all_services()
        degraded_services = self.degradation_detector.get_degraded_services()
        
        healthy_count = sum(1 for status in health_results.values() if status.healthy)
        total_count = len(health_results)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_health": healthy_count / total_count if total_count > 0 else 0,
            "healthy_services": healthy_count,
            "total_services": total_count,
            "degraded_services": degraded_services,
            "recovery_attempts": dict(self.recovery_attempts),
            "last_health_checks": {
                service: timestamp.isoformat() 
                for service, timestamp in self.last_health_check.items()
            },
            "services": {
                service: {
                    "healthy": status.healthy,
                    "degraded": status.service in degraded_services,
                    "response_time": status.response_time,
                    "error": status.error
                }
                for service, status in health_results.items()
            }
        }

    def check_configuration(self) -> bool:
        """
        Check if configuration is valid.
        
        Returns:
            bool: True if configuration is valid
        """
        return self._check_configuration().healthy
    
    def check_llm_service(self) -> bool:
        """
        Check if LLM service is available.
        
        Returns:
            bool: True if LLM service is healthy
        """
        return self._check_llm_service().healthy
    
    def check_ragflow_service(self) -> bool:
        """
        Check if RAGFlow service is available.
        
        Returns:
            bool: True if RAGFlow service is healthy
        """
        return self._check_ragflow_service().healthy
    
    def _check_configuration(self) -> HealthStatus:
        """
        Check configuration validity.
        
        Returns:
            HealthStatus: Configuration health status
        """
        start_time = time.time()
        
        try:
            # Check required configuration using new nested structure
            required_config = [
                "llm.model_provider",
                "llm.model", 
                "llm.temperature"
            ]
            
            missing_config = []
            for key in required_config:
                if not self.config.get(key):
                    missing_config.append(key)
            
            # Check environment variables for API keys
            provider_enum = self.config.get("llm.model_provider")
            provider = provider_enum.value.lower() if hasattr(provider_enum, 'value') else str(provider_enum).lower()
            api_key_env_vars = {
                "openai": "OPENAI_API_KEY",
                "openrouter": "OPENAI_API_KEY",  # OpenRouter uses OPENAI_API_KEY
                "deepseek": "DEEPSEEK_API_KEY", 
                "anthropic": "ANTHROPIC_API_KEY",
                "groq": "GROQ_API_KEY"
            }
            
            missing_env_vars = []
            if provider in api_key_env_vars:
                env_var = api_key_env_vars[provider]
                if not os.getenv(env_var):
                    missing_env_vars.append(env_var)
            
            # Check file paths
            config_file_issues = []
            if not os.path.exists(".env"):
                config_file_issues.append(".env file not found")
            
            response_time = time.time() - start_time
            
            if missing_config or missing_env_vars or config_file_issues:
                issues = []
                if missing_config:
                    issues.append(f"Missing config: {', '.join(missing_config)}")
                if missing_env_vars:
                    issues.append(f"Missing env vars: {', '.join(missing_env_vars)}")
                if config_file_issues:
                    issues.extend(config_file_issues)
                
                return HealthStatus(
                    service="configuration",
                    healthy=False,
                    details={
                        "missing_config": missing_config,
                        "missing_env_vars": missing_env_vars,
                        "file_issues": config_file_issues,
                        "provider": provider
                    },
                    error="; ".join(issues),
                    response_time=response_time
                )
            
            return HealthStatus(
                service="configuration",
                healthy=True,
                details={
                    "provider": provider,
                    "model": self.config.get("llm.model"),
                    "config_file_exists": os.path.exists(".env")
                },
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Configuration health check failed: {e}")
            
            return HealthStatus(
                service="configuration",
                healthy=False,
                details={},
                error=str(e),
                response_time=response_time
            )
    
    def _check_llm_service(self) -> HealthStatus:
        """
        Check LLM service health.
        
        Returns:
            HealthStatus: LLM service health status
        """
        start_time = time.time()
        
        try:
            from ..services.llm_service import LLMService
            
            # Create LLM service instance
            llm_service = LLMService(self.config)
            
            # Test basic functionality
            test_response = llm_service.generate_response(
                "Hello", 
                messages=[],
                max_tokens=10
            )
            
            response_time = time.time() - start_time
            
            if test_response:
                return HealthStatus(
                    service="llm_service",
                    healthy=True,
                    details={
                        "provider": self.config.get("llm.model_provider"),
                        "model": self.config.get("llm.model"),
                        "test_response_length": len(test_response),
                        "connection_successful": True
                    },
                    response_time=response_time
                )
            else:
                return HealthStatus(
                    service="llm_service",
                    healthy=False,
                    details={
                        "provider": self.config.get("llm.model_provider"),
                        "model": self.config.get("llm.model")
                    },
                    error="Empty response from LLM service",
                    response_time=response_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            logger.warning(f"LLM service health check failed: {e}")
            
            return HealthStatus(
                service="llm_service",
                healthy=False,
                details={
                    "provider": self.config.get("llm.model_provider", "unknown"),
                    "model": self.config.get("llm.model", "unknown")
                },
                error=str(e),
                response_time=response_time
            )
    
    def _check_ragflow_service(self) -> HealthStatus:
        """
        Check RAGFlow service health.
        
        Returns:
            HealthStatus: RAGFlow service health status
        """
        start_time = time.time()
        
        try:
            from ..services.ragflow_service import RAGFlowService
            
            # Create RAGFlow service instance
            ragflow_service = RAGFlowService(self.config)
            
            # Check if service is available
            is_available = ragflow_service.is_available()
            docker_status = ragflow_service.get_docker_status()
            
            response_time = time.time() - start_time
            
            if is_available:
                return HealthStatus(
                    service="ragflow_service",
                    healthy=True,
                    details={
                        "docker_status": docker_status,
                        "service_available": True,
                        "knowledge_bases": ragflow_service.get_knowledge_base_count(),
                        "model_loaded": ragflow_service.is_model_loaded("bge-m3")
                    },
                    response_time=response_time
                )
            else:
                return HealthStatus(
                    service="ragflow_service",
                    healthy=False,
                    details={
                        "docker_status": docker_status,
                        "service_available": False
                    },
                    error="RAGFlow service not available",
                    response_time=response_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            logger.warning(f"RAGFlow service health check failed: {e}")
            
            return HealthStatus(
                service="ragflow_service",
                healthy=False,
                details={
                    "docker_status": "unknown",
                    "service_available": False
                },
                error=str(e),
                response_time=response_time
            )
    
    def _check_memory_service(self) -> HealthStatus:
        """
        Check memory service health.
        
        Returns:
            HealthStatus: Memory service health status
        """
        start_time = time.time()
        
        try:
            from ..services.memory_service import MemoryService
            
            # Create memory service instance
            memory_service = MemoryService(enabled=True)
            
            # Test basic functionality
            test_message = "Health check test message"
            memory_service.add_user_message(test_message)
            messages = memory_service.get_messages()
            memory_service.clear()  # Clean up test message
            
            response_time = time.time() - start_time
            
            if messages and len(messages) > 0:
                return HealthStatus(
                    service="memory_service",
                    healthy=True,
                    details={
                        "enabled": memory_service.is_enabled(),
                        "max_messages": memory_service.get_max_messages(),
                        "test_successful": True
                    },
                    response_time=response_time
                )
            else:
                return HealthStatus(
                    service="memory_service",
                    healthy=False,
                    details={
                        "enabled": memory_service.is_enabled()
                    },
                    error="Memory service test failed",
                    response_time=response_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Memory service health check failed: {e}")
            
            return HealthStatus(
                service="memory_service",
                healthy=False,
                details={},
                error=str(e),
                response_time=response_time
            )
    
    def _check_system_resources(self) -> HealthStatus:
        """
        Check system resources.
        
        Returns:
            HealthStatus: System resources health status
        """
        start_time = time.time()
        
        try:
            import psutil
            
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            response_time = time.time() - start_time
            
            # Check if resources are within acceptable limits
            warnings = []
            if cpu_percent > 80:
                warnings.append(f"High CPU usage: {cpu_percent}%")
            if memory.percent > 80:
                warnings.append(f"High memory usage: {memory.percent}%")
            if disk.percent > 90:
                warnings.append(f"High disk usage: {disk.percent}%")
            
            return HealthStatus(
                service="system_resources",
                healthy=len(warnings) == 0,
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_percent": disk.percent,
                    "disk_free_gb": disk.free / (1024**3)
                },
                error="; ".join(warnings) if warnings else None,
                response_time=response_time
            )
            
        except ImportError:
            # psutil not available, return basic info
            response_time = time.time() - start_time
            return HealthStatus(
                service="system_resources",
                healthy=True,
                details={
                    "note": "psutil not available, limited system info"
                },
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"System resources health check failed: {e}")
            
            return HealthStatus(
                service="system_resources",
                healthy=False,
                details={},
                error=str(e),
                response_time=response_time
            ) 