# Upgrade Plan: Integrating **RAGFlow** into *learning‑agent*

## 0️⃣ Executive Summary

Integrate InfiniFlow’s **RAGFlow** as the primary Retrieval‑Augmented Generation (RAG) engine for *learning‑agent* while **retaining a 100 % local/zero‑cost workflow**.
Key outcomes:

* Layout‑aware ingestion (OCR, tables, figures) → higher‑precision retrieval.
* Automatic, granular citations → traceable answers.
* Pluggable retriever factory → instant A/B swap between **RAGFlow** and existing **Qdrant** pipeline.

---

## 1️⃣ Current State Snapshot

| Layer            | Tech                                             | Location                   |
| ---------------- | ------------------------------------------------ | -------------------------- |
| **Ingestion**    | naïve splitter + `bge-small-en` embeddings       | `ingest.py`, `config.yaml` |
| **Vector store** | Qdrant (local, Docker)                           | `setup_qdrant.py`          |
| **Retrieval**    | `VectorStoreRetriever` (LangChain)               | `learning_agent.py`        |
| **LLM**          | Ollama local **or** OpenRouter remote            | config‑selectable          |
| **Citations**    | manual (string concat)                           |                            |
| **Pain points**  | no OCR; arbitrary chunk sizes; weak traceability |                            |

---

## 2️⃣ Target Architecture (local‑only)

```mermaid
graph TD
  Docs["PDFs / Word / Web pages"] --> |ragflow-cli upload| RAGFlow
  subgraph RAGFlow Service (Docker)
    DeepDoc --> Chunker --> Embeddings
    Embeddings --> KB[(Knowledge Base)]
  end
  learning-agent --> |REST query| RAGFlowRetriever --> |Documents + metadata| learning-agent
  learning-agent --> |prompt| LLM
  LLM --> |answer + citations| User
```

### 2.1 Component Inventory

| Component                 | Runs Locally?     | Licence            | Notes                    |
| ------------------------- | ----------------- | ------------------ | ------------------------ |
| **RAGFlow** service       | ✅ (Docker)        | Apache‑2.0         | CPU or GPU tag           |
| **ragflow-sdk**           | ✅                 | Apache‑2.0         | Python client            |
| **Embeddings**            | ✅ (`bge-m3` GGUF) | Apache‑2.0         | 2–3 GB RAM               |
| **LLM**                   | ✅ (Ollama)        | various permissive | e.g. `deepseek-prover:2` |
| **Vector store fallback** | ✅ Qdrant          | Apache‑2.0         | optional                 |

> **Hardware baseline:** 16 GB RAM, 50 GB disk; GPU (≥8 GB VRAM) strongly recommended for faster OCR/embeddings but not required.

---

## 3️⃣ Work Breakdown Structure

### 3.1 Infrastructure

* [ ] `ops/docker-compose.ragflow.yml` (CPU & GPU profiles)
* [ ] `ops/init_ragflow.sh` (first‑run model download cache)
* [ ] GitHub Action `ci-cache-ragflow` → pre‑warm OCI layer
* [ ] `.env` template: `RAGFLOW_ENDPOINT`, `RAGFLOW_API_KEY`

### 3.2 Codebase Changes

| File                                                     | Action                                               |
| -------------------------------------------------------- | ---------------------------------------------------- |
| `requirements.txt`                                       | + `ragflow-sdk>=0.18.0` (pin), + `ragflow-langchain` |
| `config.yaml`                                            | \`\`\`yaml                                           |
| retriever: ragflow  # or qdrant                          |                                                      |
| ragflow:                                                 |                                                      |
| endpoint: [http://localhost:8000](http://localhost:8000) |                                                      |
| api\_key: null      # not required locally               |                                                      |
| kb\_id: morava\_thesis                                   |                                                      |
| top\_k: 8                                                |                                                      |

````|
| `retriever_factory.py` *(new)* | returns **RAGFlowRetriever** or Qdrant based on config |
| `learning_agent.py` | import factory; remove manual citation stitching |
| `ingest.py` | replace Qdrant push with `subprocess.run(["ragflow-cli", "upload", …])` |
| `Makefile` | `make ragflow-up` / `make ragflow-down` targets |

### 3.3 Data Migration
- [ ] Script `tools/export_qdrant.py` → JSONL
- [ ] `ragflow-cli upload --kb morava_thesis export.jsonl`

### 3.4 Testing & Benchmarking
- [ ] Unit tests (`tests/test_ragflow_retriever.py`)
- [ ] 20‑query regression JSON; pytest parametrised against both retrievers
- [ ] Latency + precision metrics logged to `benchmarks/` (CSV)

### 3.5 Documentation
- [ ] `docs/ragflow_setup.md` (install, GPU flags, troubleshooting)
- [ ] README badges: **local‑only / open‑source**

### 3.6 Roll‑out
1. **Phase 0** – feature flag off (ship infra).
2. **Phase 1** – dev branch: ragflow flag on; run benchmarks.
3. **Phase 2** – staging; gather qualitative feedback.
4. **Phase 3** – merge → tag `v0.4.0`.

---

## 4️⃣ Timeline (10‑day sprint)
| Day | Deliverable |
|-----|-------------|
| 1 | Docker compose + env scaffolding |
| 2 | Retriever factory + config parsing |
| 3 | `RAGFlowRetriever` class + unit tests |
| 4 | Data migration script + first KB import |
| 5 | Update chat loop & ingest pipeline |
| 6 | Benchmark run vs Qdrant (collect metrics) |
| 7 | Optimise `top_k`, chunk templates |
| 8 | Documentation draft & Makefile targets |
| 9 | CI integration + cache job |
| 10 | Code review, changelog, release |

---

## 5️⃣ Detailed **Step‑by‑Step Integration Guide**

### A. Prerequisites
```bash
# host packages
brew install docker docker-compose  # or apt
brew install jq yq  # convenience parsers
pipx install ragflow-cli
````

