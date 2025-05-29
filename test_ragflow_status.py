#!/usr/bin/env python3
"""
Quick test script to check RAGFlow status and knowledge base information.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.config import ConfigManager
from services.ragflow_service import RAGFlowService

def main():
    try:
        config = ConfigManager()
        ragflow = RAGFlowService(config)
        
        print("=== RAGFlow Status Check ===")
        print(f"Service Available: {ragflow.is_available()}")
        print(f"Service Status: {ragflow.get_service_status()}")
        
        print("\n=== Knowledge Bases ===")
        kbs = ragflow.get_knowledge_bases()
        if kbs:
            for kb in kbs:
                print(f"Name: {kb.name}")
                print(f"ID: {kb.id}")
                print(f"Documents: {kb.document_count}")
                print(f"Chunks: {kb.chunk_count}")
                print(f"Embedding Model: {kb.embedding_model}")
                print("-" * 40)
        else:
            print("No knowledge bases found or error retrieving them")
        
        print("\n=== Test Query ===")
        try:
            result = ragflow.retrieve_and_answer(
                "What is the main architecture of this system?",
                []
            )
            print(f"Query Result: {result[:200]}...")
        except Exception as e:
            print(f"Query failed: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 