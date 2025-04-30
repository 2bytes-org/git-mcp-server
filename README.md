# MCP Git Server

A Model Context Protocol server for Git repository interaction and automation. This server provides robust tools to read, search, and manipulate Git repositories via Large Language Models.

## Features

- Seamless Git command execution through MCP
- Support for all essential Git operations (status, diff, commit, branch, etc.)
- Easy integration with Claude Desktop, VS Code, and Zed
- Reliable error handling and comprehensive logging
- Docker support for isolated and consistent environment

## Installation

### Docker Installation (Recommended)

Using Docker is the most reliable way to run MCP Git Server, as it ensures a consistent environment with all dependencies.

```bash
# Clone the repository
git clone https://github.com/2bytes-org/git-mcp-server.git
cd git-mcp-server

# Build Docker image
# Linux/macOS
./scripts/build-docker.sh

# or Windows
.\scripts\build-docker.ps1
```

For detailed Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## Configuration with Claude Desktop (Recommended Method)

### Using Docker with Claude Desktop

Add the following to your Claude Desktop configuration file:

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

Configuration file locations:
- Windows: `%APPDATA%\Claude\config.json`
- macOS: `~/Library/Application Support/Claude/config.json` 
- Linux: `~/.config/Claude/config.json`

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

## Troubleshooting

If you encounter issues with the Docker build, check the following:

1. Ensure Docker is installed and running
2. Verify that you have proper permissions to build Docker images
3. Try running the Docker build manually:
   ```bash
   docker build -t mcp/git .
   ```

For more detailed troubleshooting, check the logs:
```bash
docker logs $(docker ps -q --filter "ancestor=mcp/git")
```

## VS Code and Zed Integration

The server also works with other editors that support MCP. See the `examples` directory for configuration templates.

## License

This MCP server is licensed under the MIT License.