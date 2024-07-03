import pytest
from pyswc import SWCClient
from pyswc import SWCConfig
from pyswc.schemas import League, Team, Player, Performance
import csv
import os
from io import StringIO

current_dir = os.path.dirname(__file__)
data_dir = current_dir + "/test_data_output/"

"""Unit tests for PYSWC SDK

    Tests the functionality of the SDK to interact
    with the SWC API.

Typical usage example:

    pytest test_pyswc.py

"""


config = SWCConfig(url="http://127.0.0.1:8000",backoff=False)
client = SWCClient(config)    

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

def test_list_leagues():
    """Tests get leagues from SDK"""
    config = SWCConfig(url="http://127.0.0.1:8000")
    client = SWCClient(config)    
    leagues_response = client.list_leagues()
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5

def test_list_leagues_no_backoff():
    """Tests get leagues from SDK without backoff"""
    config = SWCConfig(url="http://127.0.0.1:8000",backoff=False)
    client = SWCClient(config)    
    leagues_response = client.list_leagues()
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5    

def test_get_leagues_with_filter():
    """Tests get leagues from SDK"""
    
    leagues_response = client.list_leagues(league_name='Pigskin Prodigal Fantasy League')

    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 1


def test_get_league_by_id():
    """Tests get leagues from SDK"""

    league_response = client.get_league_by_id(5002)
        
    assert isinstance(league_response, League)
    assert len(league_response.teams) == 8        

def test_list_teams():
    """Tests list teams from SDK"""
    
    teams_response = client.list_teams()

    # Assert the list is not empty
    assert isinstance(teams_response, list)
    # Assert each item in the list is an instance of League
    for team in teams_response:
        assert isinstance(team, Team)
    assert len(teams_response) == 20



#players
def test_list_players():
    """Tests get players from SDK"""
    
    players_response = client.list_players(skip=0,limit=600)

    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 550


def test_list_players_by_name():
    """Tests that the count of players in the database is what is expected"""
    players_response = client.list_players(first_name="Bryce", last_name="Young")

    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 1
    assert players_response[0].player_id == 102


def test_get_player_by_id():
    """Tests get player by ID from SDK"""

    player_response = client.get_player_by_id(102)

    assert isinstance(player_response, Player)
    assert player_response.first_name == "Bryce"       

#scoring endpoints
def test_list_performances():
    """Tests get peformances from SDK"""

    performances_response = client.list_performances(skip=0,limit=2000)


    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 1100


#test /v0/performances/ with changed date
def test_list_performances_by_date():
    """Tests get peformances from SDK"""
    
    performances_response = client.list_performances(skip=0,limit=2000,minimum_last_changed_date="2024-04-01")

    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 550
