# LearningAgent: Simple RAG Assistant with Memory

A streamlined Retrieval-Augmented Generation (RAG) system that provides an easy-to-use chat interface with document reference capabilities.

## Key Features

- **Simple Design**: Focused core functionality without unnecessary complexity
- **Flexible Models**: Support for Ollama local models or OpenRouter cloud models
- **Configurable Collection**: Single configuration file for consistent settings
- **Long-term Memory**: Conversation history is maintained between sessions
- **Document Retrieval**: Semantic search of your knowledge base
- **Web Search Fallback**: Optional web search when answers aren't in your documents

## Quick Setup

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure**

Edit `config.yaml` to customize settings:

```yaml
# Model settings
model: qwen3:4b
model_provider: "ollama"  # Options: "ollama" or "openrouter"
openrouter_model: "deepseek/deepseek-prover-v2:free"
temperature: 0.3

# Memory
use_memory: true

# Embedding
embedding_model: BAAI/bge-small-en-v1.5

# Retrieval settings
top_k: 8
similarity_threshold: 0.5

# Chunking settings
chunk_size: 10000
chunk_overlap: 500

# Web search fallback
use_web_fallback: false
web_results: 3

# Collection name (used across all files)
collection: MoravaKTheory
```

3. **Setup Database**

```bash
# Start a local Qdrant instance (if using Docker)
make start_qdrant

# Or the script will use embedded Qdrant as fallback
python setup_qdrant.py
```

4. **Add Documents**

```bash
# Add documents from the docs folder
python ingest.py --path ./docs

# Add a specific document
python ingest.py --path /path/to/your/file.pdf
```

5. **Start Chat**

```bash
# Start the chat interface
python learning_agent.py
```

## Using the Agent

Once started, you can:

- Ask questions directly about your documents
- Use commands by typing a colon followed by the command:

```
> What does the document say about surface operations?
> :memory on             # Turn conversation memory on
> :memory off            # Turn conversation memory off
> :search quantum theory # Search the web for information
> :provider ollama       # Switch to local model
> :provider openrouter   # Switch to cloud model
> :exit                  # Quit the application
```

## Troubleshooting

### Database Issues

If retrieval isn't working properly, try these steps:

1. Check documents were ingested correctly:
```bash
python audit_qdrant.py --count 2
```

2. Rebuild the collection from scratch:
```bash
python ingest.py --path ./docs --rebuild
```

### API Keys

For web search, add EXA_API_KEY to your .env file.
For OpenRouter models, add OPENAI_API_KEY to your .env file.

## Understanding the Code

The codebase has been significantly simplified:

- **learning_agent.py**: Core chat functionality with memory and retrieval
- **ingest.py**: Document processing and storage in the vector database
- **setup_qdrant.py**: Database setup and initialization
- **audit_qdrant.py**: Database inspection and troubleshooting

All files now consistently read from config.yaml for settings, including the collection name.

## Improvements

- **Collection name consistency**: All scripts now read collection name from config.yaml
- **Document storage fix**: Documents are now stored with their content correctly preserved
- **Simplified codebase**: Removed unnecessary complexity while maintaining core functions
- **Clearer error messages**: Better feedback on what might be going wrong
- **Streamlined startup**: Faster startup with fewer dependencies

## Development Notes

- The configuration file `config.yaml` is the single source of truth for settings
- Embedding model `BAAI/bge-small-en-v1.5` provides good quality with low resource usage
- Qdrant is used for vector storage with flexible Docker or embedded options
