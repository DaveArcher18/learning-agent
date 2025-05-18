#!/usr/bin/env python
"""
audit_qdrant.py
--------------
Audit and search the Qdrant database for LearningAgent.
Displays stats, sample data, and provides search capabilities.
"""

import os
import yaml
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from rich import print as rprint
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress

# Load configuration
CONFIG_PATH = "config.yaml"

def load_config():
    """Load configuration from YAML file."""
    if not os.path.exists(CONFIG_PATH):
        rprint(f"[yellow]⚠️ Config file {CONFIG_PATH} not found, using defaults.[/yellow]")
        return {
            "collection": "kb",
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "db_search_limit": 20
        }

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
COLLECTION = CONFIG.get("collection", "kb")
SEARCH_LIMIT = CONFIG.get("db_search_limit", 20)

class QdrantAuditor:
    """Class for auditing and searching Qdrant database."""
    
    def __init__(self):
        self.client = self._connect_to_qdrant()
        self.collection_name = COLLECTION
        self.console = Console()
    
    def _connect_to_qdrant(self) -> QdrantClient:
        """Connect to Qdrant, prioritizing Docker over embedded."""
        # Try Docker connection first
        try:
            client = QdrantClient(host="localhost", port=6333)
            # Test the connection
            client.get_collections()
            rprint("[green]✅ Connected to Docker Qdrant[/green]")
            return client
        except Exception as docker_e:
            rprint(f"[yellow]⚠️ Could not connect to Docker Qdrant: {docker_e}[/yellow]")
            
            # Try embedded Qdrant as fallback
            try:
                rprint("[cyan]🔄 Trying embedded Qdrant as fallback...[/cyan]")
                client = QdrantClient(path="./qdrant_data")
                client.get_collections()
                rprint("[green]✅ Connected to embedded Qdrant[/green]")
                return client
            except Exception as e:
                rprint(f"[red]❌ Failed to connect to embedded Qdrant: {e}[/red]")
                rprint("[yellow]💡 Try running 'make start_qdrant' to start Qdrant Docker[/yellow]")
                raise RuntimeError("Could not connect to any Qdrant instance")
    
    def get_collection_info(self):
        """Get information about the collection."""
        collections = [c.name for c in self.client.get_collections().collections]
        
        if self.collection_name in collections:
            return self.client.get_collection(self.collection_name)
        else:
            rprint(f"[yellow]⚠️ Collection '{self.collection_name}' not found[/yellow]")
            return None
    
    def get_collection_stats(self):
        """Get statistics about the collection."""
        collection_info = self.get_collection_info()
        if not collection_info:
            return None
        
        return {
            "points_count": collection_info.points_count,
            "vectors_config": {
                "size": collection_info.config.params.vectors.size,
                "distance": str(collection_info.config.params.vectors.distance)
            },
            "indexed": collection_info.indexed_percent
        }
    
    def get_sample_points(self, limit: int = 5, with_vectors: bool = False):
        """Get sample points from the collection."""
        try:
            return self.client.scroll(
                collection_name=self.collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=with_vectors
            )[0]
        except Exception as e:
            rprint(f"[red]❌ Error retrieving sample points: {e}[/red]")
            return []
    
    def search_by_text(self, query: str, limit: int = 10):
        """Search for points by text similarity."""
        try:
            # Import here to avoid circular imports
            from langchain_community.embeddings import FastEmbedEmbeddings
            
            # Get embedding model from config
            embedding_model = CONFIG.get("embedding_model", "BAAI/bge-small-en-v1.5")
            embedding_device = CONFIG.get("embedding_device", "cpu")
            use_fp16 = CONFIG.get("use_fp16", False)
            
            # Create embeddings
            embeddings = FastEmbedEmbeddings(
                model_name=embedding_model,
                device=embedding_device,
                model_kwargs={"use_fp16": use_fp16}
            )
            
            # Generate query embedding
            query_vector = embeddings.embed_query(query)
            
            # Search using the query vector
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )
            
            return search_result
        except Exception as e:
            rprint(f"[red]❌ Error during text search: {e}[/red]")
            return []
    
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
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                filter=filter_query,
                limit=limit,
                with_payload=True
            )[0]
            
            return search_result
        except Exception as e:
            rprint(f"[red]❌ Error during metadata search: {e}[/red]")
            return []
    
    def export_points(self, points, file_path: str):
        """Export points to a JSON file."""
        try:
            # Convert points to serializable format
            serializable_points = []
            for point in points:
                point_dict = {
                    "id": point.id,
                    "payload": point.payload
                }
                serializable_points.append(point_dict)
            
            # Write to file
            with open(file_path, "w") as f:
                json.dump(serializable_points, f, indent=2)
            
            rprint(f"[green]✅ Exported {len(serializable_points)} points to {file_path}[/green]")
        except Exception as e:
            rprint(f"[red]❌ Error exporting points: {e}[/red]")
    
    def display_summary(self):
        """Display a summary of the database."""
        stats = self.get_collection_stats()
        if not stats:
            return
        
        rprint("\n[bold cyan]📊 Database Summary[/bold cyan]")
        rprint(f"  Collection Name: [green]{self.collection_name}[/green]")
        rprint(f"  Vector Count: [green]{stats['points_count']}[/green]")
        rprint(f"  Vector Size: [green]{stats['vectors_config']['size']}[/green]")
        rprint(f"  Distance Metric: [green]{stats['vectors_config']['distance']}[/green]")
        rprint(f"  Indexed: [green]{stats['indexed']}%[/green]")
        
        if stats['points_count'] == 0:
            rprint("\n[yellow]⚠️ No documents in the database. Use 'make ingest' to add documents.[/yellow]")
    
    def display_sample_points(self, count: int = 5, full: bool = False):
        """Display sample points from the collection."""
        stats = self.get_collection_stats()
        if not stats or stats['points_count'] == 0:
            return
        
        points = self.get_sample_points(limit=count)
        if not points:
            return
        
        rprint(f"\n[bold]Sample entries ({min(count, len(points))} of {stats['points_count']}):[/bold]")
        
        # Create a table for better visualization
        table = Table(title=f"Sample Documents from '{self.collection_name}' Collection")
        table.add_column("ID", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Fields", style="yellow")
        table.add_column("Content Preview", style="blue")
        
        for i, point in enumerate(points):
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
    
    def display_search_results(self, results, query: str = None, full: bool = False):
        """Display search results."""
        if not results:
            rprint("[yellow]⚠️ No results found[/yellow]")
            return
        
        # Create a table for better visualization
        title = f"Search Results" if not query else f"Search Results for '{query}'"
        table = Table(title=title)
        table.add_column("ID", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Score", style="yellow")
        table.add_column("Content Preview", style="blue")
        
        for i, point in enumerate(results):
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
        
        # Handle search operations first
        if args.search:
            rprint(f"\n[bold cyan]🔍 Searching for: {args.search}[/bold cyan]")
            results = auditor.search_by_text(args.search, limit=args.limit)
            auditor.display_search_results(results, query=args.search, full=args.full)
            
            # Export results if requested
            if args.export:
                auditor.export_points(results, args.export)
            
            return
        
        # Handle metadata search
        if args.field and args.value:
            rprint(f"\n[bold cyan]🔍 Searching for metadata: {args.field}={args.value}[/bold cyan]")
            results = auditor.search_by_metadata(args.field, args.value, limit=args.limit)
            auditor.display_search_results(results, full=args.full)
            
            # Export results if requested
            if args.export:
                auditor.export_points(results, args.export)
            
            return
        
        # Display summary
        auditor.display_summary()
        
        # If summary only, skip the detailed information
        if args.summary:
            rprint("\n[dim]For more details, run without --summary flag[/dim]")
            return
        
        # Display sample points
        limit = args.points if args.points is not None else args.count
        auditor.display_sample_points(count=limit, full=args.full)
        
        # Export if requested
        if args.export:
            points = auditor.get_sample_points(limit=limit)
            auditor.export_points(points, args.export)
            
    except Exception as e:
        rprint(f"[red]❌ Fatal error: {e}[/red]")
        import traceback
        rprint(traceback.format_exc())
    
    def log(msg):
        """Log message to both console and output list"""
        rprint(msg)
        if args.export:
            output.append(msg.replace("[bold]", "").replace("[/bold]", "")
                         .replace("[bold green]", "").replace("[/bold green]", "")
                         .replace("[bold cyan]", "").replace("[/bold cyan]", "")
                         .replace("[yellow]", "").replace("[/yellow]", "")
                         .replace("[red]", "").replace("[/red]", "")
                         .replace("[green]", "").replace("[/green]", "")
                         .replace("[cyan]", "").replace("[/cyan]", "")
                         .replace("[blue]", "").replace("[/blue]", "")
                         .replace("[dim]", "").replace("[/dim]", ""))
    
    try:
        # Try Docker first
        try:
            client = QdrantClient(host="localhost", port=6333)
            collections = client.get_collections().collections
            log("[green]✅ Connected to Docker Qdrant[/green]")
            connection_type = "Docker"
        except Exception:
            # Fall back to embedded
            client = QdrantClient(path="./qdrant_data")
            collections = client.get_collections().collections
            log("[green]✅ Connected to embedded Qdrant[/green]")
            connection_type = "Embedded"
        
        collection_names = [collection.name for collection in collections]
        log(f"[bold]Collections: {collection_names}[/bold]")
        
        if COLLECTION in collection_names:
            collection_info = client.get_collection(COLLECTION)
            vector_count = collection_info.points_count
            vector_size = collection_info.config.params.vectors.size
            
            # Display summary information in a more structured format
            log("\n[bold cyan]📊 Database Summary[/bold cyan]")
            log(f"  Connection Type: [green]{connection_type}[/green]")
            log(f"  Collection Name: [green]{COLLECTION}[/green]")
            log(f"  Vector Count: [green]{vector_count}[/green]")
            log(f"  Vector Size: [green]{vector_size}[/green]")
            log(f"  Distance Metric: [green]{collection_info.config.params.vectors.distance}[/green]")
            
            # If summary only, skip the detailed information
            if args.summary:
                if vector_count == 0:
                    log("\n[yellow]⚠️ No documents in the database. Use 'make ingest' to add documents.[/yellow]")
                log("\n[dim]For more details, run without --summary flag[/dim]")
                return
            
            # Show collection config for non-summary mode
            log("\n[bold cyan]Vector Configuration:[/bold cyan]")
            log(f"  Distance: {collection_info.config.params.vectors.distance}")
            log(f"  Size: {collection_info.config.params.vectors.size}")
            
            if vector_count > 0:
                # Get a sample of points to show metadata
                limit = args.points if args.points is not None else args.count
                
                points = client.scroll(
                    collection_name=COLLECTION,
                    limit=limit,
                    with_payload=True,
                    with_vectors=False
                )[0]
                
                log(f"\n[bold]Sample entries ({min(limit, len(points))} of {vector_count}):[/bold]")
                
                # Create a table for better visualization
                table = Table(title=f"Sample Documents from '{COLLECTION}' Collection")
                table.add_column("ID", style="cyan")
                table.add_column("Source", style="green")
                table.add_column("Fields", style="yellow")
                table.add_column("Content Preview", style="blue")
                
                for i, point in enumerate(points):
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
                    if not args.full and content:
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
                    log(f"\n[bold cyan]Entry {i+1} (ID: {point_id}):[/bold cyan]")
                    log(f"  Source: {source}")
                    
                    # Show other metadata fields
                    for key, value in point.payload.items():
                        if key != "source" and key != "page_content" and key != "text":
                            log(f"  {key}: {value}")
                    
                    # Show content if available
                    if content:
                        if args.full:
                            log("\n  [bold]Content:[/bold]")
                            log(f"  {content}")
                        else:
                            log("\n  [bold]Content Preview:[/bold]")
                            log(f"  {content[:200]}{'...' if len(content) > 200 else ''}")
                
                # Print the table after detailed output
                rprint(table)
                
                # If exporting, also add table data as text
                if args.export:
                    output.append("\nSAMPLE DOCUMENTS (TABULAR)")
                    output.append("--------------------------")
                    for i, point in enumerate(points):
                        point_id = point.id
                        source = point.payload.get("source", "unknown")
                        output.append(f"Entry {i+1} (ID: {point_id})")
                        output.append(f"Source: {source}")
                        
                        content = ""
                        if "page_content" in point.payload:
                            content = point.payload["page_content"]
                        elif "text" in point.payload:
                            content = point.payload["text"]
                        
                        output.append(f"Content preview: {content[:100]}{'...' if len(content) > 100 else ''}")
                        output.append("---")
            else:
                log("[yellow]⚠️ Collection exists but contains no vectors[/yellow]")
        else:
            log(f"[yellow]⚠️ Collection '{COLLECTION}' not found[/yellow]")
            
        # Export to file if requested
        if args.export:
            with open(args.export, 'w') as f:
                f.write("\n".join(output))
            rprint(f"[green]✅ Audit exported to {args.export}[/green]")
            
    except Exception as e:
        rprint(f"[red]❌ Error connecting to Qdrant: {e}[/red]")
        import traceback
        rprint(traceback.format_exc())

if __name__ == "__main__":
    main()