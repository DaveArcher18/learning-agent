"""
BGE-M3 model configuration optimized for M1 MacBook Air.

This module provides configuration and optimization settings for the BGE-M3 
embedding model, specifically tuned for mathematical content processing
and CPU-only inference on Apple Silicon.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path


@dataclass
class BGE_M3ModelConfig:
    """
    BGE-M3 model configuration optimized for M1 MacBook Air (16GB RAM).
    
    This configuration enables multi-vector retrieval with dense embeddings,
    sparse retrieval, and ColBERT reranking, all optimized for mathematical
    content processing with CPU-only inference.
    """
    
    # Core model settings
    model_name: str = "BAAI/bge-m3"
    model_revision: str = "main"
    device: str = "cpu"  # M1 optimized - CPU only
    trust_remote_code: bool = True
    
    # Token and sequence settings for mathematical content
    max_length: int = 8192  # Extended for complete mathematical proofs
    normalize_embeddings: bool = True
    pooling_method: str = "cls"  # CLS token pooling
    
    # Multi-vector retrieval configuration
    enable_dense: bool = True
    enable_sparse: bool = True  
    enable_colbert: bool = True
    
    # Dense embedding settings
    dense_dim: int = 512  # Reduced from 1024 for memory efficiency
    dense_weight: float = 1.0
    
    # Sparse embedding settings (SPLADE-style)
    sparse_weight: float = 0.3
    sparse_top_k: int = 32  # Top tokens for sparse representation
    
    # ColBERT settings for fine-grained matching
    colbert_dim: int = 128  # Compressed ColBERT dimensions
    colbert_weight: float = 1.0
    colbert_similarity: str = "cosine"
    
    # Performance optimization for M1
    batch_size: int = 4  # Optimized for 16GB RAM
    num_threads: int = 8  # M1 efficiency cores
    enable_half_precision: bool = False  # Keep FP32 for stability
    enable_torch_compile: bool = False  # Disable for compatibility
    
    # Caching settings for small datasets (<10K pages)
    cache_embeddings: bool = True
    cache_dir: str = "./cache/bge_m3"
    cache_max_size: int = 2000  # Max cached embeddings
    
    # Mathematical content specific settings
    mathematical_notation_support: bool = True
    latex_preservation: bool = True
    theorem_aware_chunking: bool = True
    proof_chain_recognition: bool = True
    
    # Quality-first processing settings
    exhaustive_search: bool = True  # For small datasets
    enable_batch_processing: bool = True
    prefetch_embeddings: bool = True
    
    # Memory management
    memory_limit_gb: float = 6.0  # Conservative limit for M1
    garbage_collection_threshold: int = 100  # Clean up after N operations
    
    def __post_init__(self):
        """Validate and setup configuration after initialization."""
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Validate device compatibility
        if self.device == "mps":
            # MPS might have issues with some operations
            print("⚠️ MPS device detected. Falling back to CPU for stability.")
            self.device = "cpu"
        
        # Adjust batch size based on available memory
        if self.memory_limit_gb < 4.0:
            self.batch_size = max(1, self.batch_size // 2)
            print(f"📉 Reduced batch size to {self.batch_size} due to memory constraints")
    
    def get_model_kwargs(self) -> Dict[str, Any]:
        """
        Get model initialization kwargs for BGE-M3.
        
        Returns:
            Dict containing model initialization parameters
        """
        return {
            "model_name_or_path": self.model_name,
            "revision": self.model_revision,
            "trust_remote_code": self.trust_remote_code,
            "device": self.device,
            "normalize_embeddings": self.normalize_embeddings,
            "pooling_method": self.pooling_method,
        }
    
    def get_encoding_kwargs(self) -> Dict[str, Any]:
        """
        Get encoding kwargs for text processing.
        
        Returns:
            Dict containing encoding parameters
        """
        return {
            "max_length": self.max_length,
            "batch_size": self.batch_size,
            "normalize_embeddings": self.normalize_embeddings,
            "return_dense": self.enable_dense,
            "return_sparse": self.enable_sparse,
            "return_colbert_vecs": self.enable_colbert,
        }
    
    def get_retrieval_weights(self) -> Dict[str, float]:
        """
        Get weights for multi-vector retrieval combination.
        
        Returns:
            Dict containing retrieval weights
        """
        return {
            "dense": self.dense_weight,
            "sparse": self.sparse_weight,
            "colbert": self.colbert_weight,
        }
    
    def get_mathematical_settings(self) -> Dict[str, Any]:
        """
        Get mathematical content processing settings.
        
        Returns:
            Dict containing mathematical processing parameters
        """
        return {
            "mathematical_notation_support": self.mathematical_notation_support,
            "latex_preservation": self.latex_preservation,
            "theorem_aware_chunking": self.theorem_aware_chunking,
            "proof_chain_recognition": self.proof_chain_recognition,
            "exhaustive_search": self.exhaustive_search,
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """
        Get performance optimization settings.
        
        Returns:
            Dict containing performance parameters
        """
        return {
            "batch_size": self.batch_size,
            "num_threads": self.num_threads,
            "enable_half_precision": self.enable_half_precision,
            "cache_embeddings": self.cache_embeddings,
            "cache_dir": self.cache_dir,
            "memory_limit_gb": self.memory_limit_gb,
        }
    
    def estimate_memory_usage(self, num_documents: int) -> Dict[str, float]:
        """
        Estimate memory usage for given number of documents.
        
        Args:
            num_documents: Number of documents to process
            
        Returns:
            Dict containing memory usage estimates in GB
        """
        # Base model memory (BGE-M3 is ~560M parameters)
        model_memory = 2.5  # GB for FP32
        
        # Embedding memory per document (approximate)
        dense_mem_per_doc = (self.dense_dim * 4) / (1024**3)  # 4 bytes per float32
        sparse_mem_per_doc = (self.sparse_top_k * 8) / (1024**3)  # Sparse representation
        colbert_mem_per_doc = (self.max_length * self.colbert_dim * 4) / (1024**3)
        
        embedding_memory = num_documents * (
            dense_mem_per_doc + sparse_mem_per_doc + colbert_mem_per_doc
        )
        
        # Cache memory
        cache_memory = min(self.cache_max_size * embedding_memory / num_documents, 1.0)
        
        # Total estimated memory
        total_memory = model_memory + embedding_memory + cache_memory
        
        return {
            "model_memory": model_memory,
            "embedding_memory": embedding_memory,
            "cache_memory": cache_memory,
            "total_memory": total_memory,
            "fits_in_limit": total_memory <= self.memory_limit_gb,
        }
    
    def optimize_for_dataset_size(self, num_documents: int) -> None:
        """
        Optimize configuration based on dataset size.
        
        Args:
            num_documents: Number of documents in the dataset
        """
        memory_estimate = self.estimate_memory_usage(num_documents)
        
        if num_documents < 1000:
            # Very small dataset - maximize quality
            self.batch_size = min(8, self.batch_size)
            self.exhaustive_search = True
            self.cache_embeddings = True
            print(f"🎯 Optimized for small dataset ({num_documents} docs): quality-first")
            
        elif num_documents < 5000:
            # Small dataset - balance quality and performance
            self.batch_size = min(6, self.batch_size)
            self.cache_embeddings = True
            print(f"⚖️ Optimized for medium dataset ({num_documents} docs): balanced")
            
        elif num_documents < 10000:
            # Target dataset size - standard optimization
            self.batch_size = 4
            self.cache_embeddings = True
            print(f"🎯 Optimized for target dataset ({num_documents} docs): standard")
            
        else:
            # Large dataset - prioritize performance
            self.batch_size = max(2, self.batch_size // 2)
            self.cache_embeddings = False
            self.exhaustive_search = False
            print(f"🚀 Optimized for large dataset ({num_documents} docs): performance-first")
        
        # Check if configuration fits in memory
        updated_estimate = self.estimate_memory_usage(num_documents)
        if not updated_estimate["fits_in_limit"]:
            print(f"⚠️ Memory usage ({updated_estimate['total_memory']:.1f}GB) exceeds limit ({self.memory_limit_gb}GB)")
            self.batch_size = max(1, self.batch_size // 2)
            print(f"📉 Reduced batch size to {self.batch_size}")


# Global configuration instance
default_bge_m3_config = BGE_M3ModelConfig()


def get_optimized_config(num_documents: Optional[int] = None) -> BGE_M3ModelConfig:
    """
    Get BGE-M3 configuration optimized for the dataset size.
    
    Args:
        num_documents: Number of documents (for optimization)
        
    Returns:
        Optimized BGE_M3ModelConfig instance
    """
    config = BGE_M3ModelConfig()
    
    if num_documents is not None:
        config.optimize_for_dataset_size(num_documents)
    
    return config


def validate_m1_compatibility() -> bool:
    """
    Validate M1 MacBook compatibility and optimize settings.
    
    Returns:
        bool: True if configuration is compatible
    """
    import platform
    import psutil
    
    # Check if running on Apple Silicon
    is_m1 = platform.machine() == "arm64" and platform.system() == "Darwin"
    
    if is_m1:
        print("✅ M1 MacBook detected - CPU optimization enabled")
        
        # Check available memory
        available_memory = psutil.virtual_memory().available / (1024**3)
        print(f"💾 Available memory: {available_memory:.1f}GB")
        
        if available_memory < 8.0:
            print("⚠️ Low memory detected - consider closing other applications")
            return False
            
        return True
    else:
        print("ℹ️ Non-M1 system detected - standard CPU configuration")
        return True


if __name__ == "__main__":
    """Test BGE-M3 configuration and optimization."""
    print("🧪 Testing BGE-M3 Configuration...")
    
    # Test 1: Basic configuration
    print("\n📋 Basic Configuration:")
    config = BGE_M3ModelConfig()
    print(f"Model: {config.model_name}")
    print(f"Device: {config.device}")
    print(f"Max length: {config.max_length}")
    print(f"Batch size: {config.batch_size}")
    
    # Test 2: Memory estimation
    print("\n💾 Memory Estimation:")
    test_sizes = [100, 1000, 5000, 10000]
    for size in test_sizes:
        estimate = config.estimate_memory_usage(size)
        print(f"{size:5d} docs: {estimate['total_memory']:.1f}GB (fits: {estimate['fits_in_limit']})")
    
    # Test 3: Optimization for different dataset sizes
    print("\n🎯 Dataset Size Optimization:")
    for size in test_sizes:
        test_config = get_optimized_config(size)
        print(f"{size:5d} docs: batch_size={test_config.batch_size}, cache={test_config.cache_embeddings}")
    
    # Test 4: M1 compatibility
    print("\n🍎 M1 Compatibility Check:")
    is_compatible = validate_m1_compatibility()
    print(f"Compatible: {is_compatible}")
    
    print("\n✅ BGE-M3 Configuration Test Complete") 