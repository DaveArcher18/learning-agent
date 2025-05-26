#!/usr/bin/env python
"""
audit_qdrant.py
--------------
Audit and search the Qdrant database for LearningAgent.
Displays stats, sample data, and provides search capabilities.
"""

# import os # No longer used
# import yaml # No longer used directly
import argparse
import json
# from datetime import datetime # No longer used
# from pathlib import Path # No longer used
from typing import List, Dict, Any, Optional # Dict, Any might not be strictly needed now

# QdrantClient is now imported in qdrant_utils
# from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels # Keep this for qmodels
from rich import print as rprint
from qdrant_utils import connect_to_qdrant # Import the new utility
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress
from config_utils import ConfigManager # Import the new ConfigManager

# Initialize ConfigManager
config_manager = ConfigManager()

# Global configuration values for this script
COLLECTION_NAME: str = config_manager.get("collection", "kb") # Renamed for clarity
SEARCH_LIMIT: int = config_manager.get("db_search_limit", 20)

class QdrantAuditor:
    """
    Provides methods to audit and search a Qdrant vector database collection.
    Handles connection, fetching collection statistics, sampling points,
    text/metadata search, and exporting results.
    """
    
    def __init__(self) -> None:
        self.client: 'QdrantClient' = self._connect_to_qdrant()
        self.collection_name: str = COLLECTION_NAME # Use the global constant
        self.console = Console()
    
    def _connect_to_qdrant(self) -> 'QdrantClient':
        """
        Connects to Qdrant using the centralized `connect_to_qdrant` utility.
        
        Returns:
            'QdrantClient': An initialized Qdrant client instance.
        """
        return connect_to_qdrant()
    
    def get_collection_info(self) -> Optional[Any]: # Qdrant's CollectionInfo model is complex
        """
        Retrieves information/details for the configured Qdrant collection.

        Returns:
            Optional[Any]: The collection information object if found, otherwise None.
        """
        if not self.client:
            rprint("[red]❌ Qdrant client not initialized in QdrantAuditor.[/red]")
            return None
        try:
            collections_response = self.client.get_collections() # type: ignore
            # Check if collections_response itself and its collections attribute are not None
            if collections_response and collections_response.collections:
                 # Check if the collection name exists in the list of collections
                if any(c.name == self.collection_name for c in collections_response.collections):
                    return self.client.get_collection(self.collection_name) # type: ignore
                else:
                    rprint(f"[yellow]⚠️ Collection '{self.collection_name}' not found in the database.[/yellow]")
                    return None
            else: # Should not happen if client is connected, but good for robustness
                rprint(f"[yellow]⚠️ No collections found or unable to retrieve collection list.[/yellow]")
                return None

        except Exception as e:
            rprint(f"[red]❌ Error retrieving collection info for '{self.collection_name}': {e}[/red]")
            return None

    def get_collection_stats(self) -> Optional[Dict[str, Any]]:
        """
        Fetches and returns key statistics for the configured collection.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with statistics 
                                      (points_count, vectors_config, indexed_percent)
                                      or None if stats cannot be retrieved.
        """
        collection_info = self.get_collection_info()
        if not collection_info:
            return None # Message already printed by get_collection_info
        
        # Safely access attributes, especially for vector config
        vector_config = {}
        if hasattr(collection_info, 'config') and \
           hasattr(collection_info.config, 'params') and \
           hasattr(collection_info.config.params, 'vectors'):
            vector_params = collection_info.config.params.vectors
            vector_config['size'] = getattr(vector_params, 'size', 'N/A')
            vector_config['distance'] = str(getattr(vector_params, 'distance', 'N/A'))
        else: # Default if structure is not as expected
             vector_config['size'] = 'N/A'
             vector_config['distance'] = 'N/A'

        return {
            "points_count": getattr(collection_info, 'points_count', 0),
            "vectors_config": vector_config,
            "indexed_percent": getattr(collection_info, 'indexed_percent', 0.0) * 100 # Assuming it's a float 0-1
        }
    
    def get_sample_points(self, limit: int = 5, with_vectors: bool = False) -> List[Any]:
        """
        Retrieves a sample of points (documents) from the collection.

        Args:
            limit (int): The maximum number of points to retrieve.
            with_vectors (bool): Whether to include vectors in the results.

        Returns:
            List[Any]: A list of Qdrant point objects, or an empty list on error.
        """
        if not self.client:
            rprint("[red]❌ Qdrant client not initialized. Cannot get sample points.[/red]")
            return []
        try:
            points_response, _ = self.client.scroll( # type: ignore
                collection_name=self.collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=with_vectors
            )
            return points_response # scroll returns a tuple (points, next_offset_id)
        except Exception as e:
            rprint(f"[red]❌ Error retrieving sample points from '{self.collection_name}': {e}[/red]")
            return [] 
    
    def search_by_text(self, query: str, limit: int = 10) -> List[Any]:
        """
        Performs a text similarity search in the collection using embeddings.

        Args:
            query (str): The text query to search for.
            limit (int): The maximum number of results to return.

        Returns:
            List[Any]: A list of Qdrant scored point objects, or an empty list on error.
        """
        if not self.client:
            rprint("[red]❌ Qdrant client not initialized. Cannot perform text search.[/red]")
            return []
        try:
            from langchain_community.embeddings import FastEmbedEmbeddings # Local import
            
            # Configuration for embeddings, fetched via config_manager
            embed_model_name = config_manager.get("embedding_model", "BAAI/bge-small-en-v1.5")
            # These might not be in config, so provide defaults for .get()
            embedding_device = config_manager.get("embedding_device", "cpu") 
            use_fp16 = config_manager.get("use_fp16", False)
            
            embeddings_handler = FastEmbedEmbeddings(
                model_name=embed_model_name,
                device=embedding_device, # type: ignore # FastEmbedEmbeddings might not have device hint
                model_kwargs={"use_fp16": use_fp16}
            )
            
            query_vector = embeddings_handler.embed_query(query)
            
            search_results = self.client.search( # type: ignore
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True 
            )
            return search_results
        except ImportError:
            rprint("[red]❌ FastEmbedEmbeddings could not be imported. Ensure 'langchain_community' is installed.[/red]")
            return []
        except Exception as e:
            rprint(f"[red]❌ Error during text search in '{self.collection_name}': {e}[/red]")
            return [] 
    
    def search_by_metadata(self, field: str, value: str, limit: int = 10) -> List[Any]:
        """
        Searches for points in the collection based on a metadata field and value.

        Args:
            field (str): The metadata field key to filter on.
            value (str): The value to match for the specified metadata field.
            limit (int): The maximum number of results to return.

        Returns:
            List[Any]: A list of Qdrant point objects matching the filter, or an empty list on error.
        """
        if not self.client:
            rprint("[red]❌ Qdrant client not initialized. Cannot perform metadata search.[/red]")
            embeddings = FastEmbedEmbeddings(
                model_name=embedding_model,
                device=embedding_device,
                model_kwargs={"use_fp16": use_fp16}
            )
            
            # Generate query embedding
            query_vector = embeddings.embed_query(query)
            
            # Search using the query vector
            search_result = self.client.search( # type: ignore
                collection_name=self.collection_name, # type: ignore
                query_vector=query_vector, # type: ignore
                limit=limit, # type: ignore
                with_payload=True # type: ignore
            )
            
            return search_result
        except Exception as e:
            rprint(f"[red]❌ Error during text search: {e}[/red]")
            return [] # Return empty list on error
    
    def search_by_metadata(self, field: str, value: str, limit: int = 10):
        """Search for points by metadata field."""
        try:
            # Create filter for the metadata field
            filter_query = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key=field,
                        match=qmodels.MatchValue(value=value)
                    )
                ]
            )
            
            # Search using the filter
            search_result = self.client.scroll( # type: ignore
                collection_name=self.collection_name, # type: ignore
                filter=filter_query, # type: ignore
                limit=limit, # type: ignore
                with_payload=True # type: ignore
            )[0] # type: ignore
            
            return search_result
        except Exception as e:
            rprint(f"[red]❌ Error during metadata search: {e}[/red]")
            return [] # Return empty list on error
    
    def export_points(self, points: Optional[List[Any]], file_path: str):
        """Export points to a JSON file. If points is None or empty, no file is created."""
        if not points:
            rprint(f"[yellow]⚠️ No points provided to export. File '{file_path}' will not be created.[/yellow]")
            return

        serializable_points = []
        for point in points:
            # Assuming point objects have 'id' and 'payload' attributes
            point_id = getattr(point, 'id', None)
            payload = getattr(point, 'payload', None)
            serializable_points.append({"id": point_id, "payload": payload})
            
        if not serializable_points: # Should not happen if points is not empty, but as a safeguard
            rprint(f"[yellow]⚠️ No serializable data found in the provided points. File '{file_path}' will not be created.[/yellow]")
            return

        try:
            with open(file_path, "w") as f:
                json.dump(serializable_points, f, indent=2)
            rprint(f"[green]✅ Exported {len(serializable_points)} points to {file_path}[/green]")
        except Exception as e:
            rprint(f"[red]❌ Error exporting points to {file_path}: {e}[/red]")
    
    def display_summary(self):
        """Display a summary of the database."""
        stats = self.get_collection_stats()
        # Ensure client is available before proceeding
        if not self.client:
            rprint("[red]❌ Qdrant client not initialized. Cannot display summary.[/red]")
            return
        if not stats:
            # get_collection_stats already prints a message if collection not found
            return
        
        rprint("\n[bold cyan]📊 Database Summary[/bold cyan]")
        rprint(f"  Collection Name: [green]{self.collection_name}[/green]")
        rprint(f"  Vector Count: [green]{stats['points_count']}[/green]")
        rprint(f"  Vector Size: [green]{stats['vectors_config']['size']}[/green]")
        rprint(f"  Distance Metric: [green]{stats['vectors_config']['distance']}[/green]")
        rprint(f"  Indexed: [green]{stats['indexed']}%[/green]")
        
        if stats['points_count'] == 0:
            rprint("\n[yellow]⚠️ No documents in the database. Use 'make ingest' to add documents.[/yellow]")
    
    def display_sample_points(self, points_to_display: Optional[List[Any]], count: int = 5, full: bool = False):
        """Display sample points from the collection."""
        # points_to_display are now passed as an argument
        if not points_to_display:
            # This case can be hit if get_sample_points returned an empty list or None
            stats = self.get_collection_stats() # Check if collection itself is empty
            if stats and stats['points_count'] == 0:
                # Already handled by display_summary or indicates no points were fetched
                pass # No need to print 'No points found' again if summary already said so
            elif stats: # Collection exists but no points passed
                rprint("[yellow]⚠️ No sample points provided to display or an error occurred fetching them.[/yellow]")
            # If stats is None, get_collection_stats already printed an error.
            return

        stats = self.get_collection_stats() # Still useful for total point count context
        actual_displayed_count = len(points_to_display)
        total_points = stats['points_count'] if stats else actual_displayed_count
        
        rprint(f"\n[bold]Sample entries ({min(count, actual_displayed_count)} of {total_points}):[/bold]")
        
        # Create a table for better visualization
        table = Table(title=f"Sample Documents from '{self.collection_name}' Collection")
        table.add_column("ID", style="cyan", overflow="fold") # Added overflow for long IDs
        table.add_column("Source", style="green", overflow="fold")
        table.add_column("Fields", style="yellow", overflow="fold")
        table.add_column("Content Preview", style="blue", overflow="fold")
        
        for i, point in enumerate(points_to_display): # Iterate over passed points
            # Extract basic info
            point_id = point.id
            source = point.payload.get("source", "unknown")
            
            # Get content
            content = ""
            if "page_content" in point.payload:
                content = point.payload["page_content"]
            elif "text" in point.payload:
                content = point.payload["text"]
            
            # Format content preview
            if not full and content:
                content_preview = content[:100] + "..." if len(content) > 100 else content
            else:
                content_preview = content
            
            # Get other fields
            fields = []
            for key, value in point.payload.items():
                if key not in ["source", "page_content", "text"]:
                    if isinstance(value, str) and len(value) > 30:
                        value = value[:30] + "..."
                    fields.append(f"{key}: {value}")
            
            # Add row to table
            table.add_row(
                str(point_id),
                source,
                "\n".join(fields) if fields else "-",
                content_preview
            )
            
            # Detailed raw output for full inspection
            rprint(f"\n[bold cyan]Entry {i+1} (ID: {point_id}):[/bold cyan]")
            rprint(f"  Source: {source}")
            
            # Show other metadata fields
            for key, value in point.payload.items():
                if key != "source" and key != "page_content" and key != "text":
                    rprint(f"  {key}: {value}")
            
            # Show content if available
            if content:
                if full:
                    rprint("\n  [bold]Content:[/bold]")
                    rprint(f"  {content}")
                else:
                    rprint("\n  [bold]Content Preview:[/bold]")
                    rprint(f"  {content[:200]}{'...' if len(content) > 200 else ''}")
        
        # Print the table after detailed output
        rprint(table)
    
    def display_search_results(self, results: Optional[List[Any]], query: str = None, full: bool = False): # Added Optional and List[Any]
        """Display search results."""
        if not results:
            rprint("[yellow]⚠️ No results found (or an error occurred during search).[/yellow]")
            return
        
        # Create a table for better visualization
        title = f"Search Results" if not query else f"Search Results for '{query}'"
        table = Table(title=title)
        table.add_column("ID", style="cyan", overflow="fold") # Added overflow for long IDs
        table.add_column("Source", style="green", overflow="fold")
        table.add_column("Score", style="yellow")
        table.add_column("Content Preview", style="blue", overflow="fold")
        
        for i, point in enumerate(results): # Iterate over passed results
            # Extract basic info
            point_id = point.id
            source = point.payload.get("source", "unknown")
            
            # Get score if available
            score = getattr(point, "score", "N/A")
            if isinstance(score, float):
                score = f"{score:.4f}"
            
            # Get content
            content = ""
            if "page_content" in point.payload:
                content = point.payload["page_content"]
            elif "text" in point.payload:
                content = point.payload["text"]
            
            # Format content preview
            if not full and content:
                content_preview = content[:100] + "..." if len(content) > 100 else content
            else:
                content_preview = content
            
            # Add row to table
            table.add_row(
                str(point_id),
                source,
                str(score),
                content_preview
            )
            
            # Detailed raw output for full inspection
            rprint(f"\n[bold cyan]Result {i+1} (ID: {point_id}):[/bold cyan]")
            rprint(f"  Source: {source}")
            rprint(f"  Score: {score}")
            
            # Show content if available
            if content:
                if full:
                    rprint("\n  [bold]Content:[/bold]")
                    rprint(f"  {content}")
                else:
                    rprint("\n  [bold]Content Preview:[/bold]")
                    rprint(f"  {content[:200]}{'...' if len(content) > 200 else ''}")
        
        # Print the table after detailed output
        rprint(table)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Audit and search Qdrant database")
    parser.add_argument("--count", type=int, default=5, help="Number of samples to show")
    parser.add_argument("--full", action="store_true", help="Show full document contents")
    parser.add_argument("--export", type=str, help="Export audit to specified file")
    parser.add_argument("--points", type=int, default=None, help="Show specific number of points")
    parser.add_argument("--summary", action="store_true", help="Show only summary information")
    parser.add_argument("--search", type=str, help="Search for documents by text similarity")
    parser.add_argument("--field", type=str, help="Metadata field to search (use with --value)")
    parser.add_argument("--value", type=str, help="Value to search for in metadata field")
    parser.add_argument("--limit", type=int, default=SEARCH_LIMIT, help="Maximum number of search results")
    args = parser.parse_args()
    
    rprint("\n[bold cyan]🔍 Auditing Qdrant Database[/bold cyan]")
    rprint("[dim]Run with --help to see all available options[/dim]\n")
    
    try:
        auditor = QdrantAuditor()
        # Ensure client was initialized
        if not auditor.client:
            rprint("[red]❌ Auditor client not initialized. Exiting.[/red]")
            return

        results_to_export = None

        # Handle search operations first
        if args.search:
            rprint(f"\n[bold cyan]🔍 Searching for: {args.search}[/bold cyan]")
            search_results = auditor.search_by_text(args.search, limit=args.limit)
            auditor.display_search_results(search_results, query=args.search, full=args.full)
            if args.export:
                results_to_export = search_results
        
        elif args.field and args.value:
            rprint(f"\n[bold cyan]🔍 Searching for metadata: {args.field}={args.value}[/bold cyan]")
            metadata_search_results = auditor.search_by_metadata(args.field, args.value, limit=args.limit)
            auditor.display_search_results(metadata_search_results, query=f"{args.field}={args.value}", full=args.full)
            if args.export:
                results_to_export = metadata_search_results
        
        else:
            # Default action: Display summary and optionally sample points
            auditor.display_summary()
            
            if not args.summary:
                limit = args.points if args.points is not None else args.count
                sample_points = auditor.get_sample_points(limit=limit, with_vectors=False)
                # Pass the fetched points to display_sample_points
                auditor.display_sample_points(points_to_display=sample_points, count=limit, full=args.full)
                if args.export:
                    results_to_export = sample_points
            else: # --summary was used
                 rprint("\n[dim]For more details (sample points), run without --summary flag[/dim]")

        # Consolidated export logic
        if args.export and results_to_export is not None:
            auditor.export_points(results_to_export, args.export)
        elif args.export and results_to_export is None:
            # This case handles if --export was specified with --summary only, or if search yielded no results
            rprint(f"[yellow]⚠️ --export specified, but no results to export (e.g. --summary only, or search found nothing).[/yellow]")

    except RuntimeError as e: # Catch specific RuntimeError from _connect_to_qdrant
        rprint(f"[red]❌ Failed to connect to Qdrant: {e}[/red]")
    except Exception as e:
        rprint(f"[red]❌ An unexpected error occurred: {e}[/red]")
        # import traceback # Only for debugging, remove for production
        # rprint(traceback.format_exc())

if __name__ == "__main__":
    main()