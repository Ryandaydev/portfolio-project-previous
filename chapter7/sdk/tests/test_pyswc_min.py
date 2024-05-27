# """Testing the minimum viable SDK"""

# import pytest
# from pyswc import SWCClient

# client = SWCClient(swc_base_url="http://127.0.0.1:8000")


# def test_health_check():
#     """Tests health check from SDK"""
#     response = client.get_health_check()
#     assert response.status_code == 200
#     assert response.json() == {"message": "API health check successful"}
