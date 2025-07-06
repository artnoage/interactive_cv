#!/usr/bin/env python3
"""
MCP Client Implementation

A client that can connect to MCP servers and use their tools.
"""

import json
import sys
import subprocess
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """Represents a tool available from an MCP server"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPClient:
    """Client for connecting to MCP servers"""
    
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.process = None
        self.tools: List[Tool] = []
        self.initialized = False
        self.request_id = 0
    
    def get_next_request_id(self) -> int:
        """Get next request ID"""
        self.request_id += 1
        return self.request_id
    
    async def start_server(self):
        """Start the MCP server process"""
        try:
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            logger.info(f"Started MCP server: {' '.join(self.server_command)}")
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    async def send_request(self, method: str, params: Dict = None) -> Dict:
        """Send a request to the MCP server"""
        if not self.process:
            raise RuntimeError("Server not started")
        
        request = {
            "jsonrpc": "2.0",
            "id": self.get_next_request_id(),
            "method": method,
            "params": params or {}
        }
        
        request_json = json.dumps(request) + "\n"
        
        try:
            self.process.stdin.write(request_json.encode())
            await self.process.stdin.drain()
            
            response_line = await self.process.stdout.readline()
            if not response_line:
                raise RuntimeError("No response from server")
            
            response = json.loads(response_line.decode().strip())
            
            if "error" in response:
                raise RuntimeError(f"Server error: {response['error']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending request: {e}")
            raise
    
    async def initialize(self) -> bool:
        """Initialize the MCP connection"""
        try:
            response = await self.send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "mcp-client",
                    "version": "1.0.0"
                }
            })
            
            # The server returns the response directly, not wrapped in "result"
            if "protocolVersion" in response:
                logger.info("Successfully initialized MCP connection")
                self.initialized = True
                return True
            else:
                logger.error("Failed to initialize connection")
                return False
                
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            return False
    
    async def list_tools(self) -> List[Tool]:
        """List available tools from the server"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        try:
            response = await self.send_request("tools/list")
            
            if "tools" in response:
                self.tools = []
                for tool_data in response["tools"]:
                    tool = Tool(
                        name=tool_data["name"],
                        description=tool_data["description"],
                        input_schema=tool_data.get("inputSchema", {})
                    )
                    self.tools.append(tool)
                
                logger.info(f"Found {len(self.tools)} tools")
                return self.tools
            else:
                logger.error("No tools found in response")
                return []
                
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Call a tool on the server"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        try:
            response = await self.send_request("tools/call", {
                "name": tool_name,
                "arguments": arguments
            })
            
            if "content" in response:
                return response
            else:
                logger.error(f"Tool call failed: {response}")
                return {"error": "Tool call failed"}
                
        except Exception as e:
            logger.error(f"Error calling tool: {e}")
            return {"error": str(e)}
    
    async def stop_server(self):
        """Stop the MCP server"""
        if self.process:
            try:
                self.process.terminate()
                await self.process.wait()
                logger.info("MCP server stopped")
            except Exception as e:
                logger.error(f"Error stopping server: {e}")
    
    def get_tool_by_name(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None


class SequentialThinkingClient:
    """High-level client for sequential thinking"""
    
    def __init__(self, server_command: List[str]):
        self.mcp_client = MCPClient(server_command)
        self.current_thought_number = 0
        self.total_thoughts_estimate = 0
    
    async def start(self):
        """Start the client and initialize connection"""
        await self.mcp_client.start_server()
        await self.mcp_client.initialize()
        await self.mcp_client.list_tools()
        
        # Verify sequential thinking tool is available
        tool = self.mcp_client.get_tool_by_name("sequential_thinking")
        if not tool:
            raise RuntimeError("Sequential thinking tool not found")
        
        logger.info("Sequential thinking client ready")
    
    async def think(
        self, 
        thought: str, 
        next_thought_needed: bool = True,
        total_thoughts: int = 5,
        is_revision: bool = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None
    ) -> Dict:
        """Add a thought to the sequence"""
        
        if not is_revision:
            self.current_thought_number += 1
        
        if total_thoughts > self.total_thoughts_estimate:
            self.total_thoughts_estimate = total_thoughts
        
        arguments = {
            "thought": thought,
            "nextThoughtNeeded": next_thought_needed,
            "thoughtNumber": self.current_thought_number,
            "totalThoughts": self.total_thoughts_estimate
        }
        
        if is_revision:
            arguments["isRevision"] = True
            if revises_thought:
                arguments["revisesThought"] = revises_thought
        
        if branch_from_thought:
            arguments["branchFromThought"] = branch_from_thought
        
        if branch_id:
            arguments["branchId"] = branch_id
        
        result = await self.mcp_client.call_tool("sequential_thinking", arguments)
        return result
    
    async def stop(self):
        """Stop the client"""
        await self.mcp_client.stop_server()


async def main():
    """Example usage of the MCP client"""
    
    # Server command - adjust path as needed
    server_command = [
        "python", 
        "/home/artnoage/Projects/interactive_cv/mcp_experiment/server/sequential_thinking_server.py"
    ]
    
    client = SequentialThinkingClient(server_command)
    
    try:
        await client.start()
        
        # Example sequential thinking session
        problem = "Plan a marketing strategy for a new product launch"
        
        print(f"Problem: {problem}")
        print("=" * 50)
        
        # Thought 1
        result = await client.think(
            "First, I need to identify the target audience for this product",
            next_thought_needed=True,
            total_thoughts=5
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Thought 2
        result = await client.think(
            "Next, I should analyze the competitive landscape to understand positioning",
            next_thought_needed=True,
            total_thoughts=5
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Thought 3
        result = await client.think(
            "Then, I need to define the key messaging and value proposition",
            next_thought_needed=True,
            total_thoughts=5
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Thought 4
        result = await client.think(
            "I should select the most effective marketing channels and tactics",
            next_thought_needed=True,
            total_thoughts=5
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Final thought
        result = await client.think(
            "Finally, I need to create a timeline and budget for the campaign execution",
            next_thought_needed=False,
            total_thoughts=5
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
    
    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())