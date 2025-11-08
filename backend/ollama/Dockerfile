FROM ollama/ollama:latest



# Install utilities

RUN apt-get update && \

    apt-get install -y curl ca-certificates && \

    apt-get clean && \

    rm -rf /var/lib/apt/lists/*



# Expose Ollama API port

EXPOSE 11434



# Health check

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \

    CMD curl -f http://localhost:11434/api/version || exit 1



# Start Ollama service

CMD ["serve"]