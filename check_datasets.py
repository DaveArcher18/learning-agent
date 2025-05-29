#!/usr/bin/env python3
"""
RAGFlow Knowledge Base Diagnostic Tool

Purpose: Check knowledge base configuration and status
Usage: python check_datasets.py
Status: KEEP - Permanent diagnostic tool for troubleshooting
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

    print("=== RAGFlow Knowledge Base Status ===")
    print(f"Using API key: {api_key[:20]}..." if api_key else "No API key found")

    # Get datasets
    response = requests.get(
        f'{base_url}/api/v1/datasets',
        headers={'Authorization': f'Bearer {api_key}'}
    )

    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        
        if data.get('code') == 0:
            datasets = data.get('data', [])
            print(f"\nFound {len(datasets)} knowledge bases:")
            
            for ds in datasets:
                print(f'\n📚 Dataset: {ds.get("name")} (ID: {ds.get("id")})')
                print(f'   📄 Documents: {ds.get("document_count", 0)}')
                print(f'   🧩 Chunks: {ds.get("chunk_count", 0)}')
                print(f'   🤖 Embedding Model: {ds.get("embedding_model", "Not assigned")}')
                print(f'   📊 Status: {ds.get("status", "unknown")}')
                print(f'   🏗️  Parser Config: {ds.get("parser_config", {}).get("chunk_token_num", "default")} token chunks')
                
                # Health assessment
                if ds.get("chunk_count", 0) > 0:
                    print(f'   ✅ Health: Operational (documents processed)')
                elif ds.get("document_count", 0) > 0:
                    print(f'   ⚠️  Health: Documents uploaded but not processed')
                else:
                    print(f'   📭 Health: Empty knowledge base')
        else:
            print(f'❌ API Error: {data}')
    else:
        print(f'❌ HTTP Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    main() 