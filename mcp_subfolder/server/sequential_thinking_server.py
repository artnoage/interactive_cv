#!/usr/bin/env python3
"""
Sequential Thinking MCP Server

An MCP server that provides a tool for dynamic and reflective problem-solving 
through a structured thinking process.
"""

import json
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Thought:
    """Represents a single thought in the sequential thinking process"""
    number: int
    content: str
    timestamp: datetime
    is_revision: bool = False
    revises_thought: Optional[int] = None
    branch_from_thought: Optional[int] = None
    branch_id: Optional[str] = None


class SequentialThinkingEngine:
    """Engine that manages the sequential thinking process"""
    
    def __init__(self):
        self.thoughts: List[Thought] = []
        self.current_thought_number = 0
        self.total_thoughts_estimate = 0
        self.branches: Dict[str, List[Thought]] = {}
        self.current_branch = "main"
    
    def add_thought(
        self, 
        content: str, 
        is_revision: bool = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None
    ) -> Thought:
        """Add a new thought to the sequence"""
        
        if branch_id and branch_id != self.current_branch:
            # Switch to or create new branch
            self.current_branch = branch_id
            if branch_id not in self.branches:
                self.branches[branch_id] = []
        
        self.current_thought_number += 1
        
        thought = Thought(
            number=self.current_thought_number,
            content=content,
            timestamp=datetime.now(),
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id
        )
        
        if self.current_branch == "main":
            self.thoughts.append(thought)
        else:
            self.branches[self.current_branch].append(thought)
        
        return thought
    
    def get_thinking_summary(self) -> Dict[str, Any]:
        """Get a summary of the current thinking process"""
        return {
            "current_thought_number": self.current_thought_number,
            "total_thoughts_estimate": self.total_thoughts_estimate,
            "current_branch": self.current_branch,
            "main_thoughts": [asdict(t) for t in self.thoughts],
            "branches": {k: [asdict(t) for t in v] for k, v in self.branches.items()},
            "total_branches": len(self.branches)
        }


class MCPServer:
    """Basic MCP Server implementation"""
    
    def __init__(self):
        self.thinking_engine = SequentialThinkingEngine()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "sequential-thinking-server",
                "version": "1.0.0"
            }
        }
    
    def handle_tools_list(self, params: Dict) -> Dict:
        """Handle tools/list request"""
        return {
            "tools": [
                {
                    "name": "sequential_thinking",
                    "description": "Facilitates a detailed, step-by-step thinking process for problem-solving and analysis. Helps break down complex problems into manageable steps, revise and refine thoughts, and branch into alternative reasoning paths.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "thought": {
                                "type": "string",
                                "description": "The current thinking step"
                            },
                            "nextThoughtNeeded": {
                                "type": "boolean",
                                "description": "Whether another thought step is needed"
                            },
                            "thoughtNumber": {
                                "type": "integer",
                                "description": "Current thought number"
                            },
                            "totalThoughts": {
                                "type": "integer",
                                "description": "Estimated total thoughts needed"
                            },
                            "isRevision": {
                                "type": "boolean",
                                "description": "Whether this revises previous thinking"
                            },
                            "revisesThought": {
                                "type": "integer",
                                "description": "Which thought is being reconsidered"
                            },
                            "branchFromThought": {
                                "type": "integer",
                                "description": "Branching point thought number"
                            },
                            "branchId": {
                                "type": "string",
                                "description": "Branch identifier"
                            },
                            "needsMoreThoughts": {
                                "type": "boolean",
                                "description": "If more thoughts are needed"
                            }
                        },
                        "required": ["thought", "nextThoughtNeeded", "thoughtNumber", "totalThoughts"]
                    }
                }
            ]
        }
    
    def handle_tools_call(self, params: Dict) -> Dict:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "sequential_thinking":
            return self._handle_sequential_thinking(arguments)
        else:
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}"
                    }
                ]
            }
    
    def _handle_sequential_thinking(self, args: Dict) -> Dict:
        """Handle sequential thinking tool call"""
        try:
            # Extract arguments
            thought = args.get("thought", "")
            next_thought_needed = args.get("nextThoughtNeeded", False)
            thought_number = args.get("thoughtNumber", 1)
            total_thoughts = args.get("totalThoughts", 1)
            is_revision = args.get("isRevision", False)
            revises_thought = args.get("revisesThought")
            branch_from_thought = args.get("branchFromThought")
            branch_id = args.get("branchId")
            needs_more_thoughts = args.get("needsMoreThoughts", False)
            
            # Update total thoughts estimate
            self.thinking_engine.total_thoughts_estimate = total_thoughts
            
            # Add the thought
            new_thought = self.thinking_engine.add_thought(
                content=thought,
                is_revision=is_revision,
                revises_thought=revises_thought,
                branch_from_thought=branch_from_thought,
                branch_id=branch_id
            )
            
            # Generate response
            response_text = f"Thought {new_thought.number}: {thought}\n"
            
            if is_revision and revises_thought:
                response_text += f"→ Revising thought {revises_thought}\n"
            
            if branch_id:
                response_text += f"→ Branch: {branch_id}\n"
            
            if next_thought_needed:
                response_text += f"→ Progress: {new_thought.number}/{total_thoughts} thoughts\n"
                response_text += "→ Ready for next thought\n"
            else:
                response_text += "→ Thinking sequence complete\n"
            
            # Add summary if this is the last thought
            if not next_thought_needed:
                summary = self.thinking_engine.get_thinking_summary()
                response_text += f"\n--- Thinking Summary ---\n"
                response_text += f"Total thoughts: {summary['current_thought_number']}\n"
                response_text += f"Branches explored: {summary['total_branches']}\n"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": response_text
                    }
                ]
            }
            
        except Exception as e:
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"Error in sequential thinking: {str(e)}"
                    }
                ]
            }
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle incoming MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return self.handle_initialize(params)
        elif method == "tools/list":
            return self.handle_tools_list(params)
        elif method == "tools/call":
            return self.handle_tools_call(params)
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }


def main():
    """Main server loop"""
    server = MCPServer()
    
    print("Sequential Thinking MCP Server started", file=sys.stderr)
    print("Listening for JSON-RPC requests on stdin...", file=sys.stderr)
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = server.handle_request(request)
                
                # Add request ID to response if present
                if "id" in request:
                    response["id"] = request["id"]
                
                response["jsonrpc"] = "2.0"
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()