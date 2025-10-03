# DPGAI: Ollama for Digital Proving Ground

## What is Ollama?

Ollama is an open-source platform for running and serving large language models (LLMs) locally. It provides a simple way to download, run, and fine-tune various state-of-the-art AI models like Llama, Mistral, and others on your local machine or server. Key features include:

- Run powerful AI models without requiring cloud services
- Simple API for integration with applications
- Support for multiple models and model switching
- Low-latency inference for real-time applications
- Ability to run models on consumer hardware

## What This Docker Setup Provides

This Docker configuration creates a containerized environment for running Ollama with the following benefits:

1. **Isolation**: Runs Ollama in a contained environment without affecting your host system
2. **Reproducibility**: Ensures consistent setup across different development environments
3. **Portability**: Works across different operating systems and environments
4. **Corporate Network Compatibility**: Configured to work within enterprise networks with SSL inspection (e.g., Zscaler)
5. **Simplified Management**: Includes Makefile commands for easy container and model management

## How This Helps Digital Proving Ground

The Digital Proving Ground (DPG) benefits from this Ollama Docker setup in several key ways:

1. **Local AI Capabilities**: Enables DPG to run powerful AI models locally, ensuring data privacy and reducing dependency on external services.

2. **Reduced Latency**: By hosting models locally, DPG applications can interact with AI models with minimal latency, crucial for real-time analysis and decision support.

3. **Cost Efficiency**: Eliminates recurring cloud API costs associated with commercial LLM services, making AI integration more sustainable.

4. **Custom Model Control**: Provides DPG complete control over which models to use and how to configure them, allowing for specialized optimization.

5. **Air-Gapped Operation**: Supports scenarios where DPG applications need to operate in disconnected or secure environments without internet access.

6. **Integration Flexibility**: The simple API allows DPG developers to easily incorporate AI capabilities into various applications and services.

7. **Rapid Prototyping**: Enables quick experimentation with different models and approaches without complex infrastructure changes.

8. **Enterprise Network Compatibility**: Configured to work within DOD and military networks that use corporate proxies and SSL inspection.


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

For a list of available models, visit: <https://ollama.com/library>

## Updating Models

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

## Handling Certificate Issues in Corporate Environments

If you're behind a corporate proxy like Zscaler that performs TLS inspection, you might encounter certificate verification errors. Our Docker setup addresses this with:

1. Environment variables to bypass certificate verification:
   - `OLLAMA_INSECURE=true`
   - `SSL_CERT_FILE=/dev/null`
   - `GIT_SSL_NO_VERIFY=true`
   - `NO_PROXY=localhost,127.0.0.1`

2. When pulling models, use the environment variables:

   ```bash
   docker exec -it -e OLLAMA_INSECURE=true -e SSL_CERT_FILE=/dev/null ollama ollama pull <model-name>
   ```

## Troubleshooting

If your Ollama container is not starting properly or keeps restarting:

1. Check the logs:

   ```bash
   docker logs ollama
   ```

2. Complete rebuild (if needed):

   ```bash
   docker stop ollama
   docker rm ollama
   docker rmi $(docker images | grep ollama | awk '{print $3}')
   cd /Users/glennmossy/dpg-ai-projects/DPGAI/backend
   make build
   make up
   ```

3. Check resource allocation in Docker Desktop:
   - Ollama requires significant memory (8GB+ recommended)
   - Navigate to Docker Desktop → Settings → Resources → Advanced to increase allocation

## Using Makefile

This project includes a Makefile for easier management:

```bash
# Build the container
make build

# Start the container
make up

# Stop the container
make down

# Restart the container
make restart

# Pull models
make pull-models MODELS='llama3 mistral'

# List installed models
make list-models

# View logs
make logs

# Clean up containers and images
make clean
```

```

This README now includes comprehensive information about handling certificate issues in corporate environments, troubleshooting steps, and usage instructions for the Makefile.
