"""
Pytest fixtures and test utilities for the Learning Agent.

This module provides reusable fixtures for testing all components of the learning agent,
including service mocks, configuration setup, and test data generation.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, MagicMock, patch
import pytest
from dataclasses import dataclass

# Test configuration
@pytest.fixture
def test_config():
    """Provide a minimal test configuration."""
    return {
        "llm": {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 2048
        },
        "ragflow": {
            "host": "localhost",
            "port": 9380,
            "knowledge_base": "test_kb",
            "docker_image": "ragflow/ragflow:latest"
        },
        "bge_m3": {
            "device": "cpu",
            "batch_size": 4,
            "max_length": 8192,
            "dense_dim": 512
        },
        "mathematical_content": {
            "latex_rendering": True,
            "preserve_equations": True,
            "math_symbol_mapping": True
        },
        "observability": {
            "logging_level": "WARNING",
            "enable_metrics": False,
            "health_check_interval": 300
        }
    }

@pytest.fixture
def test_config_file(test_config, tmp_path):
    """Create a temporary configuration file for testing."""
    config_file = tmp_path / "test_config.yaml"
    import yaml
    with open(config_file, 'w') as f:
        yaml.dump(test_config, f)
    return str(config_file)

# Service mocks
@pytest.fixture
def mock_llm_service():
    """Mock LLM service for testing."""
    mock = Mock()
    mock.get_current_provider.return_value = "deepseek"
    mock.get_available_providers.return_value = ["deepseek", "openai", "anthropic"]
    mock.switch_provider.return_value = True
    mock.generate_response.return_value = "Test response"
    mock.health_check.return_value = {"status": "healthy", "provider": "deepseek"}
    mock.get_metrics.return_value = {
        "requests_total": 10,
        "avg_response_time": 1.5,
        "error_rate": 0.0
    }
    return mock

@pytest.fixture  
def mock_ragflow_service():
    """Mock RAGFlow service for testing."""
    mock = Mock()
    mock.is_running.return_value = True
    mock.health_check.return_value = {"status": "healthy", "containers": 1}
    mock.create_knowledge_base.return_value = {"id": "test_kb", "name": "Test KB"}
    mock.upload_document.return_value = {"id": "test_doc", "status": "processing"}
    mock.get_knowledge_bases.return_value = [{"id": "test_kb", "name": "Test KB"}]
    mock.get_metrics.return_value = {
        "documents_processed": 5,
        "avg_processing_time": 10.0,
        "storage_used": "100MB"
    }
    return mock

@pytest.fixture
def mock_memory_service():
    """Mock memory service for testing."""
    mock = Mock()
    mock.add_message.return_value = None
    mock.get_conversation.return_value = [
        {"role": "user", "content": "Test question"},
        {"role": "assistant", "content": "Test answer"}
    ]
    mock.clear_memory.return_value = None
    mock.export_conversation.return_value = {"messages": [], "metadata": {}}
    mock.get_statistics.return_value = {
        "total_messages": 2,
        "session_duration": 300,
        "memory_usage": "1MB"
    }
    return mock

@pytest.fixture
def mock_ragflow_client():
    """Mock RAGFlow client for testing."""
    mock = Mock()
    mock.retrieve.return_value = [
        {
            "content": "Mathematical proof of theorem X",
            "source": "paper1.pdf",
            "score": 0.95,
            "citations": ["Theorem 1.1", "Proof on page 5"]
        }
    ]
    mock.health_check.return_value = True
    mock.get_knowledge_bases.return_value = ["test_kb"]
    return mock

# Test data fixtures
@pytest.fixture
def sample_latex_text():
    """Sample LaTeX text for testing rendering."""
    return r"""
    The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.
    
    For the integral $\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$.
    
    Greek letters: $\alpha, \beta, \gamma, \Delta, \Omega$.
    
    Complex equation: $f(x) = \sum_{n=0}^{\infty} \frac{x^n}{n!} = e^x$.
    """

@pytest.fixture
def sample_mathematical_content():
    """Sample mathematical content for testing processing."""
    return {
        "title": "Linear Algebra Fundamentals",
        "content": r"""
        ## Theorem 1.1: Matrix Multiplication
        
        Let $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$. 
        Then the product $C = AB$ is defined as:
        
        $$C_{ij} = \sum_{k=1}^{n} A_{ik}B_{kj}$$
        
        **Proof:** The proof follows from the definition of matrix multiplication...
        """,
        "citations": ["Reference 1", "Reference 2"],
        "mathematical_expressions": [
            r"$A \in \mathbb{R}^{m \times n}$",
            r"$$C_{ij} = \sum_{k=1}^{n} A_{ik}B_{kj}$$"
        ]
    }

@pytest.fixture
def sample_retrieval_results():
    """Sample retrieval results for testing."""
    return [
        {
            "id": "result_1",
            "content": "This is a mathematical theorem about linear transformations...",
            "source": "linear_algebra.pdf",
            "page": 15,
            "score": 0.92,
            "citations": ["Theorem 2.1", "Definition 2.3"],
            "mathematical_expressions": [r"$T: V \to W$", r"$\ker(T) = \{v \in V : T(v) = 0\}$"]
        },
        {
            "id": "result_2", 
            "content": "The eigenvalue problem can be written as...",
            "source": "eigenvalues.pdf",
            "page": 8,
            "score": 0.88,
            "citations": ["Definition 3.1"],
            "mathematical_expressions": [r"$Av = \lambda v$"]
        }
    ]

# Utility fixtures
@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture  
def mock_file_system(tmp_path):
    """Mock file system with test files."""
    # Create test files
    (tmp_path / "test_document.md").write_text("# Test Document\n\nSome content here.")
    (tmp_path / "math_paper.pdf").write_bytes(b"Mock PDF content")
    
    # Create subdirectories
    docs_dir = tmp_path / "documents"
    docs_dir.mkdir()
    (docs_dir / "paper1.pdf").write_bytes(b"Mock PDF 1")
    (docs_dir / "paper2.pdf").write_bytes(b"Mock PDF 2")
    
    return tmp_path

# Environment fixtures
@pytest.fixture
def clean_environment():
    """Ensure clean environment for testing."""
    import os
    # Store original env vars
    original_env = {}
    test_vars = [
        "OPENAI_API_KEY", "DEEPSEEK_API_KEY", "ANTHROPIC_API_KEY",
        "RAGFLOW_HOST", "RAGFLOW_PORT", "LOG_LEVEL"
    ]
    
    for var in test_vars:
        if var in os.environ:
            original_env[var] = os.environ[var]
            del os.environ[var]
    
    # Set test environment
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "WARNING"
    
    yield
    
    # Restore original environment
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]
        if var in original_env:
            os.environ[var] = original_env[var]
    
    if "TESTING" in os.environ:
        del os.environ["TESTING"]

# Async fixtures for testing
@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Database/Vector store mocks
@pytest.fixture
def mock_vector_operations():
    """Mock vector database operations."""
    mock = Mock()
    mock.search.return_value = [
        {"id": "vec_1", "score": 0.95, "metadata": {"source": "doc1.pdf"}},
        {"id": "vec_2", "score": 0.88, "metadata": {"source": "doc2.pdf"}}
    ]
    mock.add_vectors.return_value = True
    mock.delete_vectors.return_value = True
    mock.get_collection_info.return_value = {"vectors": 100, "dimensions": 512}
    return mock

# Performance testing fixtures
@pytest.fixture
def performance_monitor():
    """Monitor performance during tests."""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.measurements = []
        
        def start(self):
            self.start_time = time.time()
        
        def measure(self, operation_name):
            if self.start_time:
                duration = time.time() - self.start_time
                self.measurements.append((operation_name, duration))
                self.start_time = time.time()
        
        def get_results(self):
            return self.measurements
    
    return PerformanceMonitor()

# Error simulation fixtures
@pytest.fixture
def error_scenarios():
    """Provide common error scenarios for testing."""
    return {
        "network_error": Exception("Network connection failed"),
        "auth_error": Exception("Authentication failed"),
        "config_error": Exception("Invalid configuration"),
        "docker_error": Exception("Docker service unavailable"),
        "llm_error": Exception("LLM API rate limit exceeded"),
        "parsing_error": Exception("Document parsing failed")
    }

# Configuration for mathematical content testing
@pytest.fixture
def mathematical_test_cases():
    """Comprehensive mathematical content test cases."""
    return [
        {
            "name": "basic_equations",
            "latex": r"$x^2 + y^2 = z^2$",
            "expected_unicode": "x² + y² = z²"
        },
        {
            "name": "fractions", 
            "latex": r"$\frac{a}{b} = \frac{c}{d}$",
            "expected_unicode": "a/b = c/d"
        },
        {
            "name": "greek_letters",
            "latex": r"$\alpha + \beta = \gamma$", 
            "expected_unicode": "α + β = γ"
        },
        {
            "name": "integrals",
            "latex": r"$\int_{0}^{1} x dx = \frac{1}{2}$",
            "expected_unicode": "∫₀¹ x dx = 1/2"
        },
        {
            "name": "summations",
            "latex": r"$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$", 
            "expected_unicode": "∑ᵢ₌₁ⁿ i = n(n+1)/2"
        }
    ] 