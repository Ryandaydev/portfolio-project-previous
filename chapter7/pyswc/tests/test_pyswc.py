"""Testing the sdk"""
import pytest
from pyswc import SWC_Client
from pyswc import SWC_Config
from ..schemas.sdk_schemas import League, LeagueWrapper


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

def test_get_league_by_id():
    """Tests get leagues from SDK"""
    league_response = client.get_league_by_id(5002)
    #assert response.status_code == 200
    assert isinstance(league_response, League)
    assert len(league_response.teams) == 8


def test_get_league_by_id_with_wrapper():
    """Tests get leagues from SDK"""
    wrapped_league_response = client.get_league_by_id_with_wrapper(5002)
    #assert response.status_code == 200
    assert isinstance(wrapped_league_response, LeagueWrapper)
    assert wrapped_league_response.http_response_code == 200
    assert len(wrapped_league_response.response_league.teams) == 8    