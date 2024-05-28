import pytest
from pyswc import SWCClient
from pyswc import SWCConfig
from pyswc.schemas import League

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
    config = SWCConfig(url="http://127.0.0.1:8000")
    client = SWCClient(config)    
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

def test_get_leagues():
    """Tests get leagues from SDK"""
    config = SWCConfig(url="http://127.0.0.1:8000")
    client = SWCClient(config)    
    leagues_response = client.get_leagues()
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5

def test_get_leagues_no_backoff():
    """Tests get leagues from SDK without backoff"""
    config = SWCConfig(url="http://127.0.0.1:8000",backoff=False)
    client = SWCClient(config)    
    leagues_response = client.get_leagues()
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5    