### B. Fetch & Run RAGFlow Locally

```bash
# clone for reference (optional)
git clone https://github.com/infiniflow/ragflow && cd ragflow

# pull pre‑built CPU image (~6 GB)
docker pull infiniflow/ragflow:latest-cpu

# or GPU tag (requires NVIDIA runtime)
# docker pull infiniflow/ragflow:latest-gpu

# start service on localhost:8000
docker compose -f docker/docker-compose.cpu.yml up -d
```

> **Tip:** First‑run downloads models (\~4 GB). Subsequent starts are instant.

### C. Create a Knowledge Base & Ingest Docs

```bash
# 1. create KB (returns GUID)
KB_ID=$(ragflow-cli kb create --name "morava_thesis" | jq -r .id)

# 2. upload documents (PDFs, MD, etc.)
ragflow-cli upload --kb "$KB_ID" ./data/papers/*.pdf
```

### D. Wire up the Python SDK

```bash
pip install ragflow-sdk==0.18.0 ragflow-langchain==0.2.1
```

**`retriever_factory.py`**

```python
from ragflow_langchain import RagflowRetriever  # pre‑built adapter
from langchain.vectorstores.qdrant import Qdrant


def get_retriever(cfg):
    if cfg.retriever == "ragflow":
        return RagflowRetriever(
            endpoint=cfg.ragflow.endpoint,
            knowledge_base_id=cfg.ragflow.kb_id,
            top_k=cfg.ragflow.top_k,
        )
    else:
        return Qdrant(
            client=qdrant_client,  # existing logic
            collection_name="learning-agent",
        ).as_retriever()
```

### E. Update Config & Makefile

```yaml
# config.yaml
retriever: ragflow  # toggle here
ragflow:
  endpoint: http://localhost:8000
  kb_id: ${RAGFLOW_KB_ID}
  top_k: 8
```

```makefile
ragflow-up:
	docker compose -f ops/docker-compose.ragflow.yml up -d
ragflow-down:
	docker compose -f ops/docker-compose.ragflow.yml down
```

### F. Remove Manual Citation Stitching

```python
# learning_agent.py (snippet)
results = retriever.get_relevant_documents(user_query)
# each result.metadata already has page, file_path
context = "\n".join([d.page_content for d in results])
# pass context → LLM as usual; no extra stitching
```

### G. Validation Checklist

1. **Smoke test**: `python learning_agent.py --query "What is the definition of a complex torus?"` → returns answer + `📄` citations.
2. **Benchmark**: `python tools/benchmark.py --retriever ragflow` → produces `benchmarks/ragflow.csv`.
3. **Fallback toggle**: switch `retriever: qdrant` and rerun – results change but script still works.

---

## 6️⃣ Risks & Mitigations (expanded)

| ID | Risk                      | Prob | Impact | Mitigation                                          |
| -- | ------------------------- | ---- | ------ | --------------------------------------------------- |
| R1 | OCR latency on CPU        | M    | M      | Async tasks; optional GPU; cache PNG pages          |
| R2 | Docker image >6 GB        | L    | M      | Provide `make ragflow-prune` target to clean layers |
| R3 | SDK/service version drift | M    | L      | `pip install --require-hashes`; CI test matrix      |
| R4 | Model licence conflict    | L    | H      | Use Apache‑licensed embeddings/LLMs only            |

---

## 7️⃣ Acceptance Criteria

* **Config toggle** fully swaps retriever.
* ≤15 s end‑to‑end latency on CPU for 2‑page query (<5 s with GPU).
* Precision\@3 ↑ ≥10 % vs baseline.
* All CI tests green; docs updated; Make targets pass.

---

## 8️⃣ Follow‑Ups / Future Enhancements

* GraphRAG upgrade for cross‑doc reasoning
* Table‑aware QA via RAGFlow’s DeepTable
* GitHub Action: nightly sync `/docs` folder with KB
* Add evaluation harness using `ragas` library

---

**Owner:** Dave Bowman
**Target Release:** `v0.4.0` (end of Sprint 24)
**Last updated:** 17 May 2025
