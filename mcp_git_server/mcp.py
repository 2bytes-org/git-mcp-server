"""Simple implementation of MCP (Model Context Protocol) server for Git integration."""

import sys
import json
import logging
import traceback
from jsonschema import validate
from typing import Dict, Any, List, Callable, Optional, Union

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
            request_id = request.get("id")
            method = request.get("method")
            
            logger.info(f"Handling request method: {method}, id: {request_id}")
            
            # Always include jsonrpc version and id in response
            response = {
                "jsonrpc": "2.0",
                "id": request_id
            }
            
            if method == "initialize":
                # Handle initialize request specially
                logger.info("Processing initialize request")
                response["result"] = {
                    "capabilities": {}
                }
                return response
            elif method == "mcp.get_schema":
                logger.info("Processing mcp.get_schema request")
                result = self._handle_get_schema()
                if "error" in result:
                    response["error"] = result["error"]
                else:
                    response["result"] = result["result"]
                return response
            elif method == "mcp.execute_function":
                logger.info("Processing mcp.execute_function request")
                result = self._handle_execute_function(request)
                if "error" in result:
                    response["error"] = result["error"]
                else:
                    response["result"] = result["result"]
                return response
            elif method == "notifications/cancelled":
                # Just acknowledge notification
                logger.info("Received cancellation notification")
                return response
            elif method == "shutdown":
                # Handle shutdown request
                logger.info("Processing shutdown request")
                response["result"] = None
                return response
            elif method == "exit":
                # Handle exit notification 
                logger.info("Processing exit notification")
                return response
            else:
                logger.warning(f"Unknown method requested: {method}")
                response["error"] = {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
                return response
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
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
        logger.info(f"Returning schema with {len(functions)} functions")
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
        
        logger.info(f"Executing function: {function_name} with params: {function_params}")

        function_def = self.function_registry.get_function(function_name)
        if not function_def:
            logger.warning(f"Function not found: {function_name}")
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
            logger.info(f"Function executed successfully: {function_name}")
            return {"result": result}
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            logger.error(traceback.format_exc())
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
                logger.debug("Waiting for input from stdin...")
                line = sys.stdin.readline()
                
                if not line:
                    logger.info("End of input stream detected, exiting loop")
                    break  # End of input stream
                
                logger.debug(f"Received raw input: {line.strip()}")

                # Parse the request
                request = json.loads(line)
                logger.info(f"Received request: {json.dumps(request)}")

                # Handle the request
                response = self.handle_request(request)

                # Write the response to stdout
                json_response = json.dumps(response)
                logger.info(f"Sending response: {json_response}")
                sys.stdout.write(json_response + "\n")
                sys.stdout.flush()
                
                # If this was an exit notification, break the loop
                if request.get("method") == "exit":
                    logger.info("Exit notification received, stopping server")
                    break

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON input: {str(e)}")
                sys.stdout.write(json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }) + "\n")
                sys.stdout.flush()
            
            except Exception as e:
                logger.error(f"Unexpected error in server loop: {str(e)}")
                logger.error(traceback.format_exc())
                sys.stdout.write(json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }) + "\n")
                sys.stdout.flush()