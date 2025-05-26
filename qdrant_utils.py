"""
qdrant_utils.py
---------------
Utility functions for connecting to Qdrant.
"""

from qdrant_client import QdrantClient
from rich import print as rprint

def connect_to_qdrant() -> QdrantClient:
    """
    Connects to a Qdrant instance with robust fallback mechanisms.

    Tries to connect to a Qdrant instance running in Docker (host="localhost", port=6333).
    If the Docker connection fails, it falls back to attempting a connection with an
    embedded Qdrant instance (path="./qdrant_data").

    Prints messages to the console indicating whether it connected to Docker Qdrant,
    embedded Qdrant, or if both attempts failed.

    Returns:
        QdrantClient: The QdrantClient object if a connection is successful.

    Raises:
        RuntimeError: If connection attempts to both Docker and embedded Qdrant instances fail.
    """
    # Attempt to connect to Qdrant running in Docker
    try:
        client = QdrantClient(host="localhost", port=6333)
        client.get_collections()  # Validate connection by trying a simple operation
        rprint("[green]✅ Successfully connected to Qdrant in Docker (localhost:6333).[/green]")
        return client
    except Exception as e_docker:
        rprint(f"[yellow]⚠️ Failed to connect to Qdrant in Docker: {e_docker}[/yellow]")
        rprint("[cyan]🔄 Attempting to connect to embedded Qdrant (path: ./qdrant_data)...[/cyan]")
        
        # Fallback to embedded Qdrant instance
        try:
            client = QdrantClient(path="./qdrant_data")
            client.get_collections()  # Validate connection
            rprint("[green]✅ Successfully connected to embedded Qdrant.[/green]")
            return client
        except Exception as e_embedded:
            rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e_embedded}[/red]")
            # Raise a comprehensive error if both attempts fail
            raise RuntimeError(
                "Failed to connect to Qdrant. Both Docker (localhost:6333) "
                "and embedded (./qdrant_data) connection attempts failed."
            )

if __name__ == '__main__':
    # This block provides an example of how to use the connect_to_qdrant function
    # and allows for direct testing of the connection utility.
    rprint("[bold cyan]🧪 Running Qdrant connection test...[/bold cyan]")
    try:
        qdrant_client_instance = connect_to_qdrant()
        rprint(f"\n[green]👍 Connection successful![/green]")
        rprint(f"Qdrant client object: {qdrant_client_instance}")
        
        # Example operation: List collections
        rprint("\n[cyan]Attempting to list collections...[/cyan]")
        try:
            collections_info = qdrant_client_instance.get_collections()
            rprint(f"[green]Collections found:[/green] {collections_info.collections}")
        except Exception as e_op:
            rprint(f"[red]❌ Error during example operation (get_collections): {e_op}[/red]")
            
    except RuntimeError as e_main:
        rprint(f"\n[red]❌ Connection test failed: {e_main}[/red]")
    except Exception as e_unexpected:
        rprint(f"\n[red]❌ An unexpected error occurred during the test: {e_unexpected}[/red]")
