"""Logging configuration for MCP Git Server."""

import os
import logging
import logging.handlers
from typing import Dict, Any, Optional

from mcp_git_server.config import config

def setup_logging() -> None:
    """Set up logging for the MCP Git Server."""
    # Get log level from config
    log_level_name = config.get("log_level", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # File handler
    try:
        log_dir = os.path.join(os.path.expanduser("~"), ".logs", "mcp-git-server")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "mcp-git-server.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # Don't fail if file logging isn't available
        console_handler.setLevel(logging.DEBUG)
        root_logger.warning(f"Could not set up file logging: {str(e)}")
    
    # Set GitPython logger level to be less verbose
    logging.getLogger("git").setLevel(logging.WARNING)
    
    # Log startup info
    root_logger.info(f"MCP Git Server logging initialized at level {log_level_name}")