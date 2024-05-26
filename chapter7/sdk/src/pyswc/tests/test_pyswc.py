"""Testing the sdk"""

import pytest
from pyswc import SWC_Client

client = SWC_Client(swc_base_url="http://127.0.0.1:8000")


# analytics endpoints
def test_health_check():
    """Tests health check from SDK"""
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}
