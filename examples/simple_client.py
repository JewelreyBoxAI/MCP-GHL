"""Simple client for testing the GHL MCP Server."""

import asyncio
import httpx
import json
from typing import Dict, Any


class SimpleMCPClient:
    """Simple client for testing MCP server functionality."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """Initialize the client."""
        self.server_url = server_url
        
    async def list_tools(self) -> Dict[str, Any]:
        """List all available tools."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/tools")
            return response.json()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}/tools/{tool_name}",
                json={
                    "tool_name": tool_name,
                    "arguments": arguments
                }
            )
            return response.json()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server_url}/health")
            return response.json()


async def test_ghl_mcp_server():
    """Test the GHL MCP server with sample calls."""
    client = SimpleMCPClient()
    
    print("🔍 Testing GHL MCP Server")
    print("=" * 50)
    
    # Health check
    print("\n1. Health Check")
    try:
        health = await client.health_check()
        print(f"✅ Server Status: {health}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # List available tools
    print("\n2. Available Tools")
    try:
        tools = await client.list_tools()
        print(f"📋 Found {len(tools['tools'])} tools:")
        for tool in tools['tools']:
            print(f"   • {tool['name']}: {tool['description'][:100]}...")
    except Exception as e:
        print(f"❌ Failed to list tools: {e}")
        return
    
    # Test search contacts (safe call that doesn't require existing data)
    print("\n3. Testing search_contacts")
    try:
        result = await client.call_tool(
            "search_contacts",
            {"query": "test", "limit": 5}
        )
        print(f"🔍 Search result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"❌ Search contacts failed: {e}")
    
    # Test get pipeline info (safe call)
    print("\n4. Testing get_pipeline_info")
    try:
        result = await client.call_tool(
            "get_pipeline_info",
            {}
        )
        print(f"🔧 Pipeline info: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"❌ Get pipeline info failed: {e}")
    
    # Test list opportunities (safe call)
    print("\n5. Testing list_opportunities")
    try:
        result = await client.call_tool(
            "list_opportunities",
            {}
        )
        print(f"💼 Opportunities: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"❌ List opportunities failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")


async def interactive_mode():
    """Interactive mode for testing tools manually."""
    client = SimpleMCPClient()
    
    print("🤖 GHL MCP Interactive Client")
    print("Type 'help' for available commands, 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit":
                break
            elif command == "help":
                print("""
Available commands:
  help          - Show this help
  health        - Check server health
  tools         - List available tools
  search <query> - Search contacts
  pipelines     - Get pipeline info
  opportunities - List opportunities
  quit          - Exit
                """)
            elif command == "health":
                result = await client.health_check()
                print(f"Health: {json.dumps(result, indent=2)}")
            elif command == "tools":
                result = await client.list_tools()
                print("Available tools:")
                for tool in result['tools']:
                    print(f"  • {tool['name']}")
            elif command.startswith("search "):
                query = command[7:]  # Remove "search "
                result = await client.call_tool(
                    "search_contacts",
                    {"query": query, "limit": 5}
                )
                print(f"Search result: {json.dumps(result, indent=2)}")
            elif command == "pipelines":
                result = await client.call_tool("get_pipeline_info", {})
                print(f"Pipelines: {json.dumps(result, indent=2)}")
            elif command == "opportunities":
                result = await client.call_tool("list_opportunities", {})
                print(f"Opportunities: {json.dumps(result, indent=2)}")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Goodbye!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(test_ghl_mcp_server()) 