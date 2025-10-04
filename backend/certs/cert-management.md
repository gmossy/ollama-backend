To configure Docker to use your system's certificate store on macOS, follow these steps:

## Step 1: Mount the macOS Keychain Certificates to Your Container

For macOS, certificates are stored in the System Keychain. You'll need to export these and mount them to your Docker container:

1. **Export system certificates to a file**:
   Create a script to export all trusted certificates from your macOS Keychain:

```bash
#!/bin/bash
# save_certs.sh

# Create a directory for certificates
mkdir -p certs

# Export all certificates from the System keychain
security find-certificate -a -p /Library/Keychains/System.keychain > certs/system-keychain.pem

# Export certificates from the System Roots keychain
security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain > certs/system-roots.pem

# Export certificates from the login keychain (may contain Zscaler certs)
security find-certificate -a -p ~/Library/Keychains/login.keychain-db > certs/login-keychain.pem

# Combine all certificates into a single file
cat certs/system-keychain.pem certs/system-roots.pem certs/login-keychain.pem > certs/all-certs.pem

echo "Certificates exported to certs/all-certs.pem"
```

2. **Make the script executable and run it**:
```bash
chmod +x save_certs.sh
./save_certs.sh
```

## Step 2: Update your Docker Compose File

Modify your docker-compose.yml to mount the certificates into the container:

```yaml
version: '3'
services:
  ollama:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
      - ./certs/all-certs.pem:/etc/ssl/certs/ca-certificates.crt:ro
    restart: on-failure:5
    environment:
      - NO_PROXY=localhost,127.0.0.1
```

## Step 3: Update your Dockerfile

Modify your Dockerfile to use the mounted certificates:

```dockerfile
FROM ollama/ollama:latest

# Install CA certificates package and utilities
RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# We don't need to copy a certificate file since we're mounting it

EXPOSE 11434

# More lenient healthcheck with longer intervals
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:11434/api/version || exit 1

CMD ["ollama", "serve"]
```

## Step 4: Update your Makefile

Update your pull-models target to use the system certificates:

```makefile
pull-models:
	@if [ -z "$(MODELS)" ]; then \
		echo "Please specify models to pull, e.g., make pull-models MODELS='llama3 mistral'"; \
	else \
		for model in $(MODELS); do \
			echo "Pulling $$model..."; \
			docker exec -it $(CONTAINER_NAME) ollama pull $$model; \
		done; \
	fi
```

## Step 5: Rebuild and restart your container

```bash
# Stop and remove existing containers
docker stop ollama
docker rm ollama

# Rebuild and start
make build
make up
```

## Alternative Method: Use the Host Network (macOS)

On macOS, you can also try using the host network DNS settings:

```yaml
version: '3'
services:
  ollama:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    restart: on-failure:5
    network_mode: "host"  # Use host network settings (including DNS and certificates)
```

This approach uses the host's network settings, including its certificate store, but may not work as expected on macOS due to Docker Desktop's virtualization layer.

If these methods don't work, you may need to manually extract the Zscaler certificate specifically (which is more likely to work):

```bash
# Extract Zscaler certificate specifically
security find-certificate -a -c "Zscaler" -p > certs/zscaler.pem
```

Then mount that specific certificate in your docker-compose.yml.