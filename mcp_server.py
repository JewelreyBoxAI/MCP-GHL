"""MCP Server for GoHighLevel integration."""

import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

from config import settings
import mcp_tools


class MCPRequest(BaseModel):
    """Request model for MCP tool calls."""
    tool_name: str
    arguments: Dict[str, Any]


class MCPResponse(BaseModel):
    """Response model for MCP tool calls."""
    success: bool
    result: Any
    error: Optional[str] = None


# Initialize FastAPI app
app = FastAPI(
    title="GHL MCP Server",
    description="Model Connection Protocol server for GoHighLevel integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp_server = Server("ghl-mcp-server")

# Register all tools from mcp_tools module
AVAILABLE_TOOLS = {
    "get_contact_info": mcp_tools.get_contact_info,
    "list_opportunities": mcp_tools.list_opportunities,
    "trigger_webhook": mcp_tools.trigger_webhook,
    "get_pipeline_info": mcp_tools.get_pipeline_info,
    "create_note": mcp_tools.create_note,
    "search_contacts": mcp_tools.search_contacts,
    "get_contact_activities": mcp_tools.get_contact_activities,
    "create_opportunity": mcp_tools.create_opportunity,
}


@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "GHL MCP Server",
        "version": "1.0.0",
        "description": "Model Connection Protocol server for GoHighLevel integration",
        "available_tools": list(AVAILABLE_TOOLS.keys()),
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "server": "ghl-mcp-server"}


@app.get("/tools")
async def list_tools():
    """List all available tools."""
    tools_info = []
    for tool_name, tool_func in AVAILABLE_TOOLS.items():
        tools_info.append({
            "name": tool_name,
            "description": tool_func.__doc__ or "No description available",
            "parameters": getattr(tool_func, '__annotations__', {})
        })
    return {"tools": tools_info}


@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: MCPRequest):
    """Call a specific tool with the provided arguments."""
    if tool_name not in AVAILABLE_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    try:
        tool_func = AVAILABLE_TOOLS[tool_name]
        result = await tool_func(**request.arguments)
        
        return MCPResponse(
            success=True,
            result=result
        )
    except Exception as e:
        return MCPResponse(
            success=False,
            result=None,
            error=str(e)
        )


@app.post("/mcp/call_tool")
async def mcp_call_tool(request: MCPRequest):
    """MCP-compatible tool calling endpoint."""
    return await call_tool(request.tool_name, request)


@app.get("/mcp/list_tools")
async def mcp_list_tools():
    """MCP-compatible tool listing endpoint."""
    tools = []
    for tool_name, tool_func in AVAILABLE_TOOLS.items():
        tools.append(Tool(
            name=tool_name,
            description=tool_func.__doc__ or "No description available",
            inputSchema={
                "type": "object",
                "properties": getattr(tool_func, '__annotations__', {}),
                "required": []
            }
        ))
    return {"tools": tools}


# MCP Server event handlers
@mcp_server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """Handle resource listing requests."""
    return [
        Resource(
            uri="ghl://contacts",
            name="GoHighLevel Contacts",
            description="Access to GHL contact management",
            mimeType="application/json"
        ),
        Resource(
            uri="ghl://opportunities", 
            name="GoHighLevel Opportunities",
            description="Access to GHL opportunity pipeline",
            mimeType="application/json"
        ),
        Resource(
            uri="ghl://pipelines",
            name="GoHighLevel Pipelines", 
            description="Access to GHL funnel and pipeline data",
            mimeType="application/json"
        )
    ]


@mcp_server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Handle resource reading requests."""
    if uri == "ghl://contacts":
        return "GoHighLevel Contacts Resource - Use get_contact_info or search_contacts tools"
    elif uri == "ghl://opportunities":
        return "GoHighLevel Opportunities Resource - Use list_opportunities tool"
    elif uri == "ghl://pipelines":
        return "GoHighLevel Pipelines Resource - Use get_pipeline_info tool"
    else:
        raise ValueError(f"Unknown resource: {uri}")


@mcp_server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Handle tool listing requests."""
    tools = []
    for tool_name, tool_func in AVAILABLE_TOOLS.items():
        tools.append(Tool(
            name=tool_name,
            description=tool_func.__doc__ or "No description available",
            inputSchema={
                "type": "object", 
                "properties": getattr(tool_func, '__annotations__', {}),
                "required": []
            }
        ))
    return tools


@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool execution requests."""
    if name not in AVAILABLE_TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        tool_func = AVAILABLE_TOOLS[name]
        result = await tool_func(**arguments)
        
        return [TextContent(
            type="text",
            text=str(result)
        )]
    except Exception as e:
        return [TextContent(
            type="text", 
            text=f"Error executing tool {name}: {str(e)}"
        )]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mcp_server:app",
        host=settings.mcp_server_host,
        port=settings.mcp_server_port,
        reload=True
    ) 