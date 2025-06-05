"""MCP tools for GoHighLevel integration."""

from typing import Dict, List, Optional, Any
from ghl_client import ghl_client


async def get_contact_info(contact_id: str) -> Dict[Any, Any]:
    """
    Fetch detailed contact information from GoHighLevel.
    
    Args:
        contact_id: The unique identifier for the contact
        
    Returns:
        Dict containing contact details including name, email, phone, tags, etc.
    """
    try:
        contact_data = await ghl_client.get_contact_info(contact_id)
        return {
            "success": True,
            "contact": contact_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def list_opportunities(pipeline_id: Optional[str] = None) -> Dict[Any, Any]:
    """
    List all opportunities in the GHL sub-account.
    
    Args:
        pipeline_id: Optional pipeline ID to filter opportunities
        
    Returns:
        Dict containing list of opportunities with their details
    """
    try:
        opportunities_data = await ghl_client.list_opportunities(pipeline_id)
        return {
            "success": True,
            "opportunities": opportunities_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def trigger_webhook(webhook_url: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Trigger a custom workflow webhook in GoHighLevel.
    
    Args:
        webhook_url: The webhook URL to trigger
        payload: Data to send to the webhook
        
    Returns:
        Dict containing webhook response status
    """
    try:
        result = await ghl_client.trigger_webhook(webhook_url, payload)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def get_pipeline_info(pipeline_id: Optional[str] = None) -> Dict[Any, Any]:
    """
    Retrieve funnel/pipeline structure from GoHighLevel.
    
    Args:
        pipeline_id: Optional specific pipeline ID, if None returns all pipelines
        
    Returns:
        Dict containing pipeline structure and stages
    """
    try:
        pipeline_data = await ghl_client.get_pipeline_info(pipeline_id)
        return {
            "success": True,
            "pipelines": pipeline_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def create_note(contact_id: str, note_content: str) -> Dict[Any, Any]:
    """
    Create a note on a specific contact in GoHighLevel.
    
    Args:
        contact_id: The unique identifier for the contact
        note_content: The content of the note to create
        
    Returns:
        Dict containing the created note details
    """
    try:
        note_data = await ghl_client.create_note(contact_id, note_content)
        return {
            "success": True,
            "note": note_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def search_contacts(
    query: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    limit: int = 100
) -> Dict[Any, Any]:
    """
    Search for contacts in GoHighLevel using various filters.
    
    Args:
        query: General search query
        email: Email address to search for
        phone: Phone number to search for
        limit: Maximum number of results to return
        
    Returns:
        Dict containing matching contacts
    """
    try:
        contacts_data = await ghl_client.search_contacts(query, email, phone, limit)
        return {
            "success": True,
            "contacts": contacts_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def get_contact_activities(contact_id: str) -> Dict[Any, Any]:
    """
    Get activities for a specific contact in GoHighLevel.
    
    Args:
        contact_id: The unique identifier for the contact
        
    Returns:
        Dict containing contact activities and timeline
    """
    try:
        activities_data = await ghl_client.get_contact_activities(contact_id)
        return {
            "success": True,
            "activities": activities_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def create_opportunity(
    contact_id: str,
    pipeline_id: str,
    stage_id: str,
    title: str,
    value: Optional[float] = None
) -> Dict[Any, Any]:
    """
    Create a new opportunity in GoHighLevel.
    
    Args:
        contact_id: The contact to associate with this opportunity
        pipeline_id: The pipeline to place this opportunity in
        stage_id: The initial stage for this opportunity
        title: Title/name of the opportunity
        value: Optional monetary value of the opportunity
        
    Returns:
        Dict containing the created opportunity details
    """
    try:
        opportunity_data = await ghl_client.create_opportunity(
            contact_id, pipeline_id, stage_id, title, value
        )
        return {
            "success": True,
            "opportunity": opportunity_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Export all tools for the MCP server
__all__ = [
    "get_contact_info",
    "list_opportunities", 
    "trigger_webhook",
    "get_pipeline_info",
    "create_note",
    "search_contacts",
    "get_contact_activities",
    "create_opportunity"
] 