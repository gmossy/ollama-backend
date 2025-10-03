FROM ollama/ollama:latest

# Install CA certificates package and utilities
RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables to bypass certificate verification
ENV OLLAMA_INSECURE=true
ENV SSL_CERT_FILE=/dev/null
ENV GIT_SSL_NO_VERIFY=true
ENV NO_PROXY=localhost,127.0.0.1

# Override the entrypoint
ENTRYPOINT []

# Set simple command
CMD ["ollama", "serve"]

EXPOSE 11434

# More lenient healthcheck with longer intervals
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:11434/api/version || exit 1