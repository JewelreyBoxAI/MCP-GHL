"""Configuration module for GHL MCP Server."""

import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # GoHighLevel API Settings
    ghl_api_base_url: str = Field(
        default="https://rest.gohighlevel.com/v1",
        env="GHL_API_BASE_URL",
        description="Base URL for GoHighLevel API"
    )
    
    ghl_api_key: str = Field(
        default="",  # Empty default for development
        env="GHL_API_KEY",
        description="GoHighLevel API key"
    )
    
    ghl_sub_account_id: str = Field(
        default="",  # Empty default for development
        env="GHL_SUB_ACCOUNT_ID",
        description="GoHighLevel sub-account ID"
    )
    
    # Server Settings
    allowed_origins: str = Field(
        default="*",
        env="ALLOWED_ORIGINS",
        description="Allowed CORS origins"
    )
    
    mcp_server_port: int = Field(
        default=8000,
        env="MCP_SERVER_PORT",
        description="Port for MCP server"
    )
    
    mcp_server_host: str = Field(
        default="0.0.0.0",
        env="MCP_SERVER_HOST",
        description="Host for MCP server"
    )
    
    @property
    def ghl_headers(self) -> dict:
        """Get headers for GHL API requests."""
        return {
            "Authorization": f"Bearer {self.ghl_api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        }
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 