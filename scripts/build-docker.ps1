# PowerShell script to build the Docker image for mcp-git-server

# Get the directory where the script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Build the Docker image
Write-Host "Building Docker image for mcp-git-server..."
docker build -t mcp/git $ProjectRoot

Write-Host "Docker image 'mcp/git' built successfully"
Write-Host "Usage:"
Write-Host "  docker run --rm -i --mount type=bind,src=C:/path/to/repo,dst=/workspace mcp/git"