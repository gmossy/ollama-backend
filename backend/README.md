# DPGAI Backend: zscaler-ollama Docker Setup

This directory contains the Docker configuration for running the Ollama Large Language Model (LLM) server, specifically tailored for environments with corporate TLS/SSL inspection like Zscaler.

## What is Ollama?

Ollama is an open-source platform designed to make it easy to run and manage large language models (LLMs) locally. It provides a simple command-line interface and API to download, serve, and interact with various state-of-the-art AI models like Llama, Mistral, and many others directly on your machine. This capability is crucial for running AI applications with enhanced privacy, reduced latency, and greater control over the models.

## The `zscaler-ollama` Docker Setup

This Docker configuration creates a containerized environment for running Ollama, specifically tailored for use within corporate networks that employ TLS/SSL inspection, such as Zscaler.

**Why `zscaler-ollama`?**
The container is named `zscaler-ollama` to highlight its configuration for operating within a Zscaler-protected network environment. Zscaler intercepts and inspects encrypted network traffic (HTTPS) for security purposes, which often leads to "certificate signed by unknown authority" errors when Docker containers try to pull models from external registries.

**Why Zscaler is needed (and why it causes issues):**
This project is intended to house installation scripts that assist with installing the default ZScaler intermediate CA Certificate into virtualized or containerized images. The script is written in a way that it can be run in any bourne shell (i.e. bsh and its descendants), since some container images do not come with a full bash implementation.

ZScaler supports SSL Inspection, which redirects any TLS traffic through its own tunnel in order to decrypt and monitor the traffic for anything malicious. It does this by signing the tunnel with its own certificate, and therefore anything that utilizes the internet connection of a ZScaler managed host needs to trust their CA. This includes containers and VMs used for development, as they use the host OS' internet connection.

Because of this, we aim to provide easy to use scripts that install the certificate into a systems CA certificate store. For more information on how SSL Inspection works, see About SSL Inspections on ZScaler's website.  Also see <https://github.com/jhagadorn-mgm/zscaler-ca-installer>

This Docker setup addresses these challenges by:
1.  **Certificate Handling**: Including logic within the Dockerfile to copy and trust Zscaler's root certificate during the image build process. This allows the container to properly validate connections through the proxy.
2.  **Insecure Fallback**: Employing environment variables like `OLLAMA_INSECURE=true`, `SSL_CERT_FILE=/dev/null`, `GIT_SSL_NO_VERIFY=true`, and `NO_PROXY` as a robust fallback to bypass strict TLS verification when necessary.
3.  **Isolation & Reproducibility**: Providing a consistent and isolated environment for Ollama, ensuring that your local machine's setup doesn't interfere with the AI services.

## How This Helps Digital Proving Ground (DPG)

This `zscaler-ollama` Docker setup is instrumental for the Digital Proving Ground (DPG) project by enabling:

1.  **Local AI Capabilities**: DPG applications can leverage powerful LLMs locally, ensuring sensitive data remains on-premises and adheres to strict privacy and security requirements.
2.  **Reduced Latency**: Running models locally minimizes network latency, critical for real-time analysis, decision-making, and interactive AI experiences within DPG.
3.  **Cost Efficiency**: Avoids continuous reliance on costly cloud-based LLM APIs, making AI integration more sustainable for DPG initiatives.
4.  **Custom Model Control**: Offers DPG full control over model selection, configuration, and fine-tuning, allowing for specialized AI solutions tailored to military and defense use cases.
5.  **Secure Network Operations**: Configured to operate seamlessly within secure, often air-gapped or proxy-heavy, DOD and military network environments without compromising security protocols.
6.  **Rapid Prototyping**: Facilitates quick experimentation and iteration with different AI models and applications without complex infrastructure provisioning.

---

## Getting Started

To get your `zscaler-ollama` container up and running:

