#!/usr/bin/env python
"""
audit_qdrant.py
--------------
Audit the Qdrant database for LearningAgent.
Displays stats and sample data.
"""

import os
import yaml
import argparse
from qdrant_client import QdrantClient
from rich import print as rprint
from rich.table import Table

# Load configuration
CONFIG_PATH = "config.yaml"

def load_config():
    """Load configuration from YAML file."""
    if not os.path.exists(CONFIG_PATH):
        rprint(f"[yellow]⚠️ Config file {CONFIG_PATH} not found, using defaults.[/yellow]")
        return {
            "collection": "kb",
        }

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
COLLECTION = CONFIG.get("collection", "kb")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Audit Qdrant database")
    parser.add_argument("--count", type=int, default=5, help="Number of samples to show")
    parser.add_argument("--full", action="store_true", help="Show full document contents")
    parser.add_argument("--export", type=str, help="Export audit to specified file")
    parser.add_argument("--points", type=int, default=None, help="Show specific number of points")
    parser.add_argument("--summary", action="store_true", help="Show only summary information")
    args = parser.parse_args()
    
    rprint("\n[bold cyan]🔍 Auditing Qdrant Database[/bold cyan]")
    rprint("[dim]Run with --help to see all available options[/dim]\n")
    
    output = []  # Store output for optional file export
    
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