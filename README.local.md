# Local Ollama Docker Setup

A simplified Docker setup for running Ollama locally without corporate proxy/certificate requirements.

## Quick Start

### Prerequisites
- Docker installed and running
- At least 8GB RAM available for Docker

### Build and Run

```bash
# Using Docker Compose (recommended)
docker compose -f docker-compose.local.yml up -d

# Or using Make
make -f Makefile.local up
```

### Pull Models

```bash
# Pull a single model
docker exec -it ollama-local ollama pull llama3

# Pull multiple models using Make
make -f Makefile.local pull-models MODELS='llama3 mistral'
```

### List Available Models

```bash
make -f Makefile.local list-models
```

### Test the API

```bash
# Check version
curl http://localhost:11434/api/version

# Generate text
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

### Stop the Container

```bash
make -f Makefile.local down
```

## Available Commands

```bash
make -f Makefile.local help     # Show all available commands
make -f Makefile.local build    # Build the Docker image
make -f Makefile.local up       # Start the container
make -f Makefile.local down     # Stop the container
make -f Makefile.local restart  # Restart the container
make -f Makefile.local logs     # View container logs
make -f Makefile.local status   # Check container status
make -f Makefile.local clean    # Remove container and volumes
```

## Directory Structure

```
ollama-backend/
├── docker-compose.local.yml  # Docker Compose config for local dev
├── Dockerfile.local          # Simplified Dockerfile
├── Makefile.local           # Make commands for easy management
└── README.local.md          # This file
```

## Models

Visit https://ollama.com/library for a complete list of available models.

Popular models:
- `llama3` - Meta's Llama 3 model
- `mistral` - Mistral AI's model
- `phi` - Microsoft's Phi model
- `codellama` - Code-specialized Llama model

## Troubleshooting

### Container won't start
```bash
docker logs ollama-local
```

### Check if Ollama is running
```bash
curl http://localhost:11434/api/version
```

### Remove everything and start fresh
```bash
make -f Makefile.local clean
make -f Makefile.local up
```

## Differences from Production Setup

This local setup differs from the `backend/` Zscaler setup:
- No Zscaler certificate handling
- No corporate proxy configuration
- Simpler configuration for local development
- Standard Ollama image without modifications

For production/corporate environments, see `backend/README.md`.
