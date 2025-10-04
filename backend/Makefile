.PHONY: help build up down restart pull-models update-models list-models logs clean prune pull-models-ci setup status

DOCKER_COMPOSE = docker-compose
CONTAINER_NAME = zscaler-ollama # Changed container name

help:
	@echo "Makefile commands:"
	@echo "  build        - Build the Docker image"
	@echo "  up           - Start the $(CONTAINER_NAME) container"
	@echo "  down         - Stop the $(CONTAINER_NAME) container"
	@echo "  restart      - Restart the $(CONTAINER_NAME) container"
	@echo "  pull-models  - Pull specified models (e.g., make pull-models MODELS='llama3 mistral')"
	@echo "  pull-models-ci - Pull models without interactive terminal (for CI/CD)"
	@echo "  update-models - Update all pulled models"
	@echo "  list-models  - List all available models"
	@echo "  logs         - View container logs"
	@echo "  clean        - Remove containers, volumes, and images"
	@echo "  prune        - Completely remove all $(CONTAINER_NAME) Docker resources"
	@echo "  status       - Show status of the $(CONTAINER_NAME) container"
	@echo "  setup        - Perform initial setup: generate cert, clean, build, up, pull initial models" # Updated help

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart: down up

pull-models:
	@if [ -z "$(MODELS)" ]; then \
		echo "Please specify models to pull, e.g., make pull-models MODELS='llama3 mistral'"; \
	else \
		for model in $(MODELS); do \
			echo "Pulling $$model..."; \
			docker exec -it $(CONTAINER_NAME) bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama pull $$model"; \
		done; \
	fi

pull-models-ci:
	@if [ -z "$(MODELS)" ]; then \
		echo "Please specify models to pull, e.g., make pull-models-ci MODELS='llama3 mistral'"; \
	else \
		for model in $(MODELS); do \\\
			echo "Pulling $$model..."; \
			docker exec $(CONTAINER_NAME) bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama pull $$model"; \
		done; \
	fi

update-models:
	docker exec -it $(CONTAINER_NAME) bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama list | tail -n +2 | awk '{print \$$1}' | xargs -I {} ollama pull {}"

list-models:
	docker exec -it $(CONTAINER_NAME) ollama list

logs:
	$(DOCKER_COMPOSE) logs -f

clean:
	$(DOCKER_COMPOSE) down -v --rmi local

prune:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi -f $$(docker images --format "{{.ID}}\t{{.Repository}}" | grep "zscaler-ollama" | awk '{print $$1}') || true
	docker system prune -f --volumes
	rm -rf ./zscaler_ollama_data || true # Update volume directory here
	mkdir -p ./zscaler_ollama_data

setup: cert-generate-copy clean build up pull-initial-models
	@echo ""
	@echo "=================================================="
	@echo "   DPG-Ollama Docker setup complete and running!  "
	@echo "=================================================="
	@echo ""
	@echo "To pull more models: make pull-models MODELS='<model1> <model2>'"
	@echo "To check status: make status"

# Helper target to generate and copy the Zscaler certificate
cert-generate-copy:
	@echo "Ensuring Zscaler certificate is in place..."
	@# Run script from current directory, then it generates cert in current dir
	chmod +x ./generate-cert.sh && ./generate-cert.sh
	# No need to copy from parent, as it's generated here
	# cp $(CURDIR)/../zscaler-root-ca.crt $(CURDIR)/zscaler-root-ca.crt || true 
	@echo "Zscaler certificate ready in backend/."

# Helper target to pull initial models
pull-initial-models:
	@echo "Pulling initial models (llama3, mistral, gpt-oss:20b, gemma3:12b, qwen3)..."
	# $(MAKE) pull-models MODELS='llama3 mistral gpt-oss:20b gemma3:12b qwen3'
	$(MAKE) pull-models MODELS='llama3'
	@echo "Initial models pull initiated."