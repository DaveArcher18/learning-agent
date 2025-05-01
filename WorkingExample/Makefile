.PHONY: start_qdrant stop_qdrant agent run

# Start Qdrant with persistent volume (detached)
start_qdrant:
	docker run -d --name qdrant_research \
		-p 6333:6333 \
		-v qdrant_research_agent:/qdrant/storage \
		qdrant/qdrant

# Stop & remove the Qdrant container if running
stop_qdrant:
	-@docker stop qdrant_research 2>/dev/null || true
	-@docker rm   qdrant_research 2>/dev/null || true

# Launch the interactive research agent
agent:
	python research_agent.py

# One-liner: start Qdrant (if needed) then run agent
run: start_qdrant agent