import pytest
from pyswc import SWCClient
from pyswc import SWCConfig
from pyswc.schemas import League
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

# def test_get_leagues():
#     """Tests get leagues from SDK"""
#     config = SWCConfig(url="http://127.0.0.1:8000")
#     client = SWCClient(config)    
#     leagues_response = client.get_leagues()
#     # Assert the list is not empty
#     assert isinstance(leagues_response, list)
#     # Assert each item in the list is an instance of League
#     for league in leagues_response:
#         assert isinstance(league, League)
#     assert len(leagues_response) == 5

# def test_get_leagues_no_backoff():
#     """Tests get leagues from SDK without backoff"""
#     config = SWCConfig(url="http://127.0.0.1:8000",backoff=False)
#     client = SWCClient(config)    
#     leagues_response = client.get_leagues()
#     # Assert the list is not empty
#     assert isinstance(leagues_response, list)
#     # Assert each item in the list is an instance of League
#     for league in leagues_response:
#         assert isinstance(league, League)
#     assert len(leagues_response) == 5    

#bulk endpoints
def test_bulk_players():

    config = SWCConfig()
    client = SWCClient(config)    

    """Tests bulk player download through SDK"""
    player_file = client.get_bulk_players()


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