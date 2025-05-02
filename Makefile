# --------------------------------------------------------------------
# LearningAgent Makefile
# --------------------------------------------------------------------
# Targets:
#   make start_qdrant   →  start (or reuse) a local Qdrant Docker
#   make setup_db       →  create the 'kb' collection if missing
#   make ingest         →  ingest ./docs into Qdrant
#   make run            →  chat with the agent (starts Qdrant first)
#   make stop_qdrant    →  stop & remove the Qdrant container
#   make clean          →  delete qdrant_data volume (DANGER: wipes vectors)
#   make clear_db       →  delete all data in the kb collection but keep the collection
# --------------------------------------------------------------------

PY      = python
CONTAINER = qdrant_local
VOLUME    = qdrant_data
PORT      = 6333
QDRANT_IMAGE = qdrant/qdrant:latest

# -------- Docker helpers -----------------------------------------------------
.PHONY: start_qdrant stop_qdrant clean setup_db ingest run run_docker clear_db

# Start Qdrant container (or reuse if it exists)
start_qdrant:
	@echo "🟢 Starting Qdrant Docker on port $(PORT)..."
	@if docker ps -a --format '{{.Names}}' | grep -q "^$(CONTAINER)$$"; then \
		if docker ps --format '{{.Names}}' | grep -q "^$(CONTAINER)$$"; then \
			echo "🔄 Container '$(CONTAINER)' already running."; \
		else \
			echo "🔄 Starting existing container '$(CONTAINER)'..."; \
			docker start $(CONTAINER); \
		fi; \
	else \
		echo "🏗️ Creating new container '$(CONTAINER)'..."; \
		docker run -d --name $(CONTAINER) \
			-p $(PORT):6333 \
			-v $(VOLUME):/qdrant/storage \
			$(QDRANT_IMAGE); \
	fi
	@echo "✅ Qdrant available at http://localhost:$(PORT)"

# Stop and remove the Qdrant container
stop_qdrant:
	@echo "🔴 Stopping Qdrant Docker..."
	@if docker ps -a --format '{{.Names}}' | grep -q "^$(CONTAINER)$$"; then \
		docker stop $(CONTAINER); \
		docker rm $(CONTAINER); \
		echo "✅ Container stopped and removed."; \
	else \
		echo "ℹ️ Container '$(CONTAINER)' not found."; \
	fi

# Remove the Docker volume as well
clean: stop_qdrant
	@echo "🗑️ Removing volume $(VOLUME)..."
	@if docker volume ls --format '{{.Name}}' | grep -q "^$(VOLUME)$$"; then \
		docker volume rm $(VOLUME); \
		echo "✅ Volume deleted."; \
	else \
		echo "ℹ️ Volume '$(VOLUME)' not found."; \
	fi

# -------- DB initialisation ---------------------------------------------------
setup_db: 
	@echo "🛠️  Ensuring 'kb' collection exists…"
	$(PY) setup_qdrant.py

# Clear all vectors from the kb collection but keep the collection structure
clear_db:
	@echo "🗑️  Clearing all data from the 'kb' collection..."
	@echo 'from qdrant_client import QdrantClient\n\
try:\n\
    client = QdrantClient(path="./qdrant_data")\n\
    client.delete_collection("kb")\n\
    print("Deleted local embedded collection")\n\
except Exception as e:\n\
    print(f"Could not clear embedded collection: {e}")\n\
    try:\n\
        client = QdrantClient(host="localhost", port=6333)\n\
        client.delete_collection("kb")\n\
        print("Deleted Docker-based collection")\n\
    except Exception as e2:\n\
        print(f"Could not clear Docker collection: {e2}")\n\
        print("Could not delete collection. Is Qdrant running?")\n' > clear_db_temp.py
	$(PY) clear_db_temp.py
	rm clear_db_temp.py
	$(PY) setup_qdrant.py

# -------- Ingestion & Agent ---------------------------------------------------
ingest: setup_db
	@echo "📚 Ingesting documents from ./docs …"
	@mkdir -p docs
	$(PY) ingest.py --path ./docs

# Use embedded qdrant for simplicity
run: setup_db
	@echo "💬 Starting LearningAgent CLI …"
	$(PY) learning_agent.py

# Use Docker qdrant (preferred for stability)
run_docker: start_qdrant setup_db
	@echo "💬 Starting LearningAgent CLI with Docker Qdrant …"
	$(PY) learning_agent.py