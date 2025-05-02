# LearningAgent: Build Your Own Local RAG Assistant

> A privacy-focused RAG system using LangChain, Qwen, and Qdrant that runs entirely on your local machine.

## Why a Local-First RAG?

| Reason | Explanation |
|--------|-------------|
| **Privacy** | All embeddings & LLM calls stay on your machine (no data leaves your laptop). |
| **Cost-free** | Every component (Ollama, Qdrant, FastEmbed, Exa free tier) can be used with **$0** recurring cost. |
| **Reproducible tutorial** | Clone the repo and follow deterministic steps without paid APIs. |
| **Hackability** | Full control of the vector DB, chunking strategy, and model weights. |

## Toolchain at a Glance

| Layer | Tool | Why we chose it |
|-------|------|----------------|
| LLM | **Qwen-3 4B** via **Ollama** | 32k token context, Apache-2 license, runs on Mac M1/M2 CPUs fast enough for dev. |
| Vector DB | **Qdrant (embedded)** | Outstanding similarity search, hybrid BM25 + dense, single `pip` install or Docker. |
| Embeddings | **FastEmbed + FlagEmbedding** | ONNX-optimized — 4-10× faster on CPU vs HuggingFace PyTorch models. |
| Orchestration | LangChain | Quick plumbing for loaders, splitters, retrievers, and agents. |
| Web Search | **Exa Search MCP** | AI-native search API; free credits; returns cleaned full-text → minimal scraping code. |

## Installation Checklist

```bash
# Create & activate environment
conda create -n learning_agent python=3.10 -y
conda activate learning_agent

# Fast package installs via UV
pip install uv  # First time only
uv pip install \
  langchain langchain-qdrant langchain-exa langchain-ollama \
  qdrant-client fastembed pypdf pymupdf rich python-dotenv

# Install & pull Qwen-4B via Ollama
brew install ollama            # macOS; use installer on Windows/Linux
ollama pull qwen3:4b           # Downloads ~2.6 GB quantized model

# Set your Exa key (get one at exa.ai → account)
export EXA_API_KEY="sk-your-exa-key"
```

## Quick Start with Make

```bash
make setup_db      # Create Qdrant collection if missing
make ingest        # Load documents from ./docs into vector DB
make run           # Start the CLI assistant
```

Or use Docker to manage Qdrant:

```bash
make start_qdrant  # Start Qdrant in Docker
make stop_qdrant   # Stop the Qdrant container
```

## Usage

### Document Ingestion

```bash
python ingest.py --path ./docs               # ingest all supported files under ./docs
python ingest.py --path ./docs/my.pdf        # ingest a single file
python ingest.py --path ./docs --rebuild     # wipe & rebuild the collection
```

### Running the Agent

```bash
python learning_agent.py           # start chat with web search fallback
python learning_agent.py --no-web  # disable web search
python learning_agent.py --no-memory # disable conversation memory
```

## CLI Commands

Once the agent is running:

```
> ingest docs or ask questions interactively

Commands:
  :exit             quit the application
  :ingest PATH      ingest new docs on the fly
  :search TOPIC     search the web on a topic and store results
  :config           show current RAG params
  :memory on/off    toggle conversation memory
```

## Advanced RAG Techniques

| Technique | Motivation | Implementation |
|-----------|------------|----------------|
| Hybrid Search | Combine dense + BM25 for better recall | `RetrievalMode.HYBRID` in `QdrantVectorStore` |
| Multi-Query | Query expansion for higher coverage | `MultiQueryRetriever.from_llm(...)` |
| Metadata Filtering | Narrow results by file, date, tag | Ensure metadata stored → use `SelfQueryRetriever` |

## Project Structure

```
learning-agent/
├─ ingest.py          # one-off script: ingest local docs → Qdrant
├─ learning_agent.py  # interactive CLI loop
├─ config.yaml        # user-editable knobs (top_k, thresholds, etc.)
├─ requirements.txt   # locked deps (optional, uv handles versions)
└─ README.md          # you are here
```

## License

Apache 2.0
