# --------------------------------------------------------------------
# LearningAgent Makefile
# --------------------------------------------------------------------
# Targets:
#   make start_qdrant   →  start (or reuse) a local Qdrant Docker
#   make setup          →  create the collection in Qdrant if missing
#   make ingest         →  ingest ./docs into Qdrant
#   make run            →  chat with the agent
#   make audit          →  show stats and info about the collection
#   make stop_qdrant    →  stop & remove the Qdrant container
#   make clean          →  delete qdrant_data volume (DANGER: wipes vectors)
# --------------------------------------------------------------------

PY      = python
CONTAINER = qdrant_local
VOLUME    = qdrant_data
PORT      = 6333
QDRANT_IMAGE = qdrant/qdrant:latest

# -------- Docker helpers -----------------------------------------------------
.PHONY: start_qdrant stop_qdrant clean setup ingest run audit

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
	@sleep 2  # Give Qdrant a moment to initialize

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
	@echo "🧹 Removing embedded Qdrant data..."
	@rm -rf ./qdrant_data
	@echo "✅ Local storage cleaned."

# -------- DB initialisation and management -----------------------------------
setup: start_qdrant
	@echo "🛠️  Setting up collection from config.yaml..."
	$(PY) setup_qdrant.py

# -------- Ingestion & Agent ---------------------------------------------------
ingest: setup
	@echo "📚 Ingesting documents from ./docs …"
	@mkdir -p docs
	$(PY) ingest.py --path ./docs

# Run the learning agent
run: setup
	@echo "💬 Starting LearningAgent CLI …"
	$(PY) learning_agent.py

# Audit the database to check its status
audit: 
	@echo "🔍 Auditing Qdrant database..."
	$(PY) audit_qdrant.py