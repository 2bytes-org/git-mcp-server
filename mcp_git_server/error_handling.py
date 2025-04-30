"""Error handling module for MCP Git Server."""

import logging
import traceback
import sys
from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])

def handle_git_errors(func: F) -> F:
    """Decorator to handle Git operation errors gracefully."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Value error in {func.__name__}: {str(e)}")
            return {"error": str(e), "type": "ValueError"}
        except FileNotFoundError as e:
            logger.error(f"File not found in {func.__name__}: {str(e)}")
            return {"error": str(e), "type": "FileNotFoundError"}
        except PermissionError as e:
            logger.error(f"Permission error in {func.__name__}: {str(e)}")
            return {"error": str(e), "type": "PermissionError"}
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.debug(traceback.format_exc())
            return {
                "error": str(e),
                "type": type(e).__name__,
                "trace": traceback.format_exc() if logger.level <= logging.DEBUG else None
            }
    return cast(F, wrapper)

def setup_exception_handling() -> None:
    """Set up global exception handling."""
    def exception_handler(exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Handle uncaught exceptions."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = exception_handler