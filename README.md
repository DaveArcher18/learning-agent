# LearningAgent: Flexible RAG Assistant with Local or Cloud LLMs

> A powerful Retrieval-Augmented Generation (RAG) system that combines document understanding with conversation capability, supporting both local and cloud models.

## Key Features

- **Dual Model Support**: Use either local Ollama models for privacy or cloud OpenRouter models for enhanced capabilities
- **Vector Search**: Powerful similarity search with Qdrant, including hybrid search capabilities
- **Web Research**: Automatic web search capabilities for up-to-date information 
- **Easy Document Import**: Simple commands to ingest documents from PDFs, text files, and more
- **Interactive Interface**: Command-line interface with conversation memory and context awareness
- **One-Click Deployment**: Simple Makefile commands to get up and running quickly

## System Requirements

- Python 3.10+ 
- Docker (recommended but optional)
- 8GB+ RAM recommended for optimal performance

## Quick Start Guide

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/learning-agent.git
cd learning-agent

# Create and activate virtual environment
conda create -n learning_agent python=3.10 -y
conda activate learning_agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
# Required for web search capabilities
EXA_API_KEY=your_exa_key_here            # Get from exa.ai

# Required for cloud models via OpenRouter
OPENAI_API_KEY=your_openrouter_key_here  # Get from openrouter.ai
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

### 3. Prepare for Launch

For **Local Models** (using Ollama):

```bash
# Install Ollama and download the model
brew install ollama            # macOS; use installer on Windows/Linux
ollama pull qwen3:4b           # Downloads ~2.6 GB model
```

For **Cloud Models** (using OpenRouter):
No additional setup needed if you've configured the `.env` file.

### 4. Run the Agent

**Single-line startup:**

```bash
# Using local models:
make run

# Using cloud models via OpenRouter:
make run_openrouter  # automatically loads .env variables
```

**Advanced startup options:**

```bash
# Start with Docker-based Qdrant (more stable):
make run_docker

# Start with specific command-line options:
python learning_agent.py --provider openrouter --openrouter-model "qwen/qwen3-235b-a22b:free"
```

## Using the LearningAgent

### Adding Your Documents

```bash
# Ingest files from ./docs directory:
make ingest

# Ingest a specific document:
python ingest.py --path /path/to/your/document.pdf

# Rebuild the database from scratch:
python ingest.py --path ./docs --rebuild
```

### Interacting with the Agent

Once the agent is running, you can use these commands:

```
> What are the key themes in the document I uploaded?         # Ask questions about your documents

Commands:
:search climate change                                        # Run web search and store results
:search_kb renewable energy                                   # Search knowledge base directly
:ingest ~/Documents/important_file.pdf                        # Import new document on the fly
:provider openrouter qwen/qwen3-235b-a22b:free                # Switch to a specific cloud model
:provider ollama                                              # Switch to local model
:memory on                                                    # Turn on conversation memory
:debug on                                                     # Enable detailed debug information
:config                                                       # Show current settings
:exit                                                         # Quit the application
```

### Example Interaction

```
> :ingest ./docs/climate_report.pdf
📚 Ingesting documents from ./docs/climate_report.pdf...
✅ Added 23 chunks to vector database

> What are the main findings of the climate report?
🔍 Searching knowledge base...
✅ Found 5 relevant documents

The main findings of the climate report include:
1. Global temperatures have risen by 1.1°C since pre-industrial times [Source: climate_report.pdf, page 7]
2. Climate-related impacts are accelerating, with more frequent extreme weather events [Source: climate_report.pdf, page 12]
...

> :search latest climate data 2023
🔍 Web search for: latest climate data 2023
✅ Retrieved information from the web

According to the latest data from 2023, the year was the hottest on record globally...
```

## Database Management

The LearningAgent uses Qdrant vector database to store and retrieve document chunks.

```bash
# Check database status:
make audit_db

# Clear all data from the database:
make clear_db

# Start/stop the Qdrant database:
make start_qdrant
make stop_qdrant
```

## Understanding the Architecture

### Component Integration

LearningAgent combines multiple components:

1. **Document Processing**: 
   - Converts documents to text using PyPDF/PyMuPDF
   - Splits text into chunks with context-aware overlap

2. **Vector Embedding**:
   - Converts text chunks to vector embeddings using FastEmbed
   - Optimized for CPU performance with ONNX runtime

3. **Vector Database**:
   - Stores embeddings in Qdrant for fast similarity search
   - Supports hybrid search with BM25 text matching

4. **LLM Integration**:
   - Local: Uses Ollama with quantized models (Qwen3)
   - Cloud: Connects to OpenRouter for various hosted models

5. **Web Research**:
   - Uses Exa API for high-quality web search capabilities
   - Stores web search results in vector database for future reference

### Customization

The application can be customized through `config.yaml`:

```yaml
# LLM settings
model_provider: "openrouter"  # "ollama" or "openrouter"
openrouter_model: "qwen/qwen3-235b-a22b:free"  # only for OpenRouter
temperature: 0.3

# Retrieval settings
top_k: 5  # Number of chunks to retrieve
similarity_threshold: 0.5  # Minimum similarity score
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file contains the correct API keys
- Load the keys into your environment with `source ./export_env.sh` or export them manually
- If authentication fails, try this sequence:
  ```bash
  make export_env
  source ./export_env.sh
  make run_openrouter
  ```
- Check the key's status by running with `--debug` flag

### OpenRouter Connection Issues
- Verify your OpenRouter API key is correct and activated
- Try running `export OPENAI_API_KEY=your_key && python learning_agent.py --provider openrouter`
- If still failing, try a different model with `--openrouter-model "qwen/qwen3-235b-a22b:free"`

### Qdrant Database Issues
- Make sure Docker is running if using `make run_docker` or `make run_openrouter`
- Try `make clear_db` followed by `make setup_db` to reset the database
- Run `make audit_db` to check the state of your database

### Common Error Messages

**Authentication Error**:
```
OpenRouter authentication failed: Error code: 401
```
Fix: Check your `.env` file or run `source ./export_env.sh`

**Document Processing Error**:
```
Error ingesting documents: PyPDF Error
```
Fix: Make sure the document is valid and not password-protected

## Development

### Project Structure

```
learning-agent/
├── docs/                  # Place your documents here
├── learning_agent.py      # Main application logic
├── ingest.py              # Document ingestion logic
├── setup_qdrant.py        # Database setup script
├── config.yaml            # Configuration settings
├── export_env.sh          # Environment variable helper
├── requirements.txt       # Python dependencies
└── Makefile               # Convenient commands
```

### Adding Support for New Document Types

To support a new document format, edit `ingest.py` to add a new document loader:

```python
# Example for adding DOCX support
if file_path.suffix.lower() == '.docx':
    from langchain_community.document_loaders import Docx2txtLoader
    return Docx2txtLoader(str(file_path))
```

## License

Apache 2.0

## Acknowledgments

- This project uses [LangChain](https://github.com/langchain-ai/langchain) for orchestration
- Vector search powered by [Qdrant](https://github.com/qdrant/qdrant)
- Local models provided by [Ollama](https://github.com/ollama/ollama)
- Cloud models provided by [OpenRouter](https://openrouter.ai)
- Web search capabilities by [Exa](https://exa.ai)
