"""Testing the sdk"""
import pytest
from pyswc import SWC_Client
from pyswc import SWC_Config
from ..schemas import League
from ..errors import SWCError


#config = SWC_Config("https://swc-api-container.86jt1rvv5bo8k.us-west-2.cs.amazonlightsail.com")
#config = SWC_Config(timeout=10.0)
#config = SWC_Config("https://api.sportsworldcentral-false.com", backoff=False)
#config = SWC_Config("https://api.sportsworldcentral-false.com")
config = SWC_Config()


client = SWC_Client(config)

def test_health_check():
    """Tests health check from SDK"""
    response = client.health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}


def test_get_leagues():
    """Tests get leagues from SDK"""
    try: 
        leagues_response = client.get_leagues()
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5


def test_get_leagues_with_filter():
    """Tests get leagues from SDK"""
    try: 
        leagues_response = client.get_leagues(league_name='Pigskin Prodigal Fantasy League')
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 1


def test_get_league_by_id():
    """Tests get leagues from SDK"""
    try: 
        league_response = client.get_league_by_id(5002)
    except SWCError as e:
        raise(e)
    
    assert isinstance(league_response, League)
    assert len(league_response.teams) == 8        
