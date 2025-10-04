#!/bin/bash

# generate-cert.sh
# Script to extract Zscaler certificates from the system keychain

CERT_FILE="zscaler-root-ca.crt"

if [ -f "$CERT_FILE" ]; then
  echo "Certificate file $CERT_FILE already exists."
  exit 0
fi

# For macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "Exporting Zscaler certificate from macOS keychain..."
  security find-certificate -a -c "Zscaler" -p > "$CERT_FILE"
  if [ $? -eq 0 ] && [ -s "$CERT_FILE" ]; then
    echo "Certificate exported successfully to $CERT_FILE"
  else
    echo "Failed to find Zscaler certificate in keychain."
    echo "Creating empty certificate file as placeholder. Please replace with your Zscaler certificate."
    echo "-----BEGIN CERTIFICATE-----" > "$CERT_FILE"
    echo "Add your certificate content here" >> "$CERT_FILE"
    echo "-----END CERTIFICATE-----" >> "$CERT_FILE"
  fi
else
  # For other systems, create placeholder
  echo "Creating placeholder certificate file. Please replace with your Zscaler certificate."
  echo "-----BEGIN CERTIFICATE-----" > "$CERT_FILE"
  echo "Add your certificate content here" >> "$CERT_FILE"
  echo "-----END CERTIFICATE-----" >> "$CERT_FILE"
fi

echo "You may need to modify $CERT_FILE with the correct Zscaler certificate content before building."