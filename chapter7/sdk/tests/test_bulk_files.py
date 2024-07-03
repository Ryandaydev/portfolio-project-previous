import pytest
from pyswc import SWCClient
from pyswc import SWCConfig
from pyswc.schemas import League, Team, Player, Performance
import csv
import os
from io import StringIO, BytesIO
import pyarrow.parquet as pq
import pandas as pd

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


def test_bulk_player_file_parquet():
    """Tests bulk player download through SDK - Parquet"""

    config = SWCConfig(bulk_file_format = "parquet")
    client = SWCClient(config)    

    player_file_parquet = client.get_bulk_player_file()

    player_table = pq.read_table(BytesIO(player_file_parquet))

    player_df = player_table.to_pandas()

    # Assert the file has the correct number of records (including header)
    assert len(player_df) == 1018