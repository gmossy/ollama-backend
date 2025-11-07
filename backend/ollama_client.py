#!/usr/bin/env python3
"""
Example client for switching between Ollama models in a single container.
Supports text-only and vision (image+text) requests.
"""

import base64
import json
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment from .env (optional)
load_dotenv()

OLLAMA_BASE = "http://localhost:11434"


def encode_image_path(image_path: str) -> str:
    """Return base64-encoded image from file path."""
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate(model: str, prompt: str, image_path: str | None = None, stream: bool = False):
    """
    Send a generation request to Ollama.
    - model: e.g., 'llama3' or 'qwen3-vl:latest'
    - prompt: text prompt
    - image_path: optional path to an image file for vision models
    - stream: whether to stream tokens (default: False)
    Returns: JSON response (or generator if streaming)
    """
    payload = {"model": model, "prompt": prompt, "stream": stream}
    if image_path:
        payload["images"] = [encode_image_path(image_path)]

    resp = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, stream=False)
    resp.raise_for_status()
    # Ollama may still stream lines; handle both cases
    try:
        data = resp.json()
        return data
    except requests.exceptions.JSONDecodeError:
        # Fallback: parse line-by-line and return the last complete JSON
        final = None
        for line in resp.iter_lines(decode_unicode=True):
            if line:
                final = json.loads(line)
        return final


def main():
    """Demo: call both text and vision models."""
    # Text-only example with llama3
    print("=== llama3 (text) ===")
    start = time.time()
    try:
        result = generate("llama3", "List three benefits of Docker.")
        print(result["response"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"[Time: {time.time() - start:.2f}s]\n")

    print("=== qwen3-vl:latest (text) ===")
    start = time.time()
    try:
        result = generate("qwen3-vl:latest", "Explain quantum computing in one sentence.")
        print(result["response"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"[Time: {time.time() - start:.2f}s]\n")

    # Vision example (provide an image path on CLI or change here)
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    if image_path:
        print(f"=== qwen3-vl:latest (vision with {image_path}) ===")
        start = time.time()
        try:
            result = generate("qwen3-vl:latest", "What is shown in this image?", image_path=image_path)
            print(result["response"])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f"[Time: {time.time() - start:.2f}s]")
    else:
        print("\n=== Vision example skipped ===")
        print("Provide an image path as an argument to test vision, e.g.:")
        print("  python ollama_client.py /path/to/image.png")


if __name__ == "__main__":
    main()
