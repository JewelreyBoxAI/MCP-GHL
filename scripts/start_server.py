#!/usr/bin/env python3
"""Startup script for GHL MCP Server."""

import os
import sys
import asyncio
import uvicorn
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import settings


def main():
    """Start the GHL MCP Server."""
    print("🚀 Starting GHL MCP Server")
    print(f"📍 Host: {settings.mcp_server_host}")
    print(f"🔌 Port: {settings.mcp_server_port}")
    print(f"🔧 Sub-account: {settings.ghl_sub_account_id}")
    print("=" * 50)
    
    # Check required environment variables
    required_vars = ["GHL_API_KEY", "GHL_SUB_ACCOUNT_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file or environment setup.")
        sys.exit(1)
    
    try:
        uvicorn.run(
            "mcp_server:app",
            host=settings.mcp_server_host,
            port=settings.mcp_server_port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 