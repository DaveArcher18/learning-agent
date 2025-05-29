#!/usr/bin/env python3
"""
Trigger Document Processing with New Embedding Model

Purpose: Trigger fresh document processing after updating embedding model
Usage: python trigger_processing.py
"""

import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from core.config import ConfigManager

def verify_ragflow():
    """Verify RAGFlow is responding and check embedding model configuration"""
    print("🔍 Verifying RAGFlow status...")
    try:
        # Check if RAGFlow is responding
        response = requests.get('http://localhost:9380/api/v1/datasets', timeout=10)
        if response.status_code in [200, 401]:  # 401 is fine, means server is up but needs auth
            print("✅ RAGFlow is responding")
            return True
        else:
            print(f"❌ RAGFlow returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ CRITICAL ERROR: RAGFlow is not responding: {e}")
        return False

def main():
    config = ConfigManager()
    api_key = config.get('ragflow.api.key', '')
    kb_id = '56b87cee3bda11f0ba5e427dc5bb4ea3'
    base_url = 'http://localhost:9380'

    print("=== Triggering Document Processing with BGE-M3 ===")
    print(f"Knowledge Base ID: {kb_id}")
    print(f"Using API key: {api_key[:20]}..." if api_key else "No API key found")
    
    # Verify RAGFlow is operational
    if not verify_ragflow():
        print("\n❌ CRITICAL FAILURE: Cannot proceed without RAGFlow!")
        print("🔧 Please check RAGFlow status manually:")
        print("   docker ps | grep ragflow")
        print("   curl http://localhost:9380/api/v1/datasets")
        sys.exit(1)

    # Get document IDs
    print("📄 Fetching document list...")
    response = requests.get(
        f'{base_url}/api/v1/datasets/{kb_id}/documents',
        headers={'Authorization': f'Bearer {api_key}'}
    )

    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 0:
            # Access docs through data.docs
            docs_data = data.get('data', {})
            docs = docs_data.get('docs', [])
            
            print(f"Found {len(docs)} documents")
            
            if docs:
                doc_ids = [doc['id'] for doc in docs]
                print(f"Document IDs: {doc_ids[:3]}..." if len(doc_ids) > 3 else f"Document IDs: {doc_ids}")
                
                # Trigger processing with BGE-M3 embedding model
                print("🚀 Triggering document processing with BGE-M3...")
                process_response = requests.post(
                    f'{base_url}/api/v1/datasets/{kb_id}/chunks',
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={'document_ids': doc_ids}
                )
                
                print(f'Processing trigger status: {process_response.status_code}')
                if process_response.status_code == 200:
                    result = process_response.json()
                    print(f'✅ Processing triggered successfully!')
                    print(f'📄 Processing {len(doc_ids)} documents with BGE-M3 embedding model')
                    print("⏳ Monitor progress with: python check_documents.py")
                    print("\n🎯 Expected: No more 'NoneType' encoding errors!")
                    print("📊 The database configuration should now use bge-m3@Ollama")
                else:
                    print(f'❌ Processing trigger failed: {process_response.text}')
                    sys.exit(1)
            else:
                print('❌ No documents found to process')
                sys.exit(1)
        else:
            print(f'❌ API Error: {data}')
            sys.exit(1)
    else:
        print(f'❌ Failed to get documents: {response.status_code} - {response.text}')
        sys.exit(1)

if __name__ == "__main__":
    main() 