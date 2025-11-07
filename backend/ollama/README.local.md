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

make -f ../makefile.local up

```
