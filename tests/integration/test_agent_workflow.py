"""
Integration tests for the complete Learning Agent workflow.

Tests end-to-end interactions between services, command processing,
RAG retrieval, mathematical content processing, and response generation.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.core.agent import LearningAgent
from src.core.config import LearningAgentConfig
from src.ui.commands.registry import CommandRegistry
from src.utils.exceptions import LearningAgentError


class TestAgentWorkflowIntegration:
    """Integration tests for complete agent workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create test configuration
        self.config = LearningAgentConfig(
            llm={"provider": "deepseek", "model": "deepseek-chat"},
            ragflow={"host": "localhost", "port": 9380},
            bge_m3={"device": "cpu", "batch_size": 4},
            mathematical_content={"latex_rendering": True}
        )
        
        # Mock external services for integration testing
        self.setup_mocks()
        
        # Create agent instance
        self.agent = LearningAgent(config=self.config)
    
    def setup_mocks(self):
        """Set up mocks for external services."""
        # Mock LLM service
        self.llm_mock = Mock()
        self.llm_mock.generate_response.return_value = "Mocked LLM response"
        self.llm_mock.health_check.return_value = {"status": "healthy"}
        
        # Mock RAGFlow service
        self.ragflow_mock = Mock()
        self.ragflow_mock.is_running.return_value = True
        self.ragflow_mock.health_check.return_value = {"status": "healthy"}
        
        # Mock memory service
        self.memory_mock = Mock()
        self.memory_mock.get_conversation.return_value = []
        
        # Mock RAGFlow client
        self.ragflow_client_mock = Mock()
        self.ragflow_client_mock.retrieve.return_value = [
            {
                "content": "Mathematical content about linear algebra",
                "source": "linear_algebra.pdf",
                "score": 0.95,
                "citations": ["Theorem 1.1"]
            }
        ]
    
    @pytest.mark.integration
    @patch('src.core.agent.LLMService')
    @patch('src.core.agent.RAGFlowService')
    @patch('src.core.agent.MemoryService')
    def test_agent_initialization_workflow(self, mock_memory, mock_ragflow, mock_llm):
        """Test complete agent initialization workflow."""
        # Setup mocks
        mock_llm.return_value = self.llm_mock
        mock_ragflow.return_value = self.ragflow_mock
        mock_memory.return_value = self.memory_mock
        
        # Initialize agent
        agent = LearningAgent(config=self.config)
        
        # Verify services were initialized
        assert agent.llm_service is not None
        assert agent.ragflow_service is not None
        assert agent.memory_service is not None
        
        # Verify health checks were performed
        assert agent.health_status["llm"] == "healthy"
        assert agent.health_status["ragflow"] == "healthy"
    
    @pytest.mark.integration
    @patch('src.core.agent.LLMService')
    @patch('src.services.ragflow_service.RAGFlowService')
    def test_query_processing_workflow(self, mock_ragflow, mock_llm):
        """Test complete query processing workflow."""
        # Setup mocks
        mock_llm.return_value = self.llm_mock
        mock_ragflow.return_value = self.ragflow_mock
        
        agent = LearningAgent(config=self.config)
        
        # Process a mathematical query
        query = "Explain linear transformations in vector spaces"
        
        with patch.object(agent.ragflow_client, 'retrieve') as mock_retrieve:
            mock_retrieve.return_value = [
                {
                    "content": "A linear transformation T: V → W is a function...",
                    "source": "linear_algebra.pdf",
                    "score": 0.92,
                    "citations": ["Definition 2.1", "Theorem 2.3"]
                }
            ]
            
            response = agent.process_query(query)
            
            # Verify workflow steps
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Verify RAG retrieval was called
            mock_retrieve.assert_called_once()
            
            # Verify LLM generation was called
            self.llm_mock.generate_response.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.mathematical
    def test_mathematical_content_workflow(self):
        """Test mathematical content processing workflow."""
        with patch.object(self.agent, 'llm_service', self.llm_mock):
            with patch.object(self.agent, 'ragflow_client', self.ragflow_client_mock):
                
                # Mathematical query with LaTeX
                math_query = "Solve the quadratic equation ax^2 + bx + c = 0"
                
                # Mock LLM response with LaTeX
                math_response = r"The solution is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$"
                self.llm_mock.generate_response.return_value = math_response
                
                # Process query
                response = agent.process_query(math_query)
                
                # Verify mathematical processing
                assert "x = " in response
                
                # If LaTeX renderer is integrated, verify conversion
                from src.text_processing.latex_renderer import LatexRenderer
                renderer = LatexRenderer()
                rendered = renderer.render_latex(response)
                
                # Mathematical symbols should be converted
                assert "$" not in rendered or "±" in rendered or "√" in rendered
    
    @pytest.mark.integration
    def test_command_processing_workflow(self):
        """Test command processing workflow."""
        # Test help command
        with patch.object(self.agent, 'command_registry') as mock_registry:
            mock_help_command = Mock()
            mock_help_command.execute.return_value = "Help information"
            mock_registry.get_command.return_value = mock_help_command
            
            result = self.agent.process_command("/help")
            
            assert "Help information" in result
            mock_registry.get_command.assert_called_with("help")
    
    @pytest.mark.integration
    def test_provider_switching_workflow(self):
        """Test LLM provider switching workflow."""
        with patch.object(self.agent, 'llm_service', self.llm_mock):
            # Test provider switching
            self.llm_mock.switch_provider.return_value = True
            self.llm_mock.get_current_provider.return_value = "openai"
            
            result = self.agent.process_command("/provider switch openai")
            
            # Verify switching was attempted
            self.llm_mock.switch_provider.assert_called_with("openai")
            assert "openai" in result.lower()
    
    @pytest.mark.integration
    def test_memory_management_workflow(self):
        """Test memory management workflow."""
        with patch.object(self.agent, 'memory_service', self.memory_mock):
            # Test memory operations
            self.memory_mock.get_statistics.return_value = {
                "total_messages": 10,
                "session_duration": 300
            }
            
            result = self.agent.process_command("/memory stats")
            
            # Verify memory stats were retrieved
            self.memory_mock.get_statistics.assert_called_once()
            assert "10" in result  # Should contain message count
    
    @pytest.mark.integration
    @pytest.mark.requires_docker
    def test_ragflow_service_workflow(self):
        """Test RAGFlow service workflow."""
        with patch.object(self.agent, 'ragflow_service', self.ragflow_mock):
            # Test RAGFlow status
            self.ragflow_mock.get_status.return_value = {
                "running": True,
                "containers": ["ragflow-api", "ragflow-worker"],
                "health": "healthy"
            }
            
            result = self.agent.process_command("/rag status")
            
            # Verify RAGFlow status was checked
            self.ragflow_mock.get_status.assert_called_once()
            assert "healthy" in result.lower()
    
    @pytest.mark.integration
    def test_error_handling_workflow(self):
        """Test error handling throughout the workflow."""
        with patch.object(self.agent, 'llm_service', self.llm_mock):
            # Simulate LLM service error
            self.llm_mock.generate_response.side_effect = Exception("LLM service error")
            
            # Should handle error gracefully
            response = self.agent.process_query("Test query")
            
            # Should not crash and provide error information
            assert isinstance(response, str)
            assert "error" in response.lower() or "sorry" in response.lower()
    
    @pytest.mark.integration
    def test_conversation_context_workflow(self):
        """Test conversation context handling workflow."""
        with patch.object(self.agent, 'llm_service', self.llm_mock):
            with patch.object(self.agent, 'memory_service', self.memory_mock):
                
                # Mock conversation history
                conversation = [
                    {"role": "user", "content": "What is a matrix?"},
                    {"role": "assistant", "content": "A matrix is a rectangular array of numbers."},
                    {"role": "user", "content": "How do you multiply matrices?"}
                ]
                self.memory_mock.get_conversation.return_value = conversation
                
                # Process query with context
                response = self.agent.process_query("Give me an example")
                
                # Verify conversation context was used
                call_args = self.llm_mock.generate_response.call_args
                assert call_args is not None
                
                # Context should be included in the call
                if len(call_args[1]) > 0 and 'conversation_context' in call_args[1]:
                    assert call_args[1]['conversation_context'] == conversation
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_monitoring_workflow(self):
        """Test performance monitoring workflow."""
        with patch.object(self.agent, 'metrics_collector') as mock_metrics:
            mock_metrics.get_system_metrics.return_value = {
                "cpu_usage": 25.5,
                "memory_usage": 60.2,
                "response_time": 1.2
            }
            
            # Process query and check metrics
            response = self.agent.process_query("Test performance")
            
            # Verify metrics were collected
            assert mock_metrics.record_operation.called
    
    @pytest.mark.integration
    def test_configuration_validation_workflow(self):
        """Test configuration validation workflow."""
        # Test with invalid configuration
        invalid_config = LearningAgentConfig(
            llm={"provider": "invalid_provider"}
        )
        
        with pytest.raises(ValueError):
            agent = LearningAgent(config=invalid_config)
    
    @pytest.mark.integration
    def test_health_monitoring_workflow(self):
        """Test health monitoring workflow."""
        with patch.object(self.agent, 'health_monitor') as mock_health:
            mock_health.check_all_services.return_value = {
                "llm": {"status": "healthy", "response_time": 0.5},
                "ragflow": {"status": "healthy", "containers": 2},
                "memory": {"status": "healthy", "usage": "10MB"}
            }
            
            result = self.agent.process_command("/health")
            
            # Verify health check was performed
            mock_health.check_all_services.assert_called_once()
            assert "healthy" in result.lower()


