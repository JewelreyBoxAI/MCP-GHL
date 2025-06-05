"""GoHighLevel API client for MCP server."""

import httpx
from typing import Dict, List, Optional, Any
from config import settings


class GHLClient:
    """Client for interacting with GoHighLevel API."""
    
    def __init__(self):
        """Initialize the GHL client."""
        self.base_url = settings.ghl_api_base_url
        self.headers = settings.ghl_headers
        self.sub_account_id = settings.ghl_sub_account_id
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[Any, Any]:
        """Make an HTTP request to the GHL API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add sub-account ID to params if not already present
        if params is None:
            params = {}
        if "locationId" not in params:
            params["locationId"] = self.sub_account_id
            
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_contact_info(self, contact_id: str) -> Dict[Any, Any]:
        """Fetch contact details by ID."""
        return await self._make_request("GET", f"/contacts/{contact_id}")
    
    async def list_opportunities(self, pipeline_id: Optional[str] = None) -> Dict[Any, Any]:
        """List all opportunities, optionally filtered by pipeline."""
        params = {}
        if pipeline_id:
            params["pipelineId"] = pipeline_id
        return await self._make_request("GET", "/opportunities/", params=params)
    
    async def get_pipeline_info(self, pipeline_id: Optional[str] = None) -> Dict[Any, Any]:
        """Retrieve funnel/pipeline structure."""
        if pipeline_id:
            return await self._make_request("GET", f"/funnels/{pipeline_id}")
        else:
            return await self._make_request("GET", "/funnels/")
    
    async def create_note(self, contact_id: str, note_content: str) -> Dict[Any, Any]:
        """Create a note on a contact."""
        data = {
            "body": note_content,
            "contactId": contact_id
        }
        return await self._make_request("POST", f"/contacts/{contact_id}/notes", data=data)
    
    async def trigger_webhook(self, webhook_url: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
        """Trigger a custom workflow webhook."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return {"status": "success", "response": response.text}
    
    async def search_contacts(
        self, 
        query: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        limit: int = 100
    ) -> Dict[Any, Any]:
        """Search contacts with various filters."""
        params = {"limit": limit}
        if query:
            params["query"] = query
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
            
        return await self._make_request("GET", "/contacts/", params=params)
    
    async def get_contact_activities(self, contact_id: str) -> Dict[Any, Any]:
        """Get activities for a specific contact."""
        return await self._make_request("GET", f"/contacts/{contact_id}/activities")
    
    async def create_opportunity(
        self,
        contact_id: str,
        pipeline_id: str,
        stage_id: str,
        title: str,
        value: Optional[float] = None
    ) -> Dict[Any, Any]:
        """Create a new opportunity."""
        data = {
            "contactId": contact_id,
            "pipelineId": pipeline_id,
            "pipelineStageId": stage_id,
            "title": title
        }
        if value:
            data["monetaryValue"] = value
            
        return await self._make_request("POST", "/opportunities/", data=data)


# Global client instance
ghl_client = GHLClient() 