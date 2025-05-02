#!/usr/bin/env python
"""
audit_qdrant.py
--------------
Audit the Qdrant database for LearningAgent.
Displays stats and sample data.
"""

from qdrant_client import QdrantClient
from rich import print as rprint
from rich.table import Table
import argparse

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Audit Qdrant database")
    parser.add_argument("--count", type=int, default=5, help="Number of samples to show")
    parser.add_argument("--full", action="store_true", help="Show full document contents")
    parser.add_argument("--export", type=str, help="Export audit to specified file")
    parser.add_argument("--points", type=int, default=None, help="Show specific number of points")
    args = parser.parse_args()
    
    rprint("[cyan]🔍 Auditing Qdrant database...[/cyan]")
    
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
        except Exception:
            # Fall back to embedded
            client = QdrantClient(path="./qdrant_data")
            collections = client.get_collections().collections
            log("[green]✅ Connected to embedded Qdrant[/green]")
        
        collection_names = [collection.name for collection in collections]
        log(f"[bold]Collections: {collection_names}[/bold]")
        
        if "kb" in collection_names:
            collection_info = client.get_collection("kb")
            vector_count = collection_info.points_count
            vector_size = collection_info.config.params.vectors.size
            log(f"[bold green]Collection 'kb' contains {vector_count} vectors (size: {vector_size})[/bold green]")
            
            # Show collection config
            log("[bold cyan]Vector Configuration:[/bold cyan]")
            log(f"  Distance: {collection_info.config.params.vectors.distance}")
            log(f"  Size: {collection_info.config.params.vectors.size}")
            
            if vector_count > 0:
                # Get a sample of points to show metadata
                limit = args.points if args.points is not None else args.count
                
                points = client.scroll(
                    collection_name="kb",
                    limit=limit,
                    with_payload=True,
                    with_vectors=False
                )[0]
                
                log(f"\n[bold]Sample entries ({min(limit, len(points))} of {vector_count}):[/bold]")
                
                # Create a table for better visualization
                table = Table(title=f"Sample Documents from 'kb' Collection")
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
            log("[yellow]⚠️ Collection 'kb' not found[/yellow]")
            
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