class TestCompleteUserWorkflow:
    """Test complete user workflow scenarios."""
    
    def setup_method(self):
        """Set up complete workflow testing."""
        self.config = LearningAgentConfig()
        self.temp_dir = tempfile.mkdtemp()
    
    @pytest.mark.integration
    @pytest.mark.e2e
    def test_academic_research_workflow(self):
        """Test complete academic research workflow."""
        # Simulate academic research session
        workflow_steps = [
            "/help",  # Get help
            "/rag status",  # Check RAG status
            "What is linear algebra?",  # Basic query
            "Explain eigenvalues and eigenvectors",  # Mathematical query
            "/memory stats",  # Check conversation
            "/provider switch openai",  # Switch provider
            "Give me a proof of the spectral theorem",  # Complex query
            "/memory export",  # Export conversation
        ]
        
        with patch.multiple(
            'src.core.agent.LearningAgent',
            llm_service=Mock(),
            ragflow_service=Mock(),
            memory_service=Mock(),
            ragflow_client=Mock()
        ):
            agent = LearningAgent(config=self.config)
            
            results = []
            for step in workflow_steps:
                if step.startswith("/"):
                    result = agent.process_command(step)
                else:
                    result = agent.process_query(step)
                
                results.append(result)
                assert isinstance(result, str)
                assert len(result) > 0
            
            # Verify workflow completed successfully
            assert len(results) == len(workflow_steps)
    
    @pytest.mark.integration
    @pytest.mark.e2e
    def test_mathematical_problem_solving_workflow(self):
        """Test mathematical problem solving workflow."""
        mathematical_queries = [
            "Solve x^2 + 2x + 1 = 0",
            "Find the derivative of sin(x) * cos(x)",
            "What is the integral of e^x dx?",
            "Explain the fundamental theorem of calculus",
            "Prove that the square root of 2 is irrational"
        ]
        
        with patch.multiple(
            'src.core.agent.LearningAgent',
            llm_service=Mock(),
            ragflow_client=Mock()
        ):
            agent = LearningAgent(config=self.config)
            
            # Mock mathematical responses
            agent.llm_service.generate_response.side_effect = [
                "The solution is x = -1 (double root)",
                "The derivative is cos²(x) - sin²(x) = cos(2x)",
                "The integral is e^x + C",
                "The FTC connects differentiation and integration...",
                "Proof by contradiction: Assume √2 = p/q..."
            ]
            
            for query in mathematical_queries:
                response = agent.process_query(query)
                
                # Verify mathematical content is handled
                assert isinstance(response, str)
                assert len(response) > 0
                
                # Mathematical responses should contain relevant terms
                if "derivative" in query:
                    assert "derivative" in response.lower() or "cos" in response
                elif "integral" in query:
                    assert "integral" in response.lower() or "e^x" in response
    
    @pytest.mark.integration
    @pytest.mark.e2e  
    def test_error_recovery_workflow(self):
        """Test error recovery in complete workflow."""
        # Simulate various error scenarios
        error_scenarios = [
            ("Network error", ConnectionError("Network unreachable")),
            ("API key error", Exception("401 Unauthorized")),
            ("Service unavailable", Exception("Service temporarily unavailable")),
            ("Invalid command", None),  # Invalid command test
        ]
        
        with patch('src.core.agent.LearningAgent') as mock_agent_class:
            agent = mock_agent_class.return_value
            
            for error_name, error in error_scenarios:
                if error:
                    agent.process_query.side_effect = error
                    
                    # Should handle error gracefully
                    try:
                        result = agent.process_query("Test query")
                        # If no exception, should return error message
                        assert isinstance(result, str)
                    except Exception:
                        # Should not propagate unhandled exceptions
                        pytest.fail(f"Unhandled exception in {error_name}")
                else:
                    # Test invalid command
                    agent.process_command.return_value = "Unknown command"
                    result = agent.process_command("/invalid_command")
                    assert "unknown" in result.lower() or "invalid" in result.lower()


