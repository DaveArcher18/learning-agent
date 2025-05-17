# LearningAgent: Build Your Own Local RAG Assistant (LangChain ✕ Qwen ✕ Qdrant)

> **Purpose of this file**  
> Act as a full **tutorial / README** so that anyone—including future‑you—​can reproduce, understand, and extend this project.  Each section explains *why* a choice was made **before** showing *how* to implement it.

---

## 0 · Why a Local‑First RAG?

| Reason | Explanation |
|--------|-------------|
| **Privacy** | All embeddings & LLM calls stay on your machine (no data leaves your laptop). |
| **Cost‑free** | Every component (Ollama, Qdrant, FastEmbed, Exa free tier) can be used with **\$0** recurring cost. |
| **Re‑producible tutorial** | Readers can clone the repo and follow deterministic steps without paid APIs. |
| **Hackability** | Full control of the vector DB, chunking strategy, and model weights. |

---

## 1 · Toolchain at a Glance

| Layer | Tool | Why we chose it |
|-------|------|----------------|
| LLM | **Qwen‑3 4B** via **Ollama** | 32 k token context, Apache‑2 license, runs on Mac M1/M2 CPUs fast enough for dev. |
| Vector DB | **Qdrant (embedded)** | Outstanding similarity search, hybrid BM25 + dense, single `pip` install or Docker. |
| Embeddings | **FastEmbed + FlagEmbedding** | ONNX‑optimised ⇒ 4‑10× faster on CPU vs HuggingFace PyTorch models. |
| Orchestration | LangChain | Quick plumbing for loaders, splitters, retrievers, and agents. |
| Web Search | **Exa Search MCP** | AI‑native search API; free credits; returns cleaned full‑text ⇒ minimal scraping code. |
| (Opt.) Scraping | Playwright MCP | JS‑heavy pages fallback; keep optional to stay lightweight. |

---

## 2 · Installation Checklist (Step‑by‑Step)

> **Tip** – copy‑paste the code blocks in order.  Each step is idempotent.

```bash
# 2.1  Create & activate environment
conda create -n learning_agent python=3.10 -y
conda activate learning_agent

# 2.2  Fast package installs via UV
pip install uv  # First time only
uv pip install \
  langchain langchain-qdrant langchain-exa langchain-ollama \
  qdrant-client fastembed pypdf pymupdf rich python-dotenv

# 2.3  Install & pull Qwen‑4B via Ollama
brew install ollama            # macOS; use installer on Windows/Linux
ollama pull qwen3:4b           # Downloads ~2.6 GB quantized model

# 2.4  Run Qdrant (embedded) first time only (creates ./qdrant_data)
qdrant --uri sqlite://./qdrant_data  # or docker run … if you prefer

# 2.5  Set your Exa key (get one at exa.ai → account)
export EXA_API_KEY="sk‑your‑exa‑key"
```

---

## 3 · Project Structure

```
learning-agent/
├─ ingest.py          # one‑off script: ingest local docs → Qdrant
├─ learning_agent.py  # interactive CLI loop
├─ config.yaml        # user‑editable knobs (top_k, thresholds, etc.)
├─ requirements.txt   # locked deps (optional, uv handles versions)
└─ README.md          # generated from this document
```

---

## 4 · Ingestion Pipeline

### 4.1  Load Documents
```python
from pathlib import Path
from langchain.document_loaders import PyPDFLoader, TextLoader

def load_files(path: str):
    path = Path(path)
    docs = []
    for file in path.rglob("*"):
        if file.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
        elif file.suffix.lower() in {".md", ".txt", ".json"}:
            docs.extend(TextLoader(str(file)).load())
    return docs
```

### 4.2  Token‑Based Chunking  
> **Why 2000 tokens?** – Qwen supports 32 k tokens, so 2 k strikes a balance: large enough for context, small enough for accurate retrieval. 200‑token overlap preserves continuity.

```python
from langchain.text_splitter import TokenTextSplitter
splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=200, model_name="qwen")
chunks = splitter.split_documents(raw_docs)
```

### 4.3  CPU‑Efficient Embeddings with FastEmbed
```python
from fastembed import FlagEmbedding

embedder = FlagEmbedding("BAAI/bge-small-en-v1.5")  # blazing fast CPU encoder
vectors = [embedder.embed(doc.page_content) for doc in chunks]
```

### 4.4  Store in Qdrant (& Create Collection if missing)
```python
from qdrant_client import QdrantClient, models as qmodels
client = QdrantClient(path="./qdrant_data")

if "kb" not in [c.name for c in client.get_collections().collections]:
    client.create_collection("kb", qmodels.VectorParams(size=embedder.embedding_size, distance=qmodels.Distance.COSINE))

client.upsert("kb", vectors=vectors, payload=[doc.metadata for doc in chunks])
```

> **Motivation** – Keeping collection name short (`kb`) simplifies CLI flags.

