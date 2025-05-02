#!/usr/bin/env python
"""
test_retrieval.py
----------------
Test script to diagnose retrieval issues in the learning agent.
This script:
1. Examines the contents of the Qdrant database
2. Performs test queries to see what's being retrieved
3. Helps diagnose issues with web search results not being found
"""

import sys
import argparse
from rich.console import Console
from rich.table import Table
from qdrant_client import QdrantClient
from pathlib import Path

# Add the current directory to path to import from learning_agent.py
sys.path.append('.')

# Import functions from learning_agent
from learning_agent import (
    connect_to_qdrant, 
    Embedder, 
    EMBED_MODEL_NAME, 
    embed_with_fallback,
    init_vector_store,
    build_retriever,
    get_llm,
    CONFIG
)

console = Console()

def list_all_points(client, collection_name="kb", limit=10):
    """List all points in the collection, including their payloads"""
    console.print(f"[cyan]Listing up to {limit} points from collection '{collection_name}'...[/cyan]")
    
    try:
        # Get total count
        collection_info = client.get_collection(collection_name)
        total_count = collection_info.points_count
        console.print(f"[green]Total points in collection: {total_count}[/green]")
        
        # Scroll through points
        points = client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )[0]
        
        # Create a table of results
        table = Table(title=f"Points in {collection_name} Collection")
        table.add_column("ID", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Query", style="yellow")
        table.add_column("Content Preview", style="blue")
        
        for point in points:
            # Extract information
            point_id = point.id
            source = point.payload.get("source", "unknown")
            query = point.payload.get("query", "-")
            
            # Extract content
            content = ""
            if "page_content" in point.payload:
                content = point.payload["page_content"]
            
            # Truncate content for display
            if content and len(content) > 100:
                content_preview = content[:97] + "..."
            else:
                content_preview = content or "-"
            
            # Add to table
            table.add_row(
                str(point_id),
                source,
                query,
                content_preview
            )
        
        console.print(table)
        return points
    
    except Exception as e:
        console.print(f"[red]Error listing points: {e}[/red]")
        return []

def perform_test_query(query, top_k=5):
    """Perform a test query and show what's being retrieved"""
    console.print(f"[cyan]Performing test query: '{query}'[/cyan]")
    
    try:
        # Initialize components
        llm = get_llm()
        embedder = Embedder(EMBED_MODEL_NAME)
        vector_store = init_vector_store(embedder)
        retriever = build_retriever(vector_store, llm, top_k)
        
        # Perform retrieval
        docs = retriever.invoke(query)
        
        console.print(f"[green]Retrieved {len(docs)} documents[/green]")
        
        # Display results in a table
        table = Table(title=f"Retrieved Documents for Query: '{query}'")
        table.add_column("Index", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Content Preview", style="blue")
        table.add_column("Score", style="yellow")
        
        for i, doc in enumerate(docs, 1):
            content = doc.page_content
            metadata = doc.metadata
            source = metadata.get("source", "unknown")
            score = metadata.get("score", "-")
            
            # Truncate content for display
            if content and len(content) > 100:
                content_preview = content[:97] + "..."
            else:
                content_preview = content or "-"
            
            # Add to table
            table.add_row(
                str(i),
                source,
                content_preview,
                str(score) if score != "-" else "-"
            )
        
        console.print(table)
        return docs
    
    except Exception as e:
        console.print(f"[red]Error performing test query: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        return []

def direct_search(query, client, top_k=5):
    """Perform a direct search against Qdrant without using the retriever"""
    console.print(f"[cyan]Performing direct search: '{query}'[/cyan]")
    
    try:
        # Create embedding for query
        embedder = Embedder(EMBED_MODEL_NAME)
        query_vector = embed_with_fallback(embedder, query)
        
        # Search directly
        results = client.search(
            collection_name="kb",
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        console.print(f"[green]Found {len(results)} results[/green]")
        
        # Display results in a table
        table = Table(title=f"Direct Search Results for Query: '{query}'")
        table.add_column("ID", style="cyan")
        table.add_column("Score", style="yellow", justify="right")
        table.add_column("Source", style="green")
        table.add_column("Query", style="magenta")
        table.add_column("Content Preview", style="blue")
        
        for result in results:
            # Extract information
            point_id = result.id
            score = result.score
            source = result.payload.get("source", "unknown")
            stored_query = result.payload.get("query", "-")
            
            # Extract content
            content = ""
            if "page_content" in result.payload:
                content = result.payload["page_content"]
            
            # Truncate content for display
            if content and len(content) > 100:
                content_preview = content[:97] + "..."
            else:
                content_preview = content or "-"
            
            # Add to table
            table.add_row(
                str(point_id),
                f"{score:.4f}",
                source,
                stored_query,
                content_preview
            )
        
        console.print(table)
        return results
    
    except Exception as e:
        console.print(f"[red]Error performing direct search: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        return []

def filter_by_query(query_term, client, limit=10):
    """Find vectors with a specific query term in their payload"""
    console.print(f"[cyan]Finding vectors with query term: '{query_term}'[/cyan]")
    
    try:
        from qdrant_client.models import Filter, FieldCondition, MatchText
        
        # Create filter
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="query",
                    match=MatchText(text=query_term)
                )
            ]
        )
        
        # Scroll with filter - using the filter parameter correctly
        points = client.scroll(
            collection_name="kb",
            scroll_filter=query_filter,  # Use scroll_filter instead of filter
            limit=limit,
            with_payload=True,
            with_vectors=False
        )[0]
        
        console.print(f"[green]Found {len(points)} points with query term '{query_term}'[/green]")
        
        # Create a table of results
        table = Table(title=f"Points with Query Term: '{query_term}'")
        table.add_column("ID", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Query", style="yellow")
        table.add_column("Content Preview", style="blue")
        
        for point in points:
            # Extract information
            point_id = point.id
            source = point.payload.get("source", "unknown")
            query = point.payload.get("query", "-")
            
            # Extract content
            content = ""
            if "page_content" in point.payload:
                content = point.payload["page_content"]
            
            # Truncate content for display
            if content and len(content) > 100:
                content_preview = content[:97] + "..."
            else:
                content_preview = content or "-"
            
            # Add to table
            table.add_row(
                str(point_id),
                source,
                query,
                content_preview
            )
        
        console.print(table)
        return points
    
    except Exception as e:
        console.print(f"[red]Error filtering by query term: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        return []

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test retrieval for LearningAgent")
    parser.add_argument("--query", type=str, help="Test query to search for")
    parser.add_argument("--list", action="store_true", help="List database contents")
    parser.add_argument("--limit", type=int, default=10, help="Limit for results")
    parser.add_argument("--direct", action="store_true", help="Perform direct search")
    parser.add_argument("--filter", type=str, help="Filter by query term")
    args = parser.parse_args()
    
    # Connect to Qdrant
    console.print("[cyan]Connecting to Qdrant...[/cyan]")
    client = connect_to_qdrant()
    
    # Check collection
    try:
        collection_info = client.get_collection("kb")
        console.print(f"[green]Collection 'kb' contains {collection_info.points_count} points[/green]")
    except Exception as e:
        console.print(f"[red]Error getting collection info: {e}[/red]")
    
    # List contents if requested
    if args.list:
        list_all_points(client, limit=args.limit)
    
    # Filter by query term if requested
    if args.filter:
        filter_by_query(args.filter, client, limit=args.limit)
    
    # Perform test query if provided
    if args.query:
        if args.direct:
            direct_search(args.query, client, top_k=args.limit)
        else:
            perform_test_query(args.query, top_k=args.limit)

if __name__ == "__main__":
    main() 