#!/bin/bash

# Check if there are two command line arguments provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <repository-url>"
    exit 1
fi

# Assign command line arguments to variables
REPO_URL="$1"
SSH_DIR="$HOME/.ssh"
REPO_DIR="$HOME/src"

# Start the ssh-agent in the background and add the private key
eval "$(ssh-agent -s)"
ssh-add "$SSH_DIR/id_ed25519"

# Clone the repository to the desired directory
git clone "$REPO_URL" "$REPO_DIR"