---

## 5 · Query Pipeline

1. **Retrieve from Qdrant (Hybrid mode)**
```python
from langchain_qdrant import QdrantVectorStore, RetrievalMode
vector_store = QdrantVectorStore(client, "kb", embedder, retrieval_mode=RetrievalMode.HYBRID)
retriever = vector_store.as_retriever(search_kwargs={"k": config["top_k"]})
```
2. **Optional Multi‑Query Expansion**
```python
from langchain.retrievers.multi_query import MultiQueryRetriever
multi_retriever = MultiQueryRetriever.from_llm(vector_store, llm=qwen_llm)
```
3. **Conditional Web Fallback (Exa MCP)**  – if `retriever.invoke()` returns empty.
4. **Assemble prompt → ask Qwen**.

---

## 6 · CLI Loop (learning_agent.py)
```
> ingest docs or ask questions interactively

Commands:
  :exit        quit
  :ingest PATH ingest new docs on the fly
  :config      show current RAG params
  :memory off  toggle conversation memory
```

---

## 7 · Configuration File (`config.yaml`)
```yaml
model: qwen3:4b
use_memory: true
embedding_model: fastembed-bge-small-en
top_k: 5
similarity_threshold: 0.5
chunk_size: 2000
chunk_overlap: 200
```
Users edit this instead of code. CLI flags override config.

---

## 8 · Advanced RAG Techniques (Motivations & How‑Tos)

| Technique | Motivation | 10‑second Implementation |
|-----------|------------|---------------------------|
| Hybrid Search | Combine dense + BM25 for better recall | `RetrievalMode.HYBRID` in `QdrantVectorStore` |
| Multi‑Query | Query expansion for higher coverage | `MultiQueryRetriever.from_llm(...)` |
| Metadata Filtering | Narrow results by file, date, tag | Ensure metadata stored → use `SelfQueryRetriever` |

> These three give the highest ROI for accuracy without leaving the local stack.

---

## 9 · Next Steps
- [ ] Write `ingest.py` script (use code in §4).
- [ ] Implement CLI loop in `learning_agent.py` (use §6 logic).
- [ ] Test end‑to‑end with sample PDFs.
- [ ] Add README badges + GIF demo.

Happy hacking! 🚀

# LearningAgent Simplified: Changes and Improvements

## Major Improvements

### 1. Collection Name Consistency

The system now consistently reads the collection name from `config.yaml` across all files:
- `learning_agent.py`
- `ingest.py`
- `setup_qdrant.py`
- `audit_qdrant.py`

This ensures that all components operate on the same collection, preventing sync issues.

### 2. Retrieval Fix

The main retrieval issue was fixed by ensuring documents are properly stored with their content:
- Documents are now correctly stored with `page_content` in the payload
- Proper embedding of content with consistent vector dimensions
- Fixed collection creation and management
- Better error handling during document ingestion

### 3. Simplified Code Structure

The codebase has been significantly simplified:
- Removed redundant code and unnecessary complexity
- Streamlined the chat agent functionality
- Consistent error messages and user feedback
- Clear separation of concerns between components
- Better command interface in the chat agent

### 4. Improved Memory Handling

Memory has been simplified but remains functional:
- Straightforward toggle for memory on/off
- Simple ChatMessageHistory implementation
- No unnecessary complexity in memory management

### 5. Streamlined Configuration

All configuration is now centralized in `config.yaml`:
- Model settings (provider, model name, temperature)
- Retrieval settings (top_k, similarity threshold)
- Document chunking settings
- Collection name and embedding model
- Memory and web search settings

## Usage Simplification

### Easier Getting Started

The startup process is now simpler:
1. Install dependencies with `pip install -r requirements.txt`
2. Configure settings in `config.yaml`
3. Start Qdrant with `make start_qdrant`
4. Ingest documents with `python ingest.py --path ./docs`
5. Run the agent with `python learning_agent.py`

### Clearer Commands

Available commands in the chat interface:
- `:memory on/off` - Toggle conversation memory
- `:search <query>` - Search the web for information
- `:provider ollama/openrouter` - Switch LLM provider
- `:config` - Show current configuration
- `:help` - Show available commands
- `:exit` - Exit the chat

## Technical Details

### Simplified Vector Storage

- Direct use of `fastembed.TextEmbedding` with cleaner interface
- Proper chunking of documents with `TokenTextSplitter`
- Consistent embedding dimensions and storage format
- Batched insertion for large document collections

### Improved Retrieval Chain

- Simple but effective retrieval using vector similarity
- Content properly formatted and presented to the LLM
- Better handling of cases with no documents
- Fallback to direct LLM queries when appropriate

### Better Error Handling

- Graceful fallbacks when services are unavailable
- Clear error messages when things go wrong
- Helpful suggestions for fixing common issues
- Audit functionality to inspect the database

