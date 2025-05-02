#!/usr/bin/env python
"""
setup_qdrant.py
--------------
Initialize Qdrant collection for LearningAgent.

This script:
1. Connects to Qdrant (Docker first, then embedded as fallback)
2. Creates a collection named 'kb' if it doesn't exist
"""

import os
import sys
from qdrant_client import QdrantClient, models
from rich import print as rprint

# Default collection name and embedding dimension
COLLECTION = "kb"
VECTOR_SIZE = 384  # BGE-Small-EN dimension

def connect_to_qdrant():
    """Connect to Qdrant, prioritizing Docker over embedded."""
    # Try Docker connection first (preferred for reliability)
    try:
        client = QdrantClient(host="localhost", port=6333)
        # Quick test to make sure it works
        client.get_collections()
        rprint("[green]✅ Connected to Docker Qdrant[/green]")
        return client, "docker"
    except Exception as docker_e:
        rprint(f"[yellow]⚠️ Could not connect to Docker Qdrant: {docker_e}[/yellow]")
        rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant in Docker[/yellow]")
        
        # Try embedded Qdrant as fallback
        try:
            rprint("[cyan]🔄 Trying embedded Qdrant as fallback...[/cyan]")
            client = QdrantClient(path="./qdrant_data")
            # Quick test to make sure it works
            client.get_collections()
            rprint("[green]✅ Connected to embedded Qdrant[/green]")
            return client, "embedded"
        except Exception as e:
            rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e}[/red]")
            rprint("[yellow]💡 Tips:[/yellow]")
            rprint("[yellow]  - Run 'make start_qdrant' to start Qdrant Docker[/yellow]")
            rprint("[yellow]  - Or make sure ./qdrant_data directory exists and is writable[/yellow]")
            raise RuntimeError("Could not connect to any Qdrant instance")


def ensure_collection(client, collection_name=COLLECTION, vector_size=VECTOR_SIZE):
    """Create collection if it doesn't exist."""
    try:
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if collection_name in collection_names:
            rprint(f"[green]✅ Collection '{collection_name}' already exists.[/green]")
            # Verify vector size matches
            collection_info = client.get_collection(collection_name)
            if hasattr(collection_info.config.params, 'vector_size'):
                actual_size = collection_info.config.params.vector_size
                if actual_size != vector_size:
                    rprint(f"[yellow]⚠️ Collection has vector size {actual_size}, but expected {vector_size}.[/yellow]")
            return
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            ),
        )
        rprint(f"[green]✅ Created collection '{collection_name}'.[/green]")
    except Exception as e:
        rprint(f"[red]❌ Failed to ensure collection exists: {e}[/red]")
        raise


def check_collection_status(client, collection_name=COLLECTION):
    """Check and print the status of the collection"""
    try:
        collection_info = client.get_collection(collection_name)
        vector_count = collection_info.points_count
        rprint(f"[green]📊 Collection '{collection_name}' contains {vector_count} vectors.[/green]")
        return vector_count
    except Exception as e:
        rprint(f"[red]❌ Failed to get collection status: {e}[/red]")
        return 0


def main():
    """Main function."""
    rprint("[cyan]🔌 Connecting to Qdrant...[/cyan]")
    try:
        client, mode = connect_to_qdrant()
        ensure_collection(client)
        vector_count = check_collection_status(client)
        rprint(f"[green]✅ Qdrant setup complete (mode: {mode}, vectors: {vector_count}).[/green]")
    except Exception as e:
        rprint(f"[red]❌ Setup failed: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()