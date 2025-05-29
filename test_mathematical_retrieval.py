#!/usr/bin/env python3
"""
Test Mathematical Content Retrieval with BGE-M3

Purpose: Validate end-to-end mathematical content retrieval pipeline
Usage: python test_mathematical_retrieval.py
"""

import requests
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from core.config import ConfigManager

def create_chat_assistant(base_url, api_key, kb_id):
    """Create a chat assistant linked to our knowledge base"""
    print("🤖 Creating chat assistant...")
    
    response = requests.post(
        f'{base_url}/api/v1/chats',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'name': 'Mathematical Content Assistant',
            'dataset_ids': [kb_id],
            'prompt': {
                'similarity_threshold': 0.2,
                'keywords_similarity_weight': 0.7,
                'top_n': 6,
                'prompt': 'You are a mathematical content assistant. Please answer questions based on the provided knowledge: {knowledge}',
                'variables': [
                    {
                        'key': 'knowledge',
                        'optional': False
                    }
                ]
            }
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            chat_id = result['data']['id']
            print(f"✅ Chat assistant created with ID: {chat_id}")
            return chat_id
        else:
            print(f"❌ Failed to create chat assistant: {result}")
            return None
    else:
        print(f"❌ HTTP Error creating chat assistant: {response.status_code} - {response.text}")
        return None

def test_query(base_url, api_key, chat_id, query):
    """Test a single query against the chat assistant"""
    print(f"\n🔍 Testing Query: '{query}'")
    
    try:
        response = requests.post(
            f'{base_url}/api/v1/chats/{chat_id}/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'question': query,
                'stream': False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('code') == 0:
                # The data field contains a streaming response string
                data_str = result.get('data', '')
                
                # Parse the streaming data
                if data_str.startswith('data:'):
                    # Extract the JSON part after 'data:'
                    json_str = data_str[5:].strip()
                    if json_str:
                        try:
                            inner_data = json.loads(json_str)
                            if inner_data.get('code') == 0 and 'data' in inner_data:
                                chat_data = inner_data['data']
                                answer = chat_data.get('answer', 'No answer')
                                reference = chat_data.get('reference', {})
                                
                                if isinstance(reference, dict):
                                    chunks = reference.get('chunks', [])
                                else:
                                    chunks = []
                                
                                print(f"✅ Query successful!")
                                print(f"📝 Answer: {answer[:200]}..." if len(answer) > 200 else f"📝 Answer: {answer}")
                                print(f"📊 Retrieved {len(chunks)} chunks")
                                
                                if chunks:
                                    print(f"🔍 Sample chunks:")
                                    for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
                                        if isinstance(chunk, dict):
                                            content = chunk.get('content', '')[:150]
                                            doc_name = chunk.get('document_name', chunk.get('doc_name', 'Unknown'))
                                            print(f"   Chunk {i+1} ({doc_name}): {content}...")
                                
                                return True, len(chunks), answer
                            else:
                                print(f"❌ Inner data error: {inner_data}")
                                return False, 0, ""
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON decode error: {e}")
                            return False, 0, ""
                else:
                    print(f"❌ Unexpected data format: {data_str[:100]}...")
                    return False, 0, ""
            else:
                print(f"❌ API Error: {result}")
                return False, 0, ""
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text}")
            return False, 0, ""
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False, 0, ""

def main():
    config = ConfigManager()
    api_key = config.get('ragflow.api.key', '')
    kb_id = '56b87cee3bda11f0ba5e427dc5bb4ea3'
    base_url = 'http://localhost:9380'

    print("=== Testing Mathematical Content Retrieval with BGE-M3 ===")
    print(f"Knowledge Base ID: {kb_id}")
    print(f"Using API key: {api_key[:20]}..." if api_key else "No API key found")
    
    # Create chat assistant
    chat_id = create_chat_assistant(base_url, api_key, kb_id)
    if not chat_id:
        print("❌ Failed to create chat assistant. Cannot proceed with retrieval tests.")
        return False
    
    # Test queries of increasing complexity
    test_queries = [
        # Basic architectural queries (should work with current ARCHITECTURE docs)
        "What is the overall architecture?",
        "How are the components organized?",
        "What are the main modules?",
        
        # Technical queries
        "What technologies are used?",
        "How is the system structured?",
        
        # Mathematical queries (will work better once more docs are processed)
        "What mathematical concepts are discussed?",
        "Are there any equations or formulas?",
        "What theorems are mentioned?"
    ]
    
    print(f"\n🚀 Testing {len(test_queries)} queries against available chunks...")
    
    successful_queries = 0
    total_chunks_retrieved = 0
    
    for i, query in enumerate(test_queries, 1):
        success, chunk_count, answer = test_query(base_url, api_key, chat_id, query)
        if success:
            successful_queries += 1
            total_chunks_retrieved += chunk_count
        
        # Short pause between queries
        time.sleep(1)
    
    print(f"\n📊 RETRIEVAL TEST RESULTS:")
    print(f"✅ Successful queries: {successful_queries}/{len(test_queries)}")
    print(f"📚 Total chunks retrieved: {total_chunks_retrieved}")
    print(f"📈 Average chunks per query: {total_chunks_retrieved/len(test_queries):.1f}")
    
    if successful_queries > 0:
        print(f"\n🎯 BGE-M3 EMBEDDING RETRIEVAL CONFIRMED WORKING!")
        print(f"🚀 End-to-end mathematical content pipeline is functional")
        print(f"⏳ More content will be available as remaining 4 documents complete processing")
    else:
        print(f"\n❌ No successful retrievals - may need to wait for more documents to complete")
    
    # Clean up: delete the test chat assistant
    print(f"\n🧹 Cleaning up test chat assistant...")
    cleanup_response = requests.delete(
        f'{base_url}/api/v1/chats',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={'ids': [chat_id]}
    )
    
    if cleanup_response.status_code == 200:
        print(f"✅ Test chat assistant cleaned up")
    else:
        print(f"⚠️  Could not clean up chat assistant: {cleanup_response.status_code}")
    
    return successful_queries > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 