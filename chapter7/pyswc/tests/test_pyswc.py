"""Testing the sdk"""
import pytest
from pyswc import SWC_Client
from pyswc import SWC_Config
from ..schemas.sdk_schemas import LeagueWrapper, LeaguesWrapper
from ..errors.swc_error import SWCError


#config = SWC_Config("https://swc-api-container.86jt1rvv5bo8k.us-west-2.cs.amazonlightsail.com")
#config = SWC_Config(timeout=10.0)
#config = SWC_Config("https://api.sportsworldcentral-false.com", backoff=False)
#config = SWC_Config("https://api.sportsworldcentral-false.com")
config = SWC_Config()

#[TODO: use monkeypatch to test more error conditions]

client = SWC_Client(config)

# def test_health_check():
#     """Tests health check from SDK"""
#     response = client.health_check()
#     assert response.status_code == 200
#     assert response.json() == {"message": "API health check successful"}



# def test_get_league_by_id():
#     """Tests get leagues from SDK"""
#     try: 
#         wrapped_league_response = client.get_league_by_id(5002)
#     except SWCError as e:
#         raise(e)
    
#     #assert response.status_code == 200
#     assert isinstance(wrapped_league_response, LeagueWrapper)
#     assert wrapped_league_response.http_response_code == 200
#     assert len(wrapped_league_response.response_league.teams) == 8    


def test_get_leagues():
    """Tests get leagues from SDK"""
    try: 
        wrapped_leagues_response = client.get_leagues()
    except SWCError as e:
        raise(e)    
    assert isinstance(wrapped_leagues_response, LeaguesWrapper)
    assert wrapped_leagues_response.http_response_code == 200
    assert len(wrapped_leagues_response.response_leagues) == 5


def test_get_leagues_with_filter():
    """Tests get leagues from SDK"""
    try: 
        wrapped_leagues_response = client.get_leagues(league_name='Pigskin Prodigal Fantasy League')
    except SWCError as e:
        raise(e)    
    assert isinstance(wrapped_leagues_response, LeaguesWrapper)
    assert wrapped_leagues_response.http_response_code == 200
    assert len(wrapped_leagues_response.response_leagues) == 1


# def test_get_league_by_id():
#     """Tests get leagues from SDK"""
#     try: 
#         wrapped_league_response = client.get_league_by_id(5002)
#     except SWCError as e:
#         raise(e)
    
#     #assert response.status_code == 200
#     assert isinstance(wrapped_league_response, LeagueWrapper)
#     assert wrapped_league_response.http_response_code == 200
#     assert len(wrapped_league_response.response_league.teams) == 8        