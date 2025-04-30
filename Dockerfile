FROM python:3.10-slim AS builder

WORKDIR /app

# Install git and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install the package
RUN pip install --no-cache-dir -e .

FROM python:3.10-slim

WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy installed package from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

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