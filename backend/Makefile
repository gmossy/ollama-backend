.PHONY: help build up down restart pull-models update-models list-models logs clean

DOCKER_COMPOSE = docker-compose
CONTAINER_NAME = ollama

help:
	@echo "Makefile commands:"
	@echo "  build        - Build the Docker image"
	@echo "  up           - Start the Ollama container"
	@echo "  down         - Stop the Ollama container"
	@echo "  restart      - Restart the Ollama container"
	@echo "  pull-models  - Pull specified models (e.g., make pull-models MODELS='llama3 mistral')"
	@echo "  update-models - Update all pulled models"
	@echo "  list-models  - List all available models"
	@echo "  logs         - View container logs"
	@echo "  clean        - Remove containers, volumes, and images"

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
		errors=0; \
		for model in $(MODELS); do \
			echo "Pulling $$model..."; \
			docker exec -it $(CONTAINER_NAME) bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama pull $$model"; \
			if [ $$? -ne 0 ]; then \
				echo "Error pulling $$model"; \
				errors=$$((errors+1)); \
			fi; \
		done; \
		echo "Pull complete with $$errors errors."; \
	fi

update-models:
	docker exec -it $(CONTAINER_NAME) bash -c "export OLLAMA_INSECURE=true && export SSL_CERT_FILE=/dev/null && export GIT_SSL_NO_VERIFY=true && export CURL_CA_BUNDLE=/dev/null && ollama list | tail -n +2 | awk '{print \$$1}' | xargs -I {} ollama pull {}"

list-models:
	docker exec -it $(CONTAINER_NAME) ollama list

logs:
	$(DOCKER_COMPOSE) logs -f

clean:
	$(DOCKER_COMPOSE) down -v --rmi local