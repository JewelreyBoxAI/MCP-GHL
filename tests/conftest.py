"""Pytest configuration for GHL MCP Server tests."""

import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        'GHL_API_KEY': 'test_api_key',
        'GHL_SUB_ACCOUNT_ID': 'test_sub_account',
        'GHL_API_BASE_URL': 'https://test.gohighlevel.com/v1',
        'ALLOWED_ORIGINS': '*'
    }):
        yield 