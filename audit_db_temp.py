from qdrant_client import QdrantClient
try:
    client = QdrantClient(host='localhost', port=6333)
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    print(f"Collections: {collection_names}")
    if "kb" in collection_names:
        collection_info = client.get_collection("kb")
        vector_count = collection_info.points_count
        print(f"Collection 'kb' contains {vector_count} vectors")
        if vector_count > 0:
            # Get a sample of points to show metadata
            points = client.scroll(
                collection_name="kb",
                limit=5,
                with_payload=True,
                with_vectors=False
            )[0]
            print(f"
Sample entries ({min(5, len(points))} of {vector_count}):")
            for i, point in enumerate(points):
                print(f"
Entry {i+1}:")
                source = point.payload.get("source", "unknown")
                print(f"  Source: {source}")
                # Show other metadata fields
                for key, value in point.payload.items():
                    if key != "source" and key != "page_content" and key != "text":
                        print(f"  {key}: {value}")
    else:
        print("Collection 'kb' not found")
except Exception as e:
    print(f"Error connecting to Qdrant: {e}")
