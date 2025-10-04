#!/bin/bash

# troubleshoot.sh
# Success Checklist for Zscaler-Ollama Docker setup

CONTAINER_NAME="zscaler-ollama"
OLLAMA_PORT="11434"
OLLAMA_API_URL="http://localhost:${OLLAMA_PORT}/api/version"
CERT_FILE="zscaler-root-ca.crt"

echo "========================================"
echo "    Zscaler-Ollama Troubleshooting Checklist"
echo "========================================"
echo ""

# --- Helper functions ---
check_command() {
    if command -v "$1" &> /dev/null; then
        echo "✅ $1 is installed."
    else
        echo "❌ $1 is NOT installed. Please install it."
        ALL_GOOD=false
    fi
}

check_file_exists() {
    if [ -f "$1" ]; then
        echo "✅ File exists: $1"
    else
        echo "❌ File NOT found: $1. Ensure it's in the current directory."
        ALL_GOOD=false
    fi
}

# --- Initialize status ---
ALL_GOOD=true

# --- 1. Check Docker and Docker Compose installation ---
echo "--- Checking Docker and Docker Compose ---"
check_command docker
check_command docker-compose
echo ""

# --- 2. Check Zscaler certificate exported ---
echo "--- Checking Zscaler Certificate ---"
check_file_exists "$CERT_FILE"
echo ""

# --- 3. Check Services running ---
echo "--- Checking Docker Container Status ---"
CONTAINER_STATUS=$(docker ps -f name="$CONTAINER_NAME" --format "{{.Status}}" 2>/dev/null)
if [ -n "$CONTAINER_STATUS" ]; then
    if [[ "$CONTAINER_STATUS" == *Up* ]]; then
        echo "✅ Container '$CONTAINER_NAME' is running ($CONTAINER_STATUS)."
    else
        echo "⚠️ Container '$CONTAINER_NAME' is in state: $CONTAINER_STATUS. Check 'make logs'."
        ALL_GOOD=false
    fi
else
    echo "❌ Container '$CONTAINER_NAME' is NOT running. Run 'make up'."
    ALL_GOOD=false
fi
echo ""

# --- 4. Check API responding ---
echo "--- Checking Ollama API Response ---"
if $ALL_GOOD; then # Only check if container is presumed running
    API_RESPONSE=$(curl -s "$OLLAMA_API_URL")
    if [ $? -eq 0 ]; then
        API_VERSION=$(echo "$API_RESPONSE" | jq -r '.version' 2>/dev/null) # Attempt to parse version
        if [ -n "$API_VERSION" ] && [ "$API_VERSION" != "null" ]; then
            echo "✅ Ollama API is responding at $OLLAMA_API_URL."
            echo "   Ollama Version: $API_VERSION"
        else
            echo "❌ Ollama API is NOT responding or returned invalid JSON at $OLLAMA_API_URL. Check container logs ('make logs')."
            echo "   Raw Response: $API_RESPONSE"
            ALL_GOOD=false
        fi
    else
        echo "❌ Ollama API is NOT responding at $OLLAMA_API_URL (curl failed). Check container logs ('make logs')."
        echo "   Response: $API_RESPONSE"
        ALL_GOOD=false
    fi
else
    echo "   (Skipping API check as container is not running.)"
fi
echo ""

# --- 5. Check for Pulled Models ---
echo "--- Checking for Pulled Models ---"
if $ALL_GOOD; then # Only check if API is responding
    MODEL_LIST=$(docker exec "$CONTAINER_NAME" ollama list 2>/dev/null)
    if [ $? -eq 0 ]; then
        # Count lines, subtract 1 for the header, or look for a model-like pattern
        MODEL_COUNT=$(echo "$MODEL_LIST" | tail -n +2 | wc -l | tr -d ' ')
        if [ "$MODEL_COUNT" -gt 0 ]; then
            echo "✅ Models found:"
            echo "$MODEL_LIST"
        else
            echo "❌ No models found. Run 'make pull-models MODELS=\"llama3\"'."
            echo "   Ollama List Output:"
            echo "$MODEL_LIST"
            ALL_GOOD=false
        fi
    else
        echo "❌ Ollama command 'ollama list' failed inside container. Check container logs ('make logs')."
        echo "   Ollama List Output:"
        echo "$MODEL_LIST"
        ALL_GOOD=false
    fi
else
    echo "   (Skipping model list check as API is not responding.)"
fi
echo ""

# --- 6. Test successful (Web UI or command line) ---
echo "--- Manual Verification ---"
echo "▶️ To interact with Ollama, you can use:"
echo "   - Web UI (if configured): Open your browser to http://localhost:${OLLAMA_PORT}"
echo "   - Command Line: After pulling a model (e.g., 'make pull-models MODELS=\"llama3\"'), run:"
echo "     docker exec -it $CONTAINER_NAME ollama run llama3"
echo "   - Your application code integrated with Ollama at http://localhost:${OLLAMA_PORT}"
echo ""

# --- Final Summary ---
echo "========================================"
if $ALL_GOOD; then
    echo "✅ All automated checks PASSED. Your Zscaler-Ollama setup appears healthy!"
else
    echo "❌ Some checks FAILED. Please review the output above and try to resolve the issues."
fi
echo "========================================"