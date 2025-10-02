# Ollama Backend

This directory contains Docker configuration for running Ollama.

## Getting Started

1. Start the Ollama service:
   ```bash
   docker-compose up -d
   ```

2. Verify the service is running:
   ```bash
   docker ps
   ```

3. Pull a model:
   ```bash
   docker exec -it ollama ollama pull <model-name>
   ```

4. Run a model:
   ```bash
   docker exec -it ollama ollama run <model-name>
   ```

## Available Models

For a list of available models, visit: https://ollama.com/library

[1 tool called]

To update all your previously pulled Ollama models in your Docker container, follow these steps:

1. Access your Ollama container with:

```bash
docker exec -it ollama bash
```

2. Once inside the container, run this one-liner to update all models:

```bash
ollama list | tail -n +2 | awk '{print $1}' | xargs -I {} ollama pull {}
```

If you prefer not to enter the container, you can run it all in one command:

```bash
docker exec -it ollama bash -c "ollama list | tail -n +2 | awk '{print \$1}' | xargs -I {} ollama pull {}"
```

This command:

1. Lists all your installed models
2. Removes the header line
3. Extracts just the model names
4. Pulls the latest version of each model

If you're running Ollama without Docker, you can simply run the command directly:

```bash
ollama list | tail -n +2 | awk '{print $1}' | xargs -I {} ollama pull {}
```
