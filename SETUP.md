# Environment Setup with uv

## Prerequisites

- Install uv: https://docs.astral.sh/uv/getting-started/installation/

## Quick setup

```bash
# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Run the client

```bash
# Text-only demo
python ollama_client.py

# Vision demo (provide an image)
python ollama_client.py /path/to/image.png
```

## Notes

- The virtual environment (.venv) is already ignored by .gitignore.
- You can also use `uv run python ollama_client.py` to run without explicit activation.