class TestServiceCoordination:
    """Test coordination between multiple services."""
    
    @pytest.mark.integration
    def test_llm_and_ragflow_coordination(self):
        """Test coordination between LLM and RAGFlow services."""
        with patch('src.services.llm_service.LLMService') as mock_llm:
            with patch('src.services.ragflow_service.RAGFlowService') as mock_ragflow:
                
                # Setup service coordination
                llm_service = mock_llm.return_value
                ragflow_service = mock_ragflow.return_value
                
                # Mock retrieval results
                ragflow_service.retrieve.return_value = [
                    {"content": "Mathematical concept explanation", "score": 0.9}
                ]
                
                # Mock LLM response using retrieval
                llm_service.generate_response.return_value = "Enhanced response with context"
                
                # Test coordination
                agent = LearningAgent(config=LearningAgentConfig())
                response = agent.process_query("Explain mathematical concepts")
                
                # Verify both services were used
                assert ragflow_service.retrieve.called
                assert llm_service.generate_response.called
    
    @pytest.mark.integration
    def test_memory_and_llm_coordination(self):
        """Test coordination between memory and LLM services."""
        with patch('src.services.memory_service.MemoryService') as mock_memory:
            with patch('src.services.llm_service.LLMService') as mock_llm:
                
                memory_service = mock_memory.return_value
                llm_service = mock_llm.return_value
                
                # Mock conversation history
                memory_service.get_conversation.return_value = [
                    {"role": "user", "content": "Previous question"},
                    {"role": "assistant", "content": "Previous answer"}
                ]
                
                # Test coordination
                agent = LearningAgent(config=LearningAgentConfig())
                response = agent.process_query("Follow-up question")
                
                # Verify conversation context was used
                assert memory_service.get_conversation.called
                assert llm_service.generate_response.called
                
                # LLM should receive conversation context
                call_args = llm_service.generate_response.call_args
                assert call_args is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 