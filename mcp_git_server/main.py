"""Main entry point for MCP Git Server."""

import logging
import sys
import json
from typing import Dict, Any, List, Optional
from model_context_protocol import Server, FunctionRegistry, FunctionDefinition

from mcp_git_server.git_operations import GitOperations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def register_functions(server: Server) -> None:
    """Register Git operations as MCP functions."""
    registry = FunctionRegistry()
    
    # git_status
    registry.register(
        FunctionDefinition(
            name="git_status",
            description="Shows the working tree status",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_status(**params)
        )
    )
    
    # git_diff_unstaged
    registry.register(
        FunctionDefinition(
            name="git_diff_unstaged",
            description="Shows changes in working directory not yet staged",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_diff_unstaged(**params)
        )
    )
    
    # git_diff_staged
    registry.register(
        FunctionDefinition(
            name="git_diff_staged",
            description="Shows changes that are staged for commit",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_diff_staged(**params)
        )
    )
    
    # git_diff
    registry.register(
        FunctionDefinition(
            name="git_diff",
            description="Shows differences between branches or commits",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "target": {
                        "type": "string",
                        "description": "Target branch or commit to compare with"
                    }
                },
                "required": ["repo_path", "target"]
            },
            function=lambda params: GitOperations.git_diff(**params)
        )
    )
    
    # git_commit
    registry.register(
        FunctionDefinition(
            name="git_commit",
            description="Records changes to the repository",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "message": {
                        "type": "string",
                        "description": "Commit message"
                    }
                },
                "required": ["repo_path", "message"]
            },
            function=lambda params: GitOperations.git_commit(**params)
        )
    )
    
    # git_add
    registry.register(
        FunctionDefinition(
            name="git_add",
            description="Adds file contents to the staging area",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of file paths to stage"
                    }
                },
                "required": ["repo_path", "files"]
            },
            function=lambda params: GitOperations.git_add(**params)
        )
    )
    
    # git_reset
    registry.register(
        FunctionDefinition(
            name="git_reset",
            description="Unstages all staged changes",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_reset(**params)
        )
    )
    
    # git_log
    registry.register(
        FunctionDefinition(
            name="git_log",
            description="Shows the commit logs",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "max_count": {
                        "type": "number",
                        "description": "Maximum number of commits to show (default: 10)"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_log(**params)
        )
    )
    
    # git_create_branch
    registry.register(
        FunctionDefinition(
            name="git_create_branch",
            description="Creates a new branch",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Name of the new branch"
                    },
                    "start_point": {
                        "type": "string",
                        "description": "Starting point for the new branch"
                    }
                },
                "required": ["repo_path", "branch_name"]
            },
            function=lambda params: GitOperations.git_create_branch(**params)
        )
    )
    
    # git_checkout
    registry.register(
        FunctionDefinition(
            name="git_checkout",
            description="Switches branches",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Name of branch to checkout"
                    }
                },
                "required": ["repo_path", "branch_name"]
            },
            function=lambda params: GitOperations.git_checkout(**params)
        )
    )
    
    # git_show
    registry.register(
        FunctionDefinition(
            name="git_show",
            description="Shows the contents of a commit",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to Git repository"
                    },
                    "revision": {
                        "type": "string",
                        "description": "The revision (commit hash, branch name, tag) to show"
                    }
                },
                "required": ["repo_path", "revision"]
            },
            function=lambda params: GitOperations.git_show(**params)
        )
    )
    
    # git_init
    registry.register(
        FunctionDefinition(
            name="git_init",
            description="Initializes a Git repository",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to directory to initialize git repo"
                    }
                },
                "required": ["repo_path"]
            },
            function=lambda params: GitOperations.git_init(**params)
        )
    )
    
    server.function_registry = registry

def main() -> None:
    """Main entry point for the MCP Git Server."""
    logger.info("Starting MCP Git Server...")
    
    server = Server()
    register_functions(server)
    
    try:
        server.start_loop()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()