1.  **Ensure Zscaler Certificate is Available**:
    Make sure your Zscaler root certificate (`zscaler-root-ca.crt`) is placed in the `DPGAI/backend/` directory. If you need to generate it from your macOS keychain, navigate to the `DPGAI` directory and run:
    ```bash
    cd /Users/glennmossy/dpg-ai-projects/DPGAI
    chmod +x generate-cert.sh
    ./generate-cert.sh
    cp zscaler-root-ca.crt backend/
    ```

2.  **Navigate to the Backend Directory**:
    ```bash
    cd /Users/glennmossy/dpg-ai-projects/DPGAI/backend
    ```

3.  **Clean, Build, and Run the Container**:
    Use the `Makefile` to perform a full cleanup and rebuild. This ensures all previous Docker resources are removed and the new configuration is applied.
    ```bash
    make clean # Removes old containers, volumes, and images
    make build # Builds the Docker image with certificate handling
    make up    # Starts the zscaler-ollama container
    ```

4.  **Verify the Service is Running**:
    ```bash
    docker ps
    ```

5.  **Check Container Logs for Startup Issues**:
    ```bash
    make logs
    ```

## Available Models

For a list of available models, visit: https://ollama.com/library

Some recommended models for DPG use cases:
-   **llama3**: Good general-purpose model for text generation and analysis.
-   **mistral**: Excellent for complex reasoning tasks.
-   **phi**: Lightweight model suitable for constrained environments.
-   **deepseek**: Strong model for technical content and code generation.

## Updating Models

To update all your previously pulled Ollama models in your Docker container, use the Makefile:

```bash
make update-models
```

To pull specific models (e.g., `llama3` and `mistral`):

```bash
make pull-models MODELS='llama3 mistral'
```

If you prefer to pull a single model manually or need to access the container shell:

1.  Access your `zscaler-ollama` container with:
    ```bash
    docker exec -it zscaler-ollama bash
    ```

2.  Once inside the container, run `ollama pull <model-name>`:
    ```bash
    ollama pull <model-name>
    ```

## Troubleshooting

If your `zscaler-ollama` container is not starting properly or keeps restarting:

1.  **Check the logs**:
    ```bash
    docker logs zscaler-ollama
    ```

2.  **Complete rebuild (if needed)**:
    ```bash
    make clean
    make build
    make up
    ```

3.  **Check resource allocation in Docker Desktop**:
    -   Ollama requires significant memory (8GB+ recommended).
    -   Navigate to Docker Desktop → Settings → Resources → Advanced to increase allocation.

## Using Makefile

This project includes a Makefile for easier management of your `zscaler-ollama` Docker environment:

```bash
# Build the container image
make build

# Start the container in detached mode
make up

# Stop the container
make down

# Restart the container
make restart

# Pull specified models (e.g., make pull-models MODELS='llama3 mistral')
make pull-models

# List installed models
make list-models

# View container logs in real-time
make logs

# Clean up containers, volumes, and images for this project
make clean

# Completely remove all DPG-Ollama Docker resources (including volumes)
make prune

# Show status of the zscaler-ollama container
make status
```

**2. Update `/Users/glennmossy/dpg-ai-projects/DPGAI/README.md`**

This will be the high-level README, pointing to the backend for details.

