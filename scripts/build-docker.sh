#!/bin/bash
# Script to build the Docker image for mcp-git-server

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Build the Docker image
echo "Building Docker image for mcp-git-server..."
docker build -t mcp/git "$PROJECT_ROOT"

echo "Docker image 'mcp/git' built successfully"
echo "Usage:"
echo "  docker run --rm -i --mount type=bind,src=/path/to/repo,dst=/workspace mcp/git"