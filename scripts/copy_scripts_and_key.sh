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
CURRENT_DIR=$(pwd)  # Gets the full path of the current directory

# Copy the current directory to the remote host's home directory
find "$CURRENT_DIR" -maxdepth 1 -type f -name "*.sh" -exec scp -i $SSH_KEY {} ${USERNAME}@${HOSTNAME}:~ \;


# Check if scp was successful
if [ $? -eq 0 ]; then
    echo "Successfully copied the current directory to ${USERNAME}@${HOSTNAME}'s home directory."
else
    echo "Failed to copy the current directory to the remote host."
fi

# Define local and remote key paths
LOCAL_KEY="$HOME/.ssh/yap_id_ed25519"
REMOTE_KEY="/.ssh/id_ed25519"  # Standard location for the private key on the remote server

# Check if the local private key file exists
if [ ! -f "$LOCAL_KEY" ]; then
    echo "Local SSH key $LOCAL_KEY does not exist."
    exit 2
fi

# Copy the local private key to the remote server's .ssh directory
scp "$LOCAL_KEY" "${USERNAME}@${HOSTNAME}:~${REMOTE_KEY}"

# Set permissions of the remote key to be read-write for the user only (important for SSH key security)
ssh -l "$USERNAME" "$HOSTNAME" "chmod 600 ~$REMOTE_KEY"

# Check if scp was successful
if [ $? -eq 0 ]; then
    echo "Successfully copied the SSH key to ${USERNAME}@${HOSTNAME}'s .ssh directory."
else
    echo "Failed to copy the SSH key to the remote host."
fi