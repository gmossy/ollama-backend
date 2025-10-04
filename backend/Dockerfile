FROM ollama/ollama:latest

# Install CA certificates package and utilities
RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Zscaler certificate if it exists in the build context
# This is preferred if the certificate doesn't change often
COPY zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/zscaler-root-ca.crt && \
    update-ca-certificates

# Set environment variables to explicitly disable verification as a fallback
ENV OLLAMA_INSECURE=true
ENV SSL_CERT_FILE=/dev/null
ENV GIT_SSL_NO_VERIFY=true
ENV NO_PROXY=localhost,127.0.0.1

EXPOSE 11434

# More lenient healthcheck with longer intervals
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:11434/api/version || exit 1

CMD ["serve"]