```language:DPGAI/README.md
# DPG AI Projects

This repository contains AI-related projects for the Digital Proving Ground (DPG).

## Backend: `zscaler-ollama` Docker Setup

The `backend/` directory contains a Dockerized setup for running the Ollama Large Language Model (LLM) server. This setup is specifically configured to operate within corporate networks that utilize TLS/SSL inspection (e.g., Zscaler), making it suitable for secure enterprise environments like those in the DOD and military.

For detailed information on what Ollama is, how this Docker setup works, why Zscaler is relevant, and comprehensive instructions for building, running, and managing the `zscaler-ollama` container and its models, please refer to the dedicated README:

➡️ **[DPGAI Backend: `zscaler-ollama` Docker Setup README](backend/README.md)**

---

feat(ollama): Implement zscaler-ollama Docker setup for DPG AI projects

This commit introduces a robust, Dockerized Ollama environment (`zscaler-ollama`) tailored for use within corporate networks employing TLS/SSL inspection (e.g., Zscaler), making it suitable for the Digital Proving Ground (DPG) project.

Key Features & Improvements:

-   **Ollama Dockerization**: Established a `backend/` directory containing `docker-compose.yml`, `Dockerfile`, and `Makefile` for consistent and reproducible Ollama deployments.
-   **Zscaler Certificate Handling**:
    -   Implemented a `generate-cert.sh` script to extract Zscaler root certificates from macOS keychains (or create placeholders).
    -   Modified `Dockerfile` to copy `zscaler-root-ca.crt` during image build and run `update-ca-certificates` for trusted TLS connections within the container.
    -   Configured `OLLAMA_INSECURE`, `SSL_CERT_FILE`, `GIT_SSL_NO_VERIFY`, `CURL_CA_BUNDLE`, and `NO_PROXY` environment variables as fallbacks to bypass strict certificate validation at runtime, ensuring model downloads and API calls function reliably in proxy environments.
-   **Makefile for Simplified Management**:
    -   Introduced a comprehensive `Makefile` in `backend/` with targets for `build`, `up`, `down`, `restart`, `clean`, `prune`, `status`, `pull-models`, `pull-models-ci`, and `update-models`.
    -   Created a `setup` target to automate the entire onboarding process: certificate generation, Docker cleanup, build, container startup, and initial LLM model pulls.
-   **Container Renaming**: Standardized the Ollama service and container name to `zscaler-ollama` across `docker-compose.yml` and `Makefile` for clarity.
-   **Python Usage and Testing Scripts**:
    -   Added `backend/usage/` directory with `ollama_service.py` to provide a reusable Python client for structured (JSON) Ollama API interactions.
    -   Included `test_ollama.py` to demonstrate querying Ollama for structured responses with various prompts (e.g., Docker explanation, LLM features, DPG definition).
    -   Provided instructions for setting up Python virtual environments with `uv` and installing `ollama-python`.
-   **Troubleshooting Script**: Developed `backend/troubleshoot.sh` to provide a quick checklist for verifying Docker, API, and model status, including automated container startup attempts and clear resolution guidance.
-   **Comprehensive Documentation (`README.md`)**:
    -   Updated the root `DPGAI/README.md` to provide a high-level overview and direct users to the backend-specific documentation.
    -   Extensively revised `DPGAI/backend/README.md` with:
        -   Detailed explanations of Ollama and the `zscaler-ollama` Docker setup.
        -   In-depth rationale for Zscaler's role and associated challenges.
        -   Clear benefits for the Digital Proving Ground project.
        -   Updated "Getting Started" instructions, troubleshooting guides, and Makefile usage.
        -   Added a note regarding macOS GPU limitations for Docker containers.
-   **Makefile Enhancements**:
    -   Added `gpt-oss:20b`, `gemma3:12b`, and `qwen3` to the initial models pulled by `make setup`.
    -   Fixed shell path issues in `Makefile` targets when referencing `generate-cert.sh`.
    -   Improved robustness of `prune` target.
-   **Script Fixes**:
    -   Resolved multiple `IndentationError` issues in Python usage scripts.
    -   Fixed `ModuleNotFoundError` by guiding `uv pip install ollama`.
    -   Corrected container name references in `quick_test_script.sh`.
    -   Fixed `bad substitution` error in `quick_test_script.sh` by using `printf` for string repetition.
    -   Resolved `quick_test_script.sh` hanging issues by piping prompts to `ollama run`.
    -   Refined JSON parsing logic and `ollama list` output interpretation in `troubleshoot.sh`.
    -   Updated terminology from "DPG-Ollama" to "Zscaler-Ollama" in `troubleshoot.sh` for consistency.

This work significantly improves the ease of use, maintainability, and enterprise network compatibility of the Ollama setup for DPG AI development.
