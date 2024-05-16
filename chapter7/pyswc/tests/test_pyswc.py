"""Testing the sdk"""
import pytest
from pyswc import SWC_Client
from pyswc import SWC_Config
from ..schemas import League, Player, Performance, Team, Counts
from ..errors import SWCError
from io import StringIO
import csv



#config = SWC_Config("https://swc-api-container.86jt1rvv5bo8k.us-west-2.cs.amazonlightsail.com")
#config = SWC_Config(timeout=10.0)
#config = SWC_Config("https://api.sportsworldcentral-false.com", backoff=False)
#config = SWC_Config("https://api.sportsworldcentral-false.com")
config = SWC_Config()


client = SWC_Client(config)

#analytics endpoints
def test_health_check():
    """Tests health check from SDK"""
    response = client.health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

def test_get_counts():
    """Tests get counts from SDK"""
    counts_response = client.get_counts()
    assert isinstance(counts_response, Counts)
    assert counts_response.league_count == 5
    assert counts_response.team_count == 20
    assert counts_response.player_count == 550


#membership endpoints
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

def test_get_teams():
    """Tests get teams from SDK"""
    try: 
        teams_response = client.get_teams()
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(teams_response, list)
    # Assert each item in the list is an instance of League
    for team in teams_response:
        assert isinstance(team, Team)
    assert len(teams_response) == 20



#players
def test_get_players():
    """Tests get players from SDK"""
    try: 
        players_response = client.get_players(skip=0,limit=600)
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 550


def test_get_players_by_name():
    """Tests that the count of players in the database is what is expected"""
    try: 
        players_response = client.get_players(first_name="Bryce", last_name="Young")
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 1
    assert players_response[0].player_id == 102


def test_get_player_by_id():
    """Tests get player by ID from SDK"""
    try: 
        player_response = client.get_player_by_id(102)
    except SWCError as e:
        raise(e)
    assert isinstance(player_response, Player)
    assert player_response.first_name == "Bryce"       

#scoring endpoints
def test_get_performances():
    """Tests get peformances from SDK"""
    try: 
        performances_response = client.get_performances(skip=0,limit=2000)
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 1100


#test /v0/performances/ with changed date
def test_get_performances_by_date():
    """Tests get peformances from SDK"""
    try: 
        performances_response = client.get_performances(skip=0,limit=2000,minimum_last_changed_date="2024-04-01")
    except SWCError as e:
        raise(e)    
    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 550

#bulk endpoints
def test_bulk_players():
    """Tests bulk player download through SDK"""
    try: 
        player_file = client.get_bulk_players()
    except SWCError as e:
        raise(e)    

    # Decode the byte content to a string
    player_file_str = player_file.decode('utf-8-sig') 

    # Use StringIO to get data from file
    player_file_s = StringIO(player_file_str)

    # Write the file to disk
    output_file_path = 'tests/test_data/players_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(player_file)

    csv_reader = csv.reader(player_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 551

    # Additional check: ensure the first row is the header
    assert rows[0] == ['player_id','gsis_id','first_name','last_name','position','last_changed_date']


def test_bulk_leagues():
    """Tests bulk league download through SDK"""
    try: 
        league_file = client.get_bulk_leagues()
    except SWCError as e:
        raise(e)    

    # Decode the byte content to a string
    league_file_str = league_file.decode('utf-8-sig') 

    # Use StringIO to get data from file
    league_file_s = StringIO(league_file_str)

    # Write the file to disk
    output_file_path = 'tests/test_data/leagues_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(league_file)

    csv_reader = csv.reader(league_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 6

    # Additional check: ensure the first row is the header
    assert rows[0] == ['league_id','league_name','scoring_type','last_change_date']

def test_bulk_performances():
    """Tests bulk performance download through SDK"""
    try: 
        performance_file = client.get_bulk_performances()
    except SWCError as e:
        raise(e)    

    # Decode the byte content to a string
    performance_file_str = performance_file.decode('utf-8-sig') 

    # Use StringIO to get data from file
    performance_file_s = StringIO(performance_file_str)

    # Write the file to disk
    output_file_path = 'tests/test_data/performances_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(performance_file)

    csv_reader = csv.reader(performance_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 1101

    # Additional check: ensure the first row is the header
    assert rows[0] == ['performance_id','week_number','fantasy_points','player_id','last_change_date']

def test_bulk_teams():
    """Tests bulk team download through SDK"""
    try: 
        team_file = client.get_bulk_teams()
    except SWCError as e:
        raise(e)    

    # Decode the byte content to a string
    team_file_str = team_file.decode('utf-8-sig') 

    # Use StringIO to get data from file
    team_file_s = StringIO(team_file_str)

    # Write the file to disk
    output_file_path = 'tests/test_data/teams_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(team_file)

    csv_reader = csv.reader(team_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 21

    # Additional check: ensure the first row is the header
    assert rows[0] == ['team_id','team_name','league_id','last_change_date']

def test_bulk_team_players():
    """Tests bulk team_player download through SDK"""
    try: 
        team_player_file = client.get_bulk_team_players()
    except SWCError as e:
        raise(e)    
    
    # Write the file to disk
    output_file_path = 'tests/test_data/team_player_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(team_player_file)

    # Decode the byte content to a string
    team_player_file_str = team_player_file.decode('utf-8-sig') 

    # Use StringIO to get data from file
    team_player_file_s = StringIO(team_player_file_str)



    csv_reader = csv.reader(team_player_file_s)

    # Assert the file has the correct number of records (including header)
    rows = list(csv_reader)
    assert len(rows) == 141

    # Additional check: ensure the first row is the header
    assert rows[0] == ['team_id','player_id','last_change_date']
