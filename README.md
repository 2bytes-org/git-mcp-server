# MCP Git Server

A Model Context Protocol server for Git repository interaction and automation. This server provides robust tools to read, search, and manipulate Git repositories via Large Language Models.

## Features

- Seamless Git command execution through MCP
- Support for all essential Git operations (status, diff, commit, branch, etc.)
- Easy integration with Claude Desktop, VS Code, and Zed
- Reliable error handling and comprehensive logging
- Docker support for isolated and consistent environment

## Installation

### Standard Installation

#### Using pip

```bash
pip install mcp-git-server
```

#### Using uv

```bash
uv install mcp-git-server
```

Or run directly:

```bash
uvx mcp-git-server
```

### Docker Installation (Recommended for Claude Desktop)

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker setup instructions.

Quick setup:

```bash
# Clone the repository
git clone https://github.com/2bytes-org/git-mcp-server.git
cd git-mcp-server

# Build Docker image
./scripts/build-docker.sh  # or .\scripts\build-docker.ps1 on Windows

# Configure Claude Desktop
# Add Docker configuration to Claude Desktop config.json
```

## Configuration

### Usage with Claude Desktop

#### Standard Installation

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "git": {
      "command": "mcp-git-server"
    }
  }
}
```

#### Docker Installation (Recommended)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,src=${workspaceFolder},dst=/workspace",
        "mcp/git"
      ]
    }
  }
}
```

### Usage with VS Code

Add to your User Settings (JSON) or `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "git": {
        "command": "mcp-git-server"
      }
    }
  }
}
```

### Usage with Zed

Add to your Zed `settings.json`:

```json
"context_servers": {
  "mcp-git-server": {
    "command": {
      "path": "mcp-git-server"
    }
  }
},
```

## Available Commands

- `git_status`: Shows the working tree status
- `git_diff_unstaged`: Shows changes in working directory not yet staged
- `git_diff_staged`: Shows changes that are staged for commit
- `git_diff`: Shows differences between branches or commits
- `git_commit`: Records changes to the repository
- `git_add`: Adds file contents to the staging area
- `git_reset`: Unstages all staged changes
- `git_log`: Shows the commit logs
- `git_create_branch`: Creates a new branch
- `git_checkout`: Switches branches
- `git_show`: Shows the contents of a commit
- `git_init`: Initializes a Git repository

## Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/2bytes-org/git-mcp-server.git
cd git-mcp-server
pip install -e ".[dev]"
```

Run tests:

```bash
python run_tests.py
```

## License

This MCP server is licensed under the MIT License.