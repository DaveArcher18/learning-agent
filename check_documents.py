#!/usr/bin/env python3
"""
RAGFlow Document Processing Diagnostic Tool

Purpose: Check document processing status and attempt to trigger processing
Usage: python check_documents.py
Status: KEEP - Permanent diagnostic tool for troubleshooting document processing issues
"""

import requests
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from core.config import ConfigManager

def main():
    config = ConfigManager()
    api_key = config.get('ragflow.api.key', '')
    base_url = 'http://localhost:9380'
    kb_id = '56b87cee3bda11f0ba5e427dc5bb4ea3'  # mathematical_kb

    print("=== RAGFlow Document Processing Status ===")
    print(f"Checking documents in knowledge base: {kb_id}")

    # Get documents in the knowledge base
    response = requests.get(
        f'{base_url}/api/v1/datasets/{kb_id}/documents',
        headers={'Authorization': f'Bearer {api_key}'}
    )

    print(f"API Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        
        if data.get('code') == 0:
            documents = data.get('data', {}).get('docs', [])
            print(f"\n📋 Found {len(documents)} documents:")
            
            unstarted_docs = []
            processing_docs = []
            completed_docs = []
            
            for doc in documents:
                print(f"\n📄 Document: {doc.get('name')}")
                print(f"   🆔 ID: {doc.get('id')}")
                print(f"   📏 Size: {doc.get('size'):,} bytes")
                print(f"   📊 Status: {doc.get('status')}")
                print(f"   ▶️  Run State: {doc.get('run')}")
                print(f"   📈 Progress: {doc.get('progress', 0):.1f}%")
                
                progress_msg = doc.get('progress_msg', 'N/A')
                if progress_msg:
                    print(f"   💬 Progress Message: {progress_msg}")
                    
                print(f"   🧩 Chunks: {doc.get('chunk_count', 0)}")
                print(f"   🔤 Tokens: {doc.get('token_count', 0)}")
                
                # Categorize documents
                run_state = doc.get('run', '')
                if run_state == 'UNSTART':
                    unstarted_docs.append(doc)
                elif run_state in ['RUNNING', 'PROCESSING']:
                    processing_docs.append(doc)
                elif run_state == 'DONE':
                    completed_docs.append(doc)
            
            # Summary
            print(f"\n📊 Processing Summary:")
            print(f"   ✅ Completed: {len(completed_docs)}")
            print(f"   🔄 Processing: {len(processing_docs)}")
            print(f"   ⏸️  Unstarted: {len(unstarted_docs)}")
            
            # Attempt to start unstarted documents using correct API endpoint
            if unstarted_docs:
                print(f"\n🚀 Attempting to start {len(unstarted_docs)} unstarted documents...")
                
                # Collect all document IDs for batch processing
                unstarted_ids = [doc.get('id') for doc in unstarted_docs]
                
                print(f"📋 Document IDs to process: {unstarted_ids}")
                
                # Use the correct API endpoint for document processing
                start_response = requests.post(
                    f'{base_url}/api/v1/datasets/{kb_id}/chunks',
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={'document_ids': unstarted_ids}
                )
                
                print(f"Processing request status: {start_response.status_code}")
                
                if start_response.status_code == 200:
                    start_data = start_response.json()
                    if start_data.get('code') == 0:
                        print(f"   ✅ Successfully triggered batch processing for all documents")
                        print(f"   📈 Processing initiated for {len(unstarted_ids)} documents")
                    else:
                        print(f"   ❌ Processing trigger failed: {start_data}")
                else:
                    print(f"   ❌ HTTP Error: {start_response.status_code}")
                    try:
                        error_data = start_response.json()
                        print(f"   📝 Error details: {error_data}")
                    except:
                        print(f"   📝 Error text: {start_response.text}")
            else:
                print(f"\n✨ All documents have been processed or are currently processing")
                
        else:
            print(f'❌ API Error: {data}')
    else:
        print(f'❌ HTTP Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    main() 