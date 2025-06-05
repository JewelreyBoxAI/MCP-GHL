"""Tests for GHL client functionality."""

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from ghl_client import GHLClient


@pytest.fixture
def ghl_client():
    """Create a GHL client for testing."""
    return GHLClient()


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = AsyncMock()
    response.json.return_value = {"id": "test_contact", "name": "Test User"}
    response.raise_for_status.return_value = None
    return response


@pytest.mark.asyncio
async def test_get_contact_info(ghl_client, mock_response):
    """Test getting contact information."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.get_contact_info("test_contact_id")
        
        assert result["id"] == "test_contact"
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_list_opportunities(ghl_client, mock_response):
    """Test listing opportunities."""
    mock_response.json.return_value = {"opportunities": [{"id": "opp1", "title": "Test Opportunity"}]}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.list_opportunities()
        
        assert "opportunities" in result
        assert len(result["opportunities"]) == 1


@pytest.mark.asyncio
async def test_create_note(ghl_client, mock_response):
    """Test creating a contact note."""
    mock_response.json.return_value = {"id": "note123", "body": "Test note"}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.create_note("contact123", "Test note")
        
        assert result["id"] == "note123"
        assert result["body"] == "Test note"


@pytest.mark.asyncio
async def test_trigger_webhook(ghl_client):
    """Test triggering a webhook."""
    mock_response = AsyncMock()
    mock_response.text = "Success"
    mock_response.raise_for_status.return_value = None
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.trigger_webhook("https://test.webhook.url", {"test": "data"})
        
        assert result["status"] == "success"
        assert result["response"] == "Success"


@pytest.mark.asyncio
async def test_search_contacts(ghl_client, mock_response):
    """Test searching contacts."""
    mock_response.json.return_value = {"contacts": [{"id": "contact1", "email": "test@example.com"}]}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.search_contacts(email="test@example.com")
        
        assert "contacts" in result
        assert len(result["contacts"]) == 1


@pytest.mark.asyncio
async def test_create_opportunity(ghl_client, mock_response):
    """Test creating an opportunity."""
    mock_response.json.return_value = {"id": "opp123", "title": "New Opportunity"}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        
        result = await ghl_client.create_opportunity(
            "contact123", "pipeline123", "stage123", "New Opportunity", 1000.0
        )
        
        assert result["id"] == "opp123"
        assert result["title"] == "New Opportunity"


@pytest.mark.asyncio
async def test_http_error_handling(ghl_client):
    """Test HTTP error handling."""
    with patch('httpx.AsyncClient') as mock_client:
        # Simulate HTTP error
        mock_request = AsyncMock()
        mock_request.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=None, response=None
        )
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(return_value=mock_request)
        
        with pytest.raises(httpx.HTTPStatusError):
            await ghl_client.get_contact_info("nonexistent_contact") 