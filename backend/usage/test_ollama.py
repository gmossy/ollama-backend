import json
from ollama_service import ask_ollama_structured
import os

def run_ollama_tests():
    """
    Demonstrates how to use the ask_ollama_structured function to get JSON responses
    from the Ollama LLM.
    """
    print("--- Running Ollama Structured Response Tests ---")

    # Assuming 'llama3' is pulled by 'make setup'
    model_name = os.getenv('OLLAMA_MODEL', 'llama3')
    ollama_host = os.getenv('OLLAMA_HOST_URL', 'http://localhost:11434')

    print(f"Using Ollama Model: {model_name} at Host: {ollama_host}")

    # Example 1: Explain Docker in a structured JSON format
    prompt_docker = "Explain Docker in one sentence, providing a concise summary and 3 key benefits."
    system_message_docker = "Provide your answer in JSON format with two keys: 'summary' (string) and 'benefits' (a list of 3 strings)."

    print("\n--- Test 1: Docker Explanation ---")
    try:
        response_docker = ask_ollama_structured(
            model=model_name,
            prompt=prompt_docker,
            system_message=system_message_docker,
            host=ollama_host
        )
        print("Received structured response:")
        print(json.dumps(response_docker, indent=2))
        print(f"Summary: {response_docker.get('summary', 'N/A')}")
        print("Benefits:")
        for i, benefit in enumerate(response_docker.get('benefits', [])):
            print(f"  {i+1}. {benefit}")

    except Exception as e:
        print(f"❌ Error testing Docker explanation: {e}")

    # Example 2: List 3 key features of Large Language Models in JSON format
    prompt_llm_features = "List 3 key features of Large Language Models (LLMs)."
    system_message_llm_features = "Provide your answer in JSON format with a single key 'features' which is a list of 3 strings."

    print("\n--- Test 2: LLM Features ---")
    try:
        response_llm_features = ask_ollama_structured(
            model=model_name,
            prompt=prompt_llm_features,
            system_message=system_message_llm_features,
            host=ollama_host
        )
        print("Received structured response:")
        print(json.dumps(response_llm_features, indent=2))
        if 'features' in response_llm_features and isinstance(response_llm_features['features'], list):
            for i, feature in enumerate(response_llm_features['features']):
                print(f"  Feature {i+1}: {feature}")
        else:
            print(
                "Response format mismatch: 'features' key not found or not a list.")

    except Exception as e:
        print(f"❌ Error testing LLM features: {e}")

    print("\n--- Ollama Structured Response Tests Complete ---")

if __name__ == "__main__":
    # To run with a specific model or host, you can set environment variables:
    # OLLAMA_MODEL=mistral OLLAMA_HOST_URL=http://your-ollama-host:11434 python test_ollama.py
    run_ollama_tests()
