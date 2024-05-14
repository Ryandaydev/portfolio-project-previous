"""Testing the sdk"""
import pytest
from pyswc import SWC_Client
from pyswc import SWC_Config

config = SWC_Config("https://swc-api-container.86jt1rvv5bo8k.us-west-2.cs.amazonlightsail.com")

client = SWC_Client(config)

def test_health_check():
    """Tests health check from SDK"""
    response = client.health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

def test_get_leagues():
    """Tests get leagues from SDK"""
    response = client.get_leagues()
    assert response.status_code == 200
    assert len(response.json()) == 5
