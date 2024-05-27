import pytest
from pyswc import SWCClient
from pyswc import SWCConfig

"""Unit tests for PYSWC SDK

    Tests the functionality of the SDK to interact
    with the SWC API.

Typical usage example:

    pytest test_pyswc.py

"""

def test_health_check():
    """Tests health check from SDK"""
    config = SWCConfig()
    client = SWCClient(config)
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

def test_health_check_with_URL():
    """Tests health check from SDK"""
    config = SWCConfig("http://127.0.0.1:8000")
    client = SWCClient(config)    
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}
