"""Integration tests for MCP Space Life Sciences"""
import pytest
from mcp_space_life_sciences import IntegratedKGClient


def test_client_initialization():
    """Test client can be initialized"""
    client = IntegratedKGClient()
    assert client is not None


def test_find_common_nodes():
    """Test finding common nodes across KGs"""
    client = IntegratedKGClient()
    result = client.find_common_nodes({
        "genes": ["TP53", "BRCA1"]
    })
    assert "found_in_both" in result
    assert "genes" in result["found_in_both"]


# Add more integration tests
