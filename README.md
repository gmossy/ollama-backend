# Ollama Backend: Simple Local Docker Setup

**Author:** Glenn Mossy  
**Branch:** `ollama-backend-simple`

A lightweight, no-fuss Docker setup to run Ollama locally without corporate proxies or certificates—perfect for development, experimentation, and integrating vision and text models.

---

## 🚀 What This Does

- **Runs Ollama locally** in a single Docker container, exposing the API on `http://localhost:11434`.
- **No Zscaler/proxy required**—stripped of all corporate TLS inspection logic.
- **Model switching on the fly**—use `llama3` for text or `qwen3-vl:latest` for vision tasks in the same container.
- **Python client example** with timing, error handling, and vision support.
- **Performance tuning defaults** in `.env` for latency, quality, and resource control.
- **uv-based Python environment** for fast, reproducible installs.

---

## 📋 Prerequisites

- Docker installed and running.
- At least 8 GB RAM available for Docker (more for larger models).
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python environment management.

---

## ⚙️ Quick Start

### 1. Clone and switch branch

```bash
git clone https://github.com/gmossy/ollama-backend
cd ollama-backend
git checkout ollama-backend-simple
```

### 2. Start Ollama with Docker Compose

```bash
cd backend/ollama
docker compose -f docker-compose.local.yml up -d
```

Verify it’s running:

```bash
curl http://localhost:11434/api/version
```

### 3. Set up Python environment with uv

```bash
cd ../../backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 4. Run the Python client

```bash
# Text-only demo
python ollama_client.py

# Vision demo (provide an image)
python ollama_client.py /path/to/image.png
```

---

## 🐳 Docker Details

- **Compose file:** `backend/ollama/docker-compose.local.yml`
- **Container name:** `ollama-local`
- **Exposed port:** `11434`
- **Persistent volume:** `ollama_data` (stores models)
- **Base image:** `ollama/ollama:latest` (pulled at runtime)

### Useful Make commands (from `backend/`)

```bash
make -f makefile.local up          # Start container
make -f makefile.local down        # Stop container
make -f makefile.local logs        # Follow logs
make -f makefile.local status      # Show container status
make -f makefile.local pull-models MODELS='llama3 mistral'  # Pull models
```

---

## 🐍 Python Client Features

- **Model-per-request switching** (text or vision).
- **Base64 image encoding** for multimodal inputs.
- **Request timing** printed for each call.
- **Timeout handling** (60s default) and robust error paths.
- **Non-streaming and optional streaming modes.**

Example usage:

```python
from ollama_client import generate

# Text
print(generate("llama3", "Summarize Docker in one sentence.")["response"])

# Vision
print(generate(
    "qwen3-vl:latest",
    "What’s in this image?",
    image_path="screenshot.png"
)["response"])
```

---

## 🎛️ Performance & Server Tuning

The included `.env` file provides sensible defaults you can override:

```bash
# Sampling
OLLAMA_TEMPERATURE=0.2
OLLAMA_TOP_P=0.85
OLLAMA_REPEAT_PENALTY=1.1

# Context & output
OLLAMA_NUM_CTX=8192
OLLAMA_NUM_PREDICT=2048

# Server behavior
OLLAMA_MAX_LOADED_MODELS=2
OLLAMA_KEEP_ALIVE=30m
OLLAMA_NUM_PARALLEL=2
```

Load in your app with `python-dotenv` or source in your shell.

---

## 📦 Project Structure

```
ollama-container/
├── .env                     # Client/server performance tuning
├── .gitignore               # Ignores local data, caches, IDE files
├── SETUP.md                 # uv setup instructions
├── backend/
│   ├── makefile.local        # Handy Docker targets
│   ├── requirements.txt      # Python deps
│   ├── ollama_client.py      # Example client with timing & vision
│   └── ollama/
│       ├── docker-compose.local.yml
│       ├── Dockerfile        # (optional; not used by default)
│       └── README.local.md   # Quick-start commands
```

---

## 🧪 Troubleshooting

- **Model pull fails with “requires a newer version of Ollama”**
  - Stop, pull the latest image, and restart:
    ```bash
    docker compose -f docker-compose.local.yml down
    docker compose -f docker-compose.local.yml pull
    docker compose -f docker-compose.local.yml up -d
    ```

- **500 errors from the API**
  - Check container logs: `make -f makefile.local logs`
  - Ensure you have enough RAM/VRAM for the selected model.

- **Vision model doesn’t see images**
  - Verify the image path exists and is a supported format.
  - Ensure you’re using `qwen3-vl:latest`.

---

## 🤝 Contributing

Feel free to open issues or PRs on the `ollama-backend-simple` branch. For major changes, please discuss first.

---

## 📜 License

This project follows the repository’s existing license.

---

> **Built by Glenn Mossy** to simplify local Ollama development without the friction of corporate proxies. Happy hacking! 🚀