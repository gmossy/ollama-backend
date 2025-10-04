#!/usr/bin/env python3
"""
Ollama + Zscaler Example Usage
Python 3.12.11 compatible
This script demonstrates how to interact with Ollama running in Docker with Zscaler support
"""

import os
import sys
import json
import time
from typing import List, Dict, Optional

try:
    import ollama
    import requests
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install ollama requests")
    sys.exit(1)


class OllamaClient:
    """
    Wrapper class for Ollama client with proper certificate handling
    """

    def __init__(self, host: str = 'http://localhost:11434'):
        self.host = host
        self.client = ollama.Client(host=host)

        # Set certificate bundle for requests if behind Zscaler
        if 'REQUESTS_CA_BUNDLE' in os.environ:
            self.verify_ssl = os.environ['REQUESTS_CA_BUNDLE']
        else:
            self.verify_ssl = True

    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(
                f"{self.host}/api/version",
                verify=self.verify_ssl,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def list_models(self) -> List[Dict]:
        """List all available models"""
        try:
            models = self.client.list()
            return models.get('models', [])
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            print(f"Pulling model: {model_name}")
            print("This may take a few minutes...")

            # Stream the pull progress
            for progress in self.client.pull(model_name, stream=True):
                status = progress.get('status', '')
                if 'total' in progress and 'completed' in progress:
                    percent = (progress['completed'] / progress['total']) * 100
                    print(f"\r{status}: {percent:.1f}%", end='', flush=True)
                else:
                    print(f"\r{status}", end='', flush=True)

            print("\n✓ Model pulled successfully!")
            return True

        except Exception as e:
            print(f"\nError pulling model: {e}")
            return False

    def generate(self, model: str, prompt: str, stream: bool = False) -> Optional[str]:
        """Generate a response from the model"""
        try:
            if stream:
                print(f"\n{model}:", end=' ', flush=True)
                full_response = ""
                for chunk in self.client.generate(model=model, prompt=prompt, stream=True):
                    content = chunk.get('response', '')
                    print(content, end='', flush=True)
                    full_response += content
                print()  # New line after streaming
                return full_response
            else:
                response = self.client.generate(model=model, prompt=prompt)
                return response.get('response', '')

        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    def chat(self, model: str, messages: List[Dict], stream: bool = False) -> Optional[str]:
        """Chat with the model using conversation history"""
        try:
            if stream:
                print(f"\n{model}:", end=' ', flush=True)
                full_response = ""
                for chunk in self.client.chat(model=model, messages=messages, stream=True):
                    content = chunk.get('message', {}).get('content', '')
                    print(content, end='', flush=True)
                    full_response += content
                print()
                return full_response
            else:
                response = self.client.chat(model=model, messages=messages)
                return response.get('message', {}).get('content', '')

        except Exception as e:
            print(f"Error in chat: {e}")
            return None


def main():
    """Main example function"""

    print("=" * 60)
    print("Ollama + Zscaler Example Usage")
    print("=" * 60)
    print()

    # Initialize client
    client = OllamaClient(host='http://localhost:11434')

    # Check connection
    print("1. Checking connection to Ollama...")
    if not client.check_connection():
        print("❌ Cannot connect to Ollama. Make sure it's running:")
        print("   docker compose up -d")
        sys.exit(1)
    print("✓ Connected to Ollama")
    print()

    # List available models
    print("2. Listing available models...")
    models = client.list_models()
    if models:
        print(f"✓ Found {len(models)} model(s):")
        for model in models:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"   - {name} ({size:.2f} GB)")
    else:
        print("⚠ No models found. Let's pull one!")
    print()

    # Ensure we have a model
    default_model = 'llama3.2'
    model_names = [m.get('name', '') for m in models]

    if not any(default_model in name for name in model_names):
        print(f"3. Pulling {default_model} model...")
        if not client.pull_model(default_model):
            print("❌ Failed to pull model")
            sys.exit(1)
        print()

    # Example 1: Simple generation
    print("=" * 60)
    print("Example 1: Simple Text Generation")
    print("=" * 60)

    prompt = "Explain what Docker is in one sentence."
    print(f"\nPrompt: {prompt}")
    print("-" * 60)

    response = client.generate(
        model=default_model,
        prompt=prompt,
        stream=True
    )

    print()

    # Example 2: Chat conversation
    print("=" * 60)
    print("Example 2: Chat Conversation")
    print("=" * 60)
    print()

    messages = [
        {
            'role': 'system',
            'content': 'You are a helpful AI assistant that provides concise answers.'
        },
        {
            'role': 'user',
            'content': 'What are the benefits of containerization?'
        }
    ]

    print("User: What are the benefits of containerization?")
    print("-" * 60)

    response = client.chat(
        model=default_model,
        messages=messages,
        stream=True
    )

    print()

    # Example 3: Multi-turn conversation
    print("=" * 60)
    print("Example 3: Multi-turn Conversation")
    print("=" * 60)
    print()

    conversation =
