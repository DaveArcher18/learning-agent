#!/usr/bin/env python
"""
setup_qdrant.py
--------------
Initialize Qdrant collection for LearningAgent.

This script:
1. Connects to Qdrant (Docker first, then embedded as fallback)
2. Creates a collection if it doesn't exist
"""

import os
import sys
# import yaml # No longer used directly
# QdrantClient is now imported in qdrant_utils
# from qdrant_client import QdrantClient
from qdrant_client import models # Keep this for models
from rich import print as rprint
from qdrant_utils import connect_to_qdrant as connect_to_qdrant_util # Import the new utility
from config_utils import ConfigManager # Import the new ConfigManager

# Initialize ConfigManager
config_manager = ConfigManager()

# Global configuration values for this script
COLLECTION_NAME: str = config_manager.get("collection", "kb") # Renamed for clarity
# VECTOR_SIZE is hardcoded as it's specific to the assumed embedding model for initial setup.
# If this needs to be dynamic based on config for setup, it should be fetched from config_manager.
VECTOR_SIZE: int = 384  # BGE-Small-EN dimension (default for many common models)

def connect_to_qdrant() -> 'QdrantClient': # Added return type hint
    """
    Connects to Qdrant by calling the centralized utility function.
    The utility handles connection attempts (Docker, embedded) and error reporting.
    
    Returns:
        'QdrantClient': An initialized Qdrant client instance.
    """
    # connect_to_qdrant_util is imported from qdrant_utils
    return connect_to_qdrant_util()


def ensure_collection(client: 'QdrantClient', collection_name: str = COLLECTION_NAME, vector_size: int = VECTOR_SIZE) -> None:
    """
    Ensures that the specified Qdrant collection exists. If not, it creates it
    with the given vector size and COSINE distance metric.
    It also verifies if an existing collection has the correct vector size.

    Args:
        client ('QdrantClient'): The Qdrant client instance.
        collection_name (str): The name of the collection. Defaults to COLLECTION_NAME.
        vector_size (int): The dimension of vectors to be stored. Defaults to VECTOR_SIZE.
        
    Raises:
        Exception: If it fails to create the collection after an attempt.
    """
    try:
        collections = client.get_collections().collections # type: ignore
        collection_names = [c.name for c in collections] # type: ignore
        
        if collection_name in collection_names:
            rprint(f"[green]✅ Collection '{collection_name}' already exists.[/green]")
            collection_info = client.get_collection(collection_name=collection_name) # type: ignore
            
            # Verify vector size if params and vectors attribute exist
            current_vector_size = None
            if hasattr(collection_info.config, 'params') and \
               hasattr(collection_info.config.params, 'vectors') and \
               hasattr(collection_info.config.params.vectors, 'size'):
                current_vector_size = collection_info.config.params.vectors.size
            
            if current_vector_size and current_vector_size != vector_size:
                rprint(f"[yellow]⚠️ Collection '{collection_name}' exists with vector size {current_vector_size}, "
                       f"but expected {vector_size}. Consider rebuilding if this is incorrect.[/yellow]")
            return
        
        # If collection does not exist, create it
        rprint(f"[cyan]ℹ️ Collection '{collection_name}' does not exist. Creating...[/cyan]")
        client.create_collection( # type: ignore
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE) # type: ignore
        )
        rprint(f"[green]✅ Created collection '{collection_name}' with vector size {vector_size}.[/green]")
    except Exception as e:
        rprint(f"[red]❌ Failed to ensure collection '{collection_name}' exists: {e}[/red]")
        raise # Re-raise the exception to be caught by the main error handler


def check_collection_status(client: 'QdrantClient', collection_name: str = COLLECTION_NAME) -> Optional[int]:
    """
    Checks and prints the status of the specified Qdrant collection,
    including the number of vectors it contains.

    Args:
        client ('QdrantClient'): The Qdrant client instance.
        collection_name (str): The name of the collection. Defaults to COLLECTION_NAME.

    Returns:
        Optional[int]: The number of vectors in the collection, or None if status check fails.
    """
    try:
        collection_info = client.get_collection(collection_name=collection_name) # type: ignore
        vector_count = collection_info.points_count # type: ignore
        rprint(f"[green]📊 Collection '{collection_name}' status: {collection_info.status}, "
               f"contains {vector_count} vectors.[/green]")
        return vector_count
    except Exception as e:
        rprint(f"[red]❌ Failed to get status for collection '{collection_name}': {e}[/red]")
        return None


def main() -> None:
    """
    Main function to set up the Qdrant environment.
    Connects to Qdrant, ensures the specified collection exists,
    and checks its status. Exits with code 1 on failure.
    """
    rprint(f"[bold cyan]🚀 Initializing Qdrant Setup for collection: '{COLLECTION_NAME}'...[/bold cyan]")
    
    try:
        qdrant_client = connect_to_qdrant()
        
        ensure_collection(client=qdrant_client, collection_name=COLLECTION_NAME, vector_size=VECTOR_SIZE)
        
        vector_count = check_collection_status(client=qdrant_client, collection_name=COLLECTION_NAME)
        
        if vector_count is not None:
            rprint(f"[green bold]✅ Qdrant setup successful for collection '{COLLECTION_NAME}'.[/green bold]")
        else:
            rprint(f"[yellow]⚠️ Qdrant setup completed for collection '{COLLECTION_NAME}', but status check failed or collection is empty.[/yellow]")
            
    except RuntimeError as e: # Catch connection errors specifically
        rprint(f"[red bold]❌ Qdrant connection failed: {e}[/red bold]")
        sys.exit(1)
    except Exception as e: # Catch other errors during setup (e.g., collection creation)
        rprint(f"[red bold]❌ Qdrant setup failed: {e}[/red bold]")
        import traceback
        rprint(traceback.format_exc()) # Print full traceback for unexpected errors
        sys.exit(1)


if __name__ == "__main__":
    main()