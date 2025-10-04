import ollama
import json
from typing import Dict, Any, Optional

def ask_ollama_structured(
    model: str,
    prompt: str,
    system_message: Optional[str] = None,
    host: str = 'http://localhost:11434'
) -> Dict[str, Any]:
    """
    Connects to an Ollama LLM and generates a structured (JSON) response.

    Args:
        model (str): The name of the Ollama model to use (e.g., 'llama3', 'mistral').
                     Ensure this model is available in your Ollama instance.
        prompt (str): The user's prompt or question.
        system_message (str, optional): A system message to guide the model's behavior,
                                        e.g., instructing it to format output as JSON.
                                        If None, a default message instructing JSON output is used.
        host (str, optional): The Ollama API host URL. Defaults to 'http://localhost:11434'.

    Returns:
        dict: The parsed JSON response from the Ollama model.

    Raises:
        ollama.ResponseError: If there's an issue connecting to Ollama or generating a response.
        json.JSONDecodeError: If the model's response is not valid JSON.
    """
    client = ollama.Client(host=host)

    # Default system message to enforce JSON output if none provided
    if system_message is None:
        system_message = "You are a helpful assistant. Provide your answer in JSON format."

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': prompt}
    ]

    # Request JSON format from Ollama
    response_raw = client.chat(
        model=model,
        messages=messages,
        format='json'
    )

    # Ollama returns the JSON in the 'message.content' key as a string
    response_content = response_raw.get('message', {}).get('content', '{}')

    try:
        return json.loads(response_content)
    except json.JSONDecodeError as e:
        print(
            f"Warning: Model response was not valid JSON. Raw response: {response_content}")
        raise e

if __name__ == '__main__':
    # Example of how to run this file directly for a quick test
    # Ensure 'llama3' model is pulled in your Ollama instance
    example_model = 'llama3'
    example_prompt = "Tell me a short story about a brave knight named Sir Reginald, summarizing the plot and listing the main characters."
    example_system_message = "Your response must be in JSON format with keys 'title', 'summary', and 'characters' (a list of strings)."

    try:
        print(f"Attempting to query model: {example_model}")
        structured_story = ask_ollama_structured(
            model=example_model,
            prompt=example_prompt,
            system_message=example_system_message
        )
        print("\n--- Structured Story Response ---")
        print(json.dumps(structured_story, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
