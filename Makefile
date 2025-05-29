# --------------------------------------------------------------------
# LearningAgent Makefile
# --------------------------------------------------------------------
# RAGFlow Targets (Primary):
#   make ragflow-start    →  start RAGFlow with BGE-M3 setup
#   make ragflow-stop     →  stop RAGFlow services
#   make ragflow-logs     →  view RAGFlow logs
#   make ragflow-health   →  check RAGFlow service health
#   make ragflow-setup    →  initialize RAGFlow knowledge base
#   make ragflow-ingest   →  ingest documents to RAGFlow
#   make ragflow-migrate  →  migrate from Qdrant to RAGFlow
#   make ragflow-clean    →  clean RAGFlow data (DANGER: wipes data)
#
# Legacy Qdrant Targets (Migration Support):
#   make start_qdrant     →  start (or reuse) a local Qdrant Docker
#   make setup            →  create the collection in Qdrant if missing
#   make ingest           →  ingest ./docs into Qdrant
#   make audit            →  show stats and info about the collection
#   make stop_qdrant      →  stop & remove the Qdrant container
#   make clean            →  delete qdrant_data volume (DANGER: wipes vectors)
#
# General Targets:
#   make run              →  chat with the agent (uses RAGFlow)
#   make test             →  run test suite
#   make install          →  install Python dependencies
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

# ====================================================================
# RAGFlow Management (Primary RAG Engine)
# ====================================================================

RAGFLOW_COMPOSE = docker-compose.ragflow.yml
RAGFLOW_SERVICE = ragflow
RAGFLOW_CONTAINER = ragflow

.PHONY: ragflow-start ragflow-stop ragflow-logs ragflow-health ragflow-setup ragflow-ingest ragflow-migrate ragflow-clean

# Start RAGFlow with BGE-M3 setup
ragflow-start:
	@echo "🚀 Starting RAGFlow with BGE-M3 mathematical content setup..."
	@mkdir -p data/documents conf
	@echo "📁 Created data directories"
	@docker compose -f $(RAGFLOW_COMPOSE) up -d
	@echo "⏳ Waiting for RAGFlow to initialize (60s)..."
	@sleep 60
	@echo "✅ RAGFlow available at http://localhost:9380"
	@echo "🔗 RAGFlow Web UI at http://localhost:80"

# Stop RAGFlow services
ragflow-stop:
	@echo "🔴 Stopping RAGFlow services..."
	@docker compose -f $(RAGFLOW_COMPOSE) down
	@echo "✅ RAGFlow services stopped"

# View RAGFlow logs
ragflow-logs:
	@echo "📋 RAGFlow logs (press Ctrl+C to exit):"
	@docker compose -f $(RAGFLOW_COMPOSE) logs -f $(RAGFLOW_SERVICE)

# Check RAGFlow service health
ragflow-health:
	@echo "🏥 Checking RAGFlow service health..."
	@if docker ps --format '{{.Names}}' | grep -q "^$(RAGFLOW_CONTAINER)$$"; then \
		echo "✅ RAGFlow container is running"; \
		curl -f http://localhost:9380/health || echo "❌ RAGFlow API health check failed"; \
	else \
		echo "❌ RAGFlow container is not running"; \
	fi

# Initialize RAGFlow knowledge base for mathematical content
ragflow-setup: ragflow-start
	@echo "🛠️ Setting up RAGFlow knowledge base for mathematical content..."
	@echo "📊 This will configure BGE-M3 embeddings and mathematical processing..."
	$(PY) -c "from src.rag.ragflow_setup import setup_mathematical_kb; setup_mathematical_kb()"
	@echo "✅ RAGFlow knowledge base initialized"

# Ingest documents to RAGFlow with mathematical content processing
ragflow-ingest: ragflow-setup
	@echo "📚 Ingesting documents to RAGFlow with mathematical processing..."
	@mkdir -p docs
	$(PY) -c "from src.rag.ragflow_ingest import ingest_documents; ingest_documents('./docs')"
	@echo "✅ Document ingestion completed"

# Migrate from Qdrant to RAGFlow
ragflow-migrate: ragflow-setup
	@echo "🔄 Starting migration from Qdrant to RAGFlow..."
	@echo "⚠️ This will export Qdrant data and import to RAGFlow"
	$(PY) -c "from src.rag.migration import migrate_qdrant_to_ragflow; migrate_qdrant_to_ragflow()"
	@echo "✅ Migration completed"

# Clean RAGFlow data (DANGEROUS)
ragflow-clean:
	@echo "🗑️ WARNING: This will delete all RAGFlow data!"
	@read -p "Type 'DELETE' to confirm: " confirm; \
	if [ "$$confirm" = "DELETE" ]; then \
		docker compose -f $(RAGFLOW_COMPOSE) down -v; \
		docker volume prune -f; \
		echo "✅ RAGFlow data cleaned"; \
	else \
		echo "❌ Cleanup cancelled"; \
	fi

# ====================================================================
# General Targets
# ====================================================================

# Install Python dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Run test suite
test:
	@echo "🧪 Running test suite..."
	$(PY) -m pytest tests/ -v
	@echo "✅ Tests completed"

# Default development workflow
dev-setup: install ragflow-start ragflow-setup
	@echo "🎯 Development environment ready!"
	@echo "📚 Add documents to ./docs/ then run: make ragflow-ingest"
	@echo "💬 Start chatting with: make run"

# Quick start for new users
quickstart: dev-setup
	@echo "🚀 Quick start completed!"
	@echo "📖 Check README.md for usage instructions"