FROM python:3.10-slim

WORKDIR /app

# Install git and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install required dependencies directly
RUN pip install --no-cache-dir gitpython>=3.1.0 pydantic>=2.0.0 jsonschema>=4.0.0

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Create a non-root user to run the service
RUN useradd -m -u 1000 mcpuser && \
    mkdir -p /home/mcpuser/.config/mcp-git-server && \
    chown -R mcpuser:mcpuser /home/mcpuser

# Set the working directory to /workspace which will be mounted
WORKDIR /workspace

# Create a directory for accessing user Git repositories
RUN mkdir -p /projects && chown -R mcpuser:mcpuser /projects

USER mcpuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_GIT_CONFIG_DIR=/home/mcpuser/.config/mcp-git-server

# The MCP server operates on stdin/stdout
ENTRYPOINT ["mcp-git-server"]