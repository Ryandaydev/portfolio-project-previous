"""Testing the sdk"""
import pytest
from pyswc import swc_client

def test_health_check():
    """Tests health check from SDK"""
    client = swc_client()
    response = client.get_leagues()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}


