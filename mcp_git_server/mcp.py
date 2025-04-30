"""Simple implementation of MCP (Model Context Protocol) server for Git integration."""

import sys
import json
import logging
from jsonschema import validate
from typing import Dict, Any, List, Callable, Optional

logger = logging.getLogger(__name__)

class FunctionDefinition:
    """Defines a function that can be called via MCP."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable[[Dict[str, Any]], Any]
    ):
        """Initialize function definition."""
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        """Convert function definition to dictionary for schema response."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

class FunctionRegistry:
    """Registry for functions that can be called via MCP."""

    def __init__(self):
        """Initialize registry."""
        self.functions: List[FunctionDefinition] = []
        self.functions_by_name: Dict[str, FunctionDefinition] = {}

    def register(self, function_def: FunctionDefinition) -> None:
        """Register a function."""
        self.functions.append(function_def)
        self.functions_by_name[function_def.name] = function_def

    def get_function(self, name: str) -> Optional[FunctionDefinition]:
        """Get a function by name."""
        return self.functions_by_name.get(name)

class Server:
    """MCP server implementation."""

    def __init__(self) -> None:
        """Initialize server."""
        self.function_registry: Optional[FunctionRegistry] = None

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP request."""
        try:
            method = request.get("method")
            if method == "mcp.get_schema":
                return self._handle_get_schema()
            elif method == "mcp.execute_function":
                return self._handle_execute_function(request)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    def _handle_get_schema(self) -> Dict[str, Any]:
        """Handle the get_schema request."""
        if not self.function_registry:
            return {
                "error": {
                    "code": -32603,
                    "message": "Function registry not initialized"
                }
            }

        functions = [f.to_dict() for f in self.function_registry.functions]
        return {
            "result": {
                "functions": functions
            }
        }

    def _handle_execute_function(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the execute_function request."""
        if not self.function_registry:
            return {
                "error": {
                    "code": -32603,
                    "message": "Function registry not initialized"
                }
            }

        params = request.get("params", {})
        function_name = params.get("name")
        function_params = params.get("parameters", {})

        function_def = self.function_registry.get_function(function_name)
        if not function_def:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Function not found: {function_name}"
                }
            }

        try:
            # Validate parameters against the schema
            validate(instance=function_params, schema=function_def.parameters)
            result = function_def.function(function_params)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Error executing function: {str(e)}"
                }
            }

    def start_loop(self) -> None:
        """Start the server loop, reading requests from stdin and writing responses to stdout."""
        logger.info("Starting MCP server loop")
        
        while True:
            try:
                # Read a line from stdin
                line = sys.stdin.readline()
                if not line:
                    break  # End of input stream

                # Parse the request
                request = json.loads(line)
                logger.debug(f"Received request: {request}")

                # Handle the request
                response = self.handle_request(request)

                # Write the response to stdout
                json_response = json.dumps(response)
                sys.stdout.write(json_response + "\n")
                sys.stdout.flush()
                logger.debug(f"Sent response: {response}")

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON input: {str(e)}")
                sys.stdout.write(json.dumps({
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }) + "\n")
                sys.stdout.flush()
            
            except Exception as e:
                logger.error(f"Unexpected error in server loop: {str(e)}")
                sys.stdout.write(json.dumps({
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }) + "\n")
                sys.stdout.flush()