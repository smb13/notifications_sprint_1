#!/bin/bash

# Check if the hostname is provided as a command-line argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <hostname>"
    exit 1
fi

# Assign command line argument to variable
HOSTNAME=$1

# Define username and SSH key path
USERNAME="yap-student"
SSH_KEY="~/.ssh/yap_id_ed25519"

# Open the remote host's SSH session
ssh -i $SSH_KEY "${USERNAME}@${HOSTNAME}"
