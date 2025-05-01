#!/usr/bin/env python
"""
setup_qdrant.py
--------------
Simple utility to create the 'kb' collection in Qdrant if it doesn't exist yet.
Used by the Makefile to ensure the database is ready for use.
"""

import os
import time
import numpy as np
from qdrant_client import QdrantClient, models as qmodels

# Constants
COLLECTION = "kb"
EMBEDDING_SIZE = 384  # bge-small-en has 384 dimensions


def main():
    """Initialize the Qdrant collection if it doesn't exist."""
    # Try connecting to embedded Qdrant first
    print("🔌 Connecting to Qdrant...")
    
    # First try local embedded mode
    try:
        client = QdrantClient(path="./qdrant_data")
        print("✅ Connected to embedded Qdrant")
    except Exception as e:
        print(f"⚠️ Could not connect to embedded Qdrant: {e}")
        
        # Try Docker connection
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Simple health check
            client.get_collections()
            print("✅ Connected to Docker Qdrant")
        except Exception as docker_e:
            print(f"❌ Failed to connect to Docker Qdrant: {docker_e}")
            print("💡 Tips:")
            print("  - Run 'make start_qdrant' to start Qdrant Docker")
            print("  - Or make sure ./qdrant_data directory exists and is writable")
            return
    
    # Check if collection exists
    try:
        existing = [c.name for c in client.get_collections().collections]
        if COLLECTION in existing:
            print(f"✅ Collection '{COLLECTION}' already exists.")
            return
    except Exception as e:
        print(f"❌ Error checking collections: {e}")
        return
    
    # Create collection
    try:
        print(f"🏗️  Creating collection '{COLLECTION}'...")
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=qmodels.VectorParams(
                size=EMBEDDING_SIZE, 
                distance=qmodels.Distance.COSINE
            ),
        )
        print(f"✅ Collection '{COLLECTION}' created successfully.")
    except Exception as e:
        print(f"❌ Error creating collection: {e}")


if __name__ == "__main__":
    main()