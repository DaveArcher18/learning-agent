# Setup Roadmap for RAG-Enabled Knowledge Consuming Agent

This guide describes in detail how to set up a local Retrieval-Augmented Generation (RAG) agent that integrates web searches and persists information in a Qdrant vector database.

---

## Step 1: Environment Setup (Conda and Python)

- **Install Conda** from [Anaconda's official website](https://www.anaconda.com/products/individual).
- Create a new Conda environment with Python 3.10:

```bash
conda create -n langchain_openrouter python=3.10
conda activate langchain_openrouter
```

## Step 2: Faster Package Installation with UV

- Install the fast Python package manager `uv`:

```bash
pip install uv
```

- Install essential packages quickly using `uv`:

```bash
uv pip install langchain langchain-community langchain-qdrant langchain-openai langchain-huggingface openai exa-py python-dotenv rich transformers sentence-transformers qdrant-client
```

---

## Step 3: Docker and Qdrant Setup

### 3.1 Docker Installation (Mac M1/M2)

- Install Docker Desktop for Apple Silicon:
  - [Docker Desktop Download](https://www.docker.com/products/docker-desktop/)
  - Drag to your Applications folder, launch it, and wait for the Docker daemon to start.

**Or** use lightweight **Colima** if preferred:

```bash
brew install colima
colima start --cpu 2 --memory 4
```

### 3.2 Qdrant Vector Database

- Pull and run Qdrant using Docker with persistent storage:

```bash
docker volume create qdrant_research_agent
docker run -d --name qdrant_research \
  -p 6333:6333 \
  -v qdrant_research_agent:/qdrant/storage \
  qdrant/qdrant
```

- Verify Qdrant is running by visiting:
  - [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## Step 4: Set Up Environment Variables

- Create a `.env` file in your project directory containing your API keys:

```env
EXA_API_KEY=your_exa_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

- Load these in your Python script:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Step 5: Embeddings Setup

- Use HuggingFace's `all-MiniLM-L6-v2` for free local embeddings without external APIs:

```python
from langchain_huggingface import HuggingFaceEmbeddings
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

---

## Step 6: Integrating Qdrant and LangChain for RAG

- Initialize the Qdrant client and vector store in your script:

```python
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

client = QdrantClient(url="http://localhost:6333")

# Ensure the collection exists
from qdrant_client.http import models as qmodels
if not any(c.name == "research_snippets" for c in client.get_collections().collections):
    client.create_collection(
        collection_name="research_snippets",
        vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE)
    )

vectordb = QdrantVectorStore(client=client, collection_name="research_snippets", embedding=hf_embeddings)
```

---

## Step 7: Implementing the Agent (LangChain + OpenRouter + Exa)

- Use OpenRouter and Exa.ai for retrieving detailed web search information:
  - Setup your LLM using OpenRouter via `ChatOpenAI` class.
  - Perform enriched web searches via Exa.ai API.
  - Embed and store search results into Qdrant.

- Implement prompt chains using `RunnableSequence`:

```python
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="meta-llama/llama-4-maverick:free")

qa_prompt = PromptTemplate(input_variables=["research", "question"], template="...")
qa_chain = RunnableSequence(qa_prompt, llm)
```

---

## Step 8: Efficient Context Handling and Truncation

- Control the retrieval size (`k`) and truncate context length to avoid exceeding LLM context window limits:

```python
search_kwargs = {"k": 3}
MAX_CONTEXT_CHARS = 600000  # ~150k tokens

# Retrieval and truncation logic
context = "\n\n".join([doc.page_content for doc in docs])
if len(context) > MAX_CONTEXT_CHARS:
    context = context[:MAX_CONTEXT_CHARS] + "\n\n...[truncated]..."
```

---

## Step 9: Terminal UI using Rich

- Use Rich library to display attractive, informative output:

```python
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel.fit("Your output here", title="Agent", border_style="green"))
```

---

## Step 10: Convenience with Makefile

- Create a `Makefile` to quickly launch the database and agent:

```makefile
.PHONY: start_qdrant stop_qdrant agent run

start_qdrant:
	docker run -d --name qdrant_research \
	-p 6333:6333 \
	-v qdrant_research_agent:/qdrant/storage \
	qdrant/qdrant

stop_qdrant:
	-docker stop qdrant_research
	-docker rm qdrant_research

agent:
	python research_agent.py

run: start_qdrant agent
```

---

## 🚀 You Are Now Set!

With this setup, you have a powerful local RAG-enabled agent capable of persistent research storage and retrieval directly from web search outputs. Enjoy experimenting and expanding your knowledge!
