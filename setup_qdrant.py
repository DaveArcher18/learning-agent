#!/usr/bin/env python
"""
setup_qdrant.py
--------------
Initialize Qdrant collection for LearningAgent.

This script:
1. Connects to local Qdrant (embedded or Docker)
2. Creates a collection named 'kb' if it doesn't exist
"""

import os
from qdrant_client import QdrantClient, models
from rich import print as rprint

# Default collection name and embedding dimension
COLLECTION = "kb"
VECTOR_SIZE = 384  # BGE-Small-EN dimension


def connect_to_qdrant():
    """Try to connect to Qdrant, first embedded then Docker."""
    # Try embedded Qdrant first
    try:
        client = QdrantClient(path="./qdrant_data")
        # Quick test to make sure it works
        client.get_collections()
        rprint("[green]✅ Connected to embedded Qdrant[/green]")
        return client
    except Exception as e:
        rprint(f"[yellow]⚠️ Could not connect to embedded Qdrant: {e}[/yellow]")
        rprint("[cyan]🔄 Trying Docker Qdrant connection...[/cyan]")

        # Try Docker connection
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Simple health check
            client.get_collections()
            rprint("[green]✅ Connected to Docker Qdrant[/green]")
            return client
        except Exception as docker_e:
            rprint(f"[red]❌ Failed to connect to Docker Qdrant: {docker_e}[/red]")
            rprint("[yellow]💡 Tips:[/yellow]")
            rprint(
                "[yellow]  - Run 'make start_qdrant' to start Qdrant Docker[/yellow]"
            )
            rprint(
                "[yellow]  - Or make sure ./qdrant_data directory exists and is writable[/yellow]"
            )
            raise RuntimeError("Could not connect to any Qdrant instance")


def ensure_collection(client, collection_name=COLLECTION, vector_size=VECTOR_SIZE):
    """Create collection if it doesn't exist."""
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if collection_name in collection_names:
        rprint(f"[green]✅ Collection '{collection_name}' already exists.[/green]")
        # Verify vector size matches
        collection_info = client.get_collection(collection_name)
        if 'vector_size' in collection_info.config.params:
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


def main():
    """Main function."""
    rprint("[cyan]🔌 Connecting to Qdrant...[/cyan]")
    client = connect_to_qdrant()
    ensure_collection(client)


if __name__ == "__main__":
    main()