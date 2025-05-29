"""
Legacy Qdrant vector service for migration support.

This module provides Qdrant connectivity and data export functionality 
to support migration to RAGFlow. Will be deprecated after migration completion.
"""

from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from rich import print as rprint
import logging


logger = logging.getLogger(__name__)


class LegacyQdrantService:
    """
    Legacy Qdrant service for data migration and fallback support.
    
    This class provides connection management and data export functionality
    to support the migration from Qdrant to RAGFlow with BGE-M3 embeddings.
    """
    
    def __init__(self, collection_name: str = "kb") -> None:
        """
        Initialize legacy Qdrant service.
        
        Args:
            collection_name: Name of the Qdrant collection
        """
        self.collection_name = collection_name
        self.client: Optional[QdrantClient] = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to Qdrant with fallback mechanisms."""
        try:
            self.client = self._connect_to_docker()
        except Exception as e_docker:
            logger.warning(f"Docker connection failed: {e_docker}")
            try:
                self.client = self._connect_to_embedded()
            except Exception as e_embedded:
                logger.error(f"Embedded connection failed: {e_embedded}")
                raise RuntimeError(
                    "Failed to connect to Qdrant. Both Docker and embedded attempts failed."
                )
    
    def _connect_to_docker(self) -> QdrantClient:
        """Connect to Qdrant running in Docker."""
        client = QdrantClient(host="localhost", port=6333)
        client.get_collections()  # Validate connection
        rprint("[green]✅ Connected to Qdrant in Docker (localhost:6333).[/green]")
        logger.info("Successfully connected to Qdrant Docker instance")
        return client
    
    def _connect_to_embedded(self) -> QdrantClient:
        """Connect to embedded Qdrant instance."""
        client = QdrantClient(path="./qdrant_data")
        client.get_collections()  # Validate connection
        rprint("[green]✅ Connected to embedded Qdrant (./qdrant_data).[/green]")
        logger.info("Successfully connected to embedded Qdrant instance")
        return client
    
    def is_connected(self) -> bool:
        """Check if Qdrant client is connected."""
        if not self.client:
            return False
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False
    
    def collection_exists(self) -> bool:
        """Check if the collection exists."""
        if not self.client:
            return False
        try:
            collections = self.client.get_collections()
            return any(col.name == self.collection_name for col in collections.collections)
        except Exception as e:
            logger.error(f"Error checking collection existence: {e}")
            return False
    
    def get_collection_info(self) -> Optional[Dict[str, Any]]:
        """Get collection information for migration planning."""
        if not self.client or not self.collection_exists():
            return None
        
        try:
            collection_info = self.client.get_collection(self.collection_name)
            points_count = self.client.count(self.collection_name)
            
            return {
                "name": self.collection_name,
                "vectors_config": collection_info.config.params.vectors,
                "points_count": points_count.count,
                "status": collection_info.status,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return None
    
    def export_all_points(self, batch_size: int = 100) -> List[Dict[str, Any]]:
        """
        Export all points from the collection for migration.
        
        Args:
            batch_size: Number of points to retrieve per batch
            
        Returns:
            List of points with vectors and metadata
        """
        if not self.client or not self.collection_exists():
            return []
        
        all_points = []
        offset = None
        
        try:
            while True:
                # Retrieve points with vectors and payload
                result = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=batch_size,
                    offset=offset,
                    with_vectors=True,
                    with_payload=True,
                )
                
                points, next_offset = result
                
                if not points:
                    break
                
                # Convert points to export format
                for point in points:
                    point_data = {
                        "id": str(point.id),
                        "vector": point.vector,
                        "payload": point.payload or {},
                    }
                    all_points.append(point_data)
                
                # Check if we've reached the end
                if next_offset is None:
                    break
                    
                offset = next_offset
                
                if len(all_points) % 1000 == 0:
                    rprint(f"[cyan]Exported {len(all_points)} points...[/cyan]")
        
        except Exception as e:
            logger.error(f"Error exporting points: {e}")
            rprint(f"[red]❌ Error during export: {e}[/red]")
        
        rprint(f"[green]✅ Exported {len(all_points)} total points.[/green]")
        return all_points
    
    def export_to_ragflow_format(self) -> Dict[str, Any]:
        """
        Export data in a format suitable for RAGFlow migration.
        
        Returns:
            Dictionary containing collection metadata and documents
        """
        collection_info = self.get_collection_info()
        if not collection_info:
            return {"error": "Collection not found or not accessible"}
        
        points = self.export_all_points()
        
        # Convert to RAGFlow-compatible format
        documents = []
        for point in points:
            doc = {
                "id": point["id"],
                "content": point["payload"].get("content", ""),
                "metadata": {
                    k: v for k, v in point["payload"].items() 
                    if k != "content"
                },
                "legacy_vector": point["vector"],  # For validation
            }
            documents.append(doc)
        
        return {
            "collection_info": collection_info,
            "documents": documents,
            "migration_metadata": {
                "source": "qdrant",
                "target": "ragflow",
                "embedding_model": "BAAI/bge-small-en-v1.5",  # Legacy model
                "total_documents": len(documents),
            }
        }
    
    def validate_export(self, exported_data: Dict[str, Any]) -> bool:
        """
        Validate exported data integrity.
        
        Args:
            exported_data: Exported data from export_to_ragflow_format()
            
        Returns:
            bool: True if validation passes
        """
        try:
            # Check required fields
            required_fields = ["collection_info", "documents", "migration_metadata"]
            for field in required_fields:
                if field not in exported_data:
                    rprint(f"[red]❌ Missing required field: {field}[/red]")
                    return False
            
            # Validate document count
            expected_count = exported_data["collection_info"]["points_count"]
            actual_count = len(exported_data["documents"])
            
            if expected_count != actual_count:
                rprint(f"[red]❌ Document count mismatch: expected {expected_count}, got {actual_count}[/red]")
                return False
            
            # Check document structure
            for i, doc in enumerate(exported_data["documents"][:5]):  # Sample first 5
                required_doc_fields = ["id", "content", "metadata", "legacy_vector"]
                for field in required_doc_fields:
                    if field not in doc:
                        rprint(f"[red]❌ Document {i} missing field: {field}[/red]")
                        return False
            
            rprint("[green]✅ Export validation passed.[/green]")
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            rprint(f"[red]❌ Validation error: {e}[/red]")
            return False
    
    def cleanup_after_migration(self) -> bool:
        """
        Clean up Qdrant data after successful migration.
        Use with caution - this will delete the collection.
        
        Returns:
            bool: True if cleanup successful
        """
        if not self.client or not self.collection_exists():
            rprint("[yellow]⚠️ No collection to clean up.[/yellow]")
            return True
        
        try:
            # Ask for confirmation
            rprint("[yellow]⚠️ This will permanently delete the Qdrant collection.[/yellow]")
            confirmation = input("Type 'DELETE' to confirm: ")
            
            if confirmation != "DELETE":
                rprint("[cyan]❌ Cleanup cancelled.[/cyan]")
                return False
            
            self.client.delete_collection(self.collection_name)
            rprint(f"[green]✅ Collection '{self.collection_name}' deleted.[/green]")
            logger.info(f"Successfully deleted collection: {self.collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            rprint(f"[red]❌ Cleanup error: {e}[/red]")
            return False


def connect_to_qdrant() -> QdrantClient:
    """
    Legacy function for backward compatibility.
    
    Returns:
        QdrantClient: Connected Qdrant client
        
    Raises:
        RuntimeError: If connection fails
    """
    service = LegacyQdrantService()
    if service.client:
        return service.client
    else:
        raise RuntimeError("Failed to connect to Qdrant")


if __name__ == "__main__":
    """Test suite for legacy Qdrant service."""
    rprint("[bold cyan]🧪 Running Legacy Qdrant Service Test Suite...[/bold cyan]")
    
    try:
        # Test 1: Connection
        rprint("\n[b]Test 1: Connection[/b]")
        service = LegacyQdrantService()
        rprint(f"Connected: {service.is_connected()}")
        
        # Test 2: Collection info
        rprint("\n[b]Test 2: Collection info[/b]")
        collection_exists = service.collection_exists()
        rprint(f"Collection exists: {collection_exists}")
        
        if collection_exists:
            info = service.get_collection_info()
            rprint(f"Collection info: {info}")
            
            # Test 3: Export sample
            rprint("\n[b]Test 3: Export sample (first 5 points)[/b]")
            sample_points = service.export_all_points(batch_size=5)
            rprint(f"Sample points: {len(sample_points)}")
            
            # Test 4: RAGFlow format export
            rprint("\n[b]Test 4: RAGFlow format export[/b]")
            ragflow_data = service.export_to_ragflow_format()
            rprint(f"RAGFlow export keys: {list(ragflow_data.keys())}")
            
            # Test 5: Validation
            rprint("\n[b]Test 5: Export validation[/b]")
            is_valid = service.validate_export(ragflow_data)
            rprint(f"Validation passed: {is_valid}")
        
        # Test 6: Legacy function
        rprint("\n[b]Test 6: Legacy function[/b]")
        legacy_client = connect_to_qdrant()
        rprint(f"Legacy client: {type(legacy_client)}")
        
    except Exception as e:
        rprint(f"[red]❌ Test failed: {e}[/red]")
    
    rprint("\n[bold cyan]✅ Legacy Qdrant Service Test Suite Complete.[/bold cyan]") 