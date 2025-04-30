"""Configuration module for MCP Git Server."""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "log_level": "INFO",
    "allowed_repos": [],  # Empty means all repos are allowed
    "max_diff_size": 1024 * 1024,  # 1MB
    "max_log_entries": 100
}

class Config:
    """Configuration handler for MCP Git Server."""
    
    def __init__(self) -> None:
        """Initialize configuration with defaults."""
        self.config_path = self._get_config_path()
        self.config = self._load_config()
    
    def _get_config_path(self) -> str:
        """Get the configuration file path."""
        config_dir = os.environ.get(
            "MCP_GIT_CONFIG_DIR",
            os.path.join(os.path.expanduser("~"), ".config", "mcp-git-server")
        )
        
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except Exception as e:
                logger.warning(f"Could not create config directory: {str(e)}")
        
        return os.path.join(config_dir, "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if not os.path.exists(self.config_path):
            logger.info(f"No configuration file found at {self.config_path}. Using defaults.")
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Add any missing default values
            updated = False
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
                    updated = True
            
            if updated:
                self._save_config(config)
            
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}. Using defaults.")
            return DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value and save."""
        self.config[key] = value
        return self._save_config(self.config)
    
    def is_repo_allowed(self, repo_path: str) -> bool:
        """Check if a repository path is allowed."""
        allowed_repos = self.get("allowed_repos", [])
        
        # If no repos are specified, all are allowed
        if not allowed_repos:
            return True
        
        # Check if path is in allowed repos
        normalized_path = os.path.normpath(os.path.abspath(repo_path))
        for allowed_repo in allowed_repos:
            allowed_normalized = os.path.normpath(os.path.abspath(allowed_repo))
            
            # Direct match
            if normalized_path == allowed_normalized:
                return True
            
            # Check if it's a subdirectory of an allowed repo
            if normalized_path.startswith(allowed_normalized + os.sep):
                return True
        
        return False

# Global configuration instance
config = Config()