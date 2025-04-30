"""Utility functions for MCP Git Server."""

import os
import logging
import platform
import subprocess
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger(__name__)

def get_system_info() -> Dict[str, str]:
    """Get system information for debugging."""
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
        "processor": platform.processor()
    }
    
    # Get Git version
    try:
        git_version = subprocess.check_output(["git", "--version"]).decode("utf-8").strip()
        info["git_version"] = git_version
    except Exception as e:
        info["git_version"] = f"Error getting Git version: {str(e)}"
    
    return info

def normalize_path(path: str) -> str:
    """Normalize a file path."""
    return os.path.normpath(os.path.abspath(os.path.expanduser(path)))

def is_git_repository(path: str) -> bool:
    """Check if a directory is a Git repository."""
    git_dir = os.path.join(path, ".git")
    return os.path.isdir(git_dir)

def find_git_root(path: str) -> Optional[str]:
    """Find the Git repository root from a path."""
    current_path = normalize_path(path)
    
    while current_path and current_path != os.path.dirname(current_path):
        if is_git_repository(current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    
    return None

def truncate_diff(diff_output: str, max_size: int = 1024 * 1024) -> str:
    """Truncate a diff output if it's too large."""
    if len(diff_output) <= max_size:
        return diff_output
    
    # Calculate the size to truncate to (half the max size)
    truncate_size = max_size // 2
    
    # Truncate both the beginning and end
    beginning = diff_output[:truncate_size]
    ending = diff_output[-truncate_size:]
    
    message = f"\n\n... [TRUNCATED: {len(diff_output) - max_size} bytes] ...\n\n"
    
    return beginning + message + ending

def parse_git_url(url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Parse a Git URL into components (hostname, owner, repo)."""
    # Handle SSH URLs (e.g., git@github.com:user/repo.git)
    if "@" in url and ":" in url.split("@")[1]:
        try:
            host_part, path_part = url.split("@")[1].split(":", 1)
            path_parts = path_part.rstrip(".git").split("/")
            if len(path_parts) >= 2:
                return host_part, path_parts[0], path_parts[1]
            else:
                return host_part, path_parts[0], None
        except Exception:
            pass
    
    # Handle HTTPS URLs (e.g., https://github.com/user/repo.git)
    try:
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").rstrip(".git").split("/")
        
        if len(path_parts) >= 2:
            return parsed.netloc, path_parts[0], path_parts[1]
        else:
            return parsed.netloc, path_parts[0] if path_parts else None, None
    except Exception:
        return None, None, None