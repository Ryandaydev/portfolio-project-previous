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

# def test_health_check():
#     """Tests health check from SDK"""
#     config = SWCConfig()
#     client = SWCClient(config)
#     response = client.get_health_check()
#     assert response.status_code == 200
#     assert response.json() == {"message": "API health check successful"}

# def test_health_check_with_URL():
#     """Tests health check from SDK"""
#     config = SWCConfig(url="http://127.0.0.1:8000")
#     client = SWCClient(config)    
#     response = client.get_health_check()
#     assert response.status_code == 200
#     assert response.json() == {"message": "API health check successful"}

# def test_list_leagues():
#     """Tests get leagues from SDK"""
#     config = SWCConfig(url="http://127.0.0.1:8000")
#     client = SWCClient(config)    
#     leagues_response = client.list_leagues()
#     # Assert the list is not empty
#     assert isinstance(leagues_response, list)
#     # Assert each item in the list is an instance of League
#     for league in leagues_response:
#         assert isinstance(league, League)
#     assert len(leagues_response) == 5

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


#bulk endpoints
def test_bulk_player_file():
    """Tests bulk player download through SDK"""

    config = SWCConfig()
    client = SWCClient(config)    

    player_file = client.get_bulk_player_file()


    # Write the file to disk to verify file download
    output_file_path = data_dir + 'players_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(player_file)

    # Decode the byte content to a string to test contents
    player_file_str = player_file.decode('utf-8-sig') 
    player_file_s = StringIO(player_file_str)

    csv_reader = csv.reader(player_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 551

    # Additional check: ensure the first row is the header
    assert rows[0] == ['player_id','gsis_id','first_name','last_name','position','last_changed_date']

def test_bulk_league_file():
    """Tests bulk league download through SDK"""

    config = SWCConfig()
    client = SWCClient(config)    

    league_file = client.get_bulk_league_file()

    # Write the file to disk to verify file download
    output_file_path = data_dir + 'leagues_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(league_file)

    # Decode the byte content to a string to test contents
    league_file_str = league_file.decode('utf-8-sig') 
    league_file_s = StringIO(league_file_str)

    csv_reader = csv.reader(league_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 6

    # Additional check: ensure the first row is the header
    assert rows[0] == ['league_id','league_name','scoring_type','last_change_date']

def test_bulk_performance_file():
    """Tests bulk performance download through SDK"""

    config = SWCConfig()
    client = SWCClient(config)    

    performance_file = client.get_bulk_performance_file()

    # Write the file to disk to verify file download
    output_file_path = data_dir + 'performances_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(performance_file)

    # Decode the byte content to a string to test contents
    performance_file_str = performance_file.decode('utf-8-sig') 
    performance_file_s = StringIO(performance_file_str)

    csv_reader = csv.reader(performance_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 1101

    # Additional check: ensure the first row is the header
    assert rows[0] == ['performance_id','week_number','fantasy_points','player_id','last_change_date']

def test_bulk_team_file():
    """Tests bulk team download through SDK"""

    config = SWCConfig()
    client = SWCClient(config)    

    team_file = client.get_bulk_team_file()

    # Write the file to disk to verify file download
    output_file_path = data_dir + 'teams_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(team_file)

    # Decode the byte content to a string to test contents
    team_file_str = team_file.decode('utf-8-sig') 
    team_file_s = StringIO(team_file_str)

    csv_reader = csv.reader(team_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 21

    # Additional check: ensure the first row is the header
    assert rows[0] == ['team_id','team_name','league_id','last_change_date']

def test_bulk_team_player_file():
    """Tests bulk team_player download through SDK"""

    config = SWCConfig()
    client = SWCClient(config)    

    team_player_file = client.get_bulk_team_player_file()
    
    # Write the file to disk to verify file download
    output_file_path = data_dir + 'team_player_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(team_player_file)

    # Decode the byte content to a string to test contents
    team_player_file_str = team_player_file.decode('utf-8-sig') 
    team_player_file_s = StringIO(team_player_file_str)

    csv_reader = csv.reader(team_player_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 141

    # Additional check: ensure the first row is the header
    assert rows[0] == ['team_id','player_id','last_change_date']