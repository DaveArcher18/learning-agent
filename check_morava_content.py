#!/usr/bin/env python
"""
check_morava_content.py
--------------------
Check if information about Morava K-theory exists in the Qdrant database
and provide instructions for adding it if missing.
"""

import os
import yaml
from qdrant_client import QdrantClient
from rich import print as rprint
from rich.panel import Panel

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

def connect_to_qdrant():
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

def search_for_morava_content(client):
    """Search for Morava K-theory content in the database."""
    try:
        # Check if collection exists
        collections = [c.name for c in client.get_collections().collections]
        if COLLECTION not in collections:
            rprint(f"[yellow]⚠️ Collection '{COLLECTION}' not found.[/yellow]")
            return False, 0
        
        # Get collection info
        collection_info = client.get_collection(COLLECTION)
        vector_count = collection_info.points_count
        
        if vector_count == 0:
            rprint(f"[yellow]⚠️ Collection '{COLLECTION}' is empty.[/yellow]")
            return False, 0
        
        # Search for Morava K-theory content
        search_terms = ["Morava", "K-theory", "Morava K-theory"]
        found_count = 0
        
        for term in search_terms:
            # Use scroll to search through payload text
            points = client.scroll(
                collection_name=COLLECTION,
                scroll_filter=None,  # No filter, get all points
                limit=100,  # Get up to 100 points
                with_payload=True,
                with_vectors=False
            )[0]
            
            # Check each point for the search term
            for point in points:
                content = ""
                if "page_content" in point.payload:
                    content = point.payload["page_content"]
                elif "text" in point.payload:
                    content = point.payload["text"]
                
                if term.lower() in content.lower():
                    found_count += 1
                    rprint(f"[green]✅ Found content containing '{term}'[/green]")
                    rprint(f"  Source: {point.payload.get('source', 'unknown')}")
                    preview = content[:100] + "..." if len(content) > 100 else content
                    rprint(f"  Preview: {preview}\n")
        
        if found_count > 0:
            rprint(f"[green]✅ Found {found_count} entries related to Morava K-theory[/green]")
            return True, found_count
        else:
            rprint("[yellow]⚠️ No content related to Morava K-theory found[/yellow]")
            return False, 0
    
    except Exception as e:
        rprint(f"[red]❌ Error searching for Morava K-theory content: {e}[/red]")
        return False, 0

def main():
    """Main function."""
    rprint(Panel.fit(
        "[bold cyan]Morava K-theory Content Check[/bold cyan]\n\n"
        "This script checks if information about Morava K-theory exists in the Qdrant database.",
        title="🔍 Content Check",
        border_style="cyan"
    ))
    
    try:
        # Connect to Qdrant
        client = connect_to_qdrant()
        
        # Search for Morava K-theory content
        found, count = search_for_morava_content(client)
        
        if found:
            rprint("\n[bold green]✅ Morava K-theory content exists in the database![/bold green]")
            rprint("\n[cyan]The retrieval issue is likely due to connection problems with Ollama.[/cyan]")
            rprint("[cyan]Run the fix_retrieval.py script to improve error handling and timeout management.[/cyan]")
            rprint("\n  python fix_retrieval.py")
        else:
            rprint("\n[bold yellow]⚠️ No Morava K-theory content found in the database![/bold yellow]")
            rprint("\n[cyan]To add Morava K-theory content to the database:[/cyan]")
            rprint("1. Create a text file with information about Morava K-theory:")
            rprint("   mkdir -p docs/mathematics")
            rprint("   touch docs/mathematics/morava_k_theory.txt")
            
            # Sample content for Morava K-theory
            morava_content = """\
Title: Morava K-theory

Morava K-theory is a generalized cohomology theory in algebraic topology, named after mathematician Jack Morava. It is a key component in chromatic homotopy theory.

Morava K-theory, denoted K(n), is a family of cohomology theories parameterized by a prime number p and a positive integer n. Each K(n) is a complex-oriented cohomology theory with a formal group law of height n.

Key properties of Morava K-theory:
1. K(n) has coefficient ring K(n)* = Fp[vn, vn^(-1)], where vn has degree 2(p^n - 1).
2. K(n) is a periodic cohomology theory with period 2(p^n - 1).
3. The formal group law associated to K(n) has height n.
4. K(n) detects the nth chromatic layer of the stable homotopy groups of spheres.

Morava K-theories play a central role in the chromatic approach to stable homotopy theory, which organizes the stable homotopy category into chromatic layers based on the height of formal group laws.

Applications include:
- Computation of stable homotopy groups of spheres
- Understanding of the chromatic filtration
- Classification of formal group laws
- Connections to modular forms and number theory

Morava K-theory is related to other important cohomology theories such as Johnson-Wilson theory E(n) and Morava E-theory E_n.
"""
            
            rprint(f"\n[cyan]Sample content for morava_k_theory.txt:[/cyan]")
            rprint(Panel(morava_content, expand=False))
            
            rprint("\n2. Add the content to the file:")
            rprint("   nano docs/mathematics/morava_k_theory.txt  # Paste the sample content")
            
            rprint("\n3. Ingest the documents:")
            rprint("   python ingest.py --path ./docs")
            
            rprint("\n4. Run the fix_retrieval.py script to improve error handling:")
            rprint("   python fix_retrieval.py")
            
            rprint("\n5. Start the learning agent and try querying about Morava K-theory again:")
            rprint("   python learning_agent.py")
    
    except Exception as e:
        rprint(f"[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    main()