"""Example LangGraph agent using GHL MCP Server."""

import asyncio
import os
from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import Tool
import httpx


class AgentState:
    """State for the LangGraph agent."""
    messages: List[Any]
    tool_results: Dict[str, Any]


class GHLLangGraphAgent:
    """LangGraph agent integrated with GHL MCP Server."""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        """Initialize the agent with MCP server connection."""
        self.mcp_server_url = mcp_server_url
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.tools = []
        self.graph = None
        
    async def setup_tools(self):
        """Load tools from the MCP server."""
        try:
            # Get available tools from MCP server
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/tools")
                tools_data = response.json()
            
            # Create LangChain tools from MCP server endpoints
            for tool_info in tools_data["tools"]:
                tool = Tool(
                    name=tool_info["name"],
                    description=tool_info["description"],
                    func=self._create_tool_function(tool_info["name"])
                )
                self.tools.append(tool)
                
            print(f"Loaded {len(self.tools)} tools from MCP server")
            
        except Exception as e:
            print(f"Error loading tools from MCP server: {e}")
            
    def _create_tool_function(self, tool_name: str):
        """Create a function for calling MCP tools."""
        async def tool_function(**kwargs):
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/{tool_name}",
                    json={
                        "tool_name": tool_name,
                        "arguments": kwargs
                    }
                )
                result = response.json()
                return result.get("result", result)
        
        return tool_function
    
    def build_graph(self):
        """Build the LangGraph workflow."""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self.agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Add edges
        workflow.add_edge("agent", "tools")
        workflow.add_edge("tools", "agent")
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Compile the graph
        self.graph = workflow.compile()
        
    async def agent_node(self, state: AgentState):
        """Main agent reasoning node."""
        # Get the last message
        last_message = state.messages[-1] if state.messages else None
        
        # Create prompt for Claude
        if isinstance(last_message, HumanMessage):
            prompt = f"""
            You are an AI assistant with access to GoHighLevel (GHL) tools through an MCP server.
            
            Available tools:
            {', '.join([tool.name for tool in self.tools])}
            
            User query: {last_message.content}
            
            Please help the user with their GoHighLevel-related task. Use the appropriate tools to gather information or perform actions.
            """
            
            # Get response from Claude
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            # Add response to state
            state.messages.append(response)
            
        return state
    
    async def run(self, user_input: str) -> str:
        """Run the agent with user input."""
        if not self.graph:
            await self.setup_tools()
            self.build_graph()
            
        # Create initial state
        initial_state = AgentState()
        initial_state.messages = [HumanMessage(content=user_input)]
        initial_state.tool_results = {}
        
        # Run the graph
        result = await self.graph.ainvoke(initial_state)
        
        # Extract the final response
        if result.messages:
            last_message = result.messages[-1]
            if isinstance(last_message, AIMessage):
                return last_message.content
                
        return "No response generated"


async def main():
    """Example usage of the GHL LangGraph agent."""
    agent = GHLLangGraphAgent()
    
    # Example queries
    queries = [
        "Search for contacts with the email 'test@example.com'",
        "Get information about contact ID 'contact_123'",
        "List all opportunities in the pipeline",
        "Create a note on contact 'contact_456' saying 'Follow up next week'"
    ]
    
    for query in queries:
        print(f"\n🤖 Query: {query}")
        response = await agent.run(query)
        print(f"📋 Response: {response}")


if __name__ == "__main__":
    # Make sure you have ANTHROPIC_API_KEY set in your environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        exit(1)
        
    asyncio.run(main()) 