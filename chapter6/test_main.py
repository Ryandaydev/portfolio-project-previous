from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#test the health check endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

#test /v0/players/
def test_read_players():
    response = client.get("/v0/players/?skip=0&limit=10000")
    assert response.status_code == 200
    assert len(response.json()) == 550

def test_read_players_by_name():
    response = client.get("/v0/players/?first_name=Bryce&last_name=Young")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("player_id") == 102

#test /v0/players/{player_id}/
def test_read_players_with_id():
    response = client.get("/v0/players/101/")
    assert response.status_code == 200
    assert response.json().get("player_id") == 101

#test /v0/performances/
def test_read_performances():
    response = client.get("/v0/performances/?skip=0&limit=10000")
    assert response.status_code == 200
    assert len(response.json()) == 1100

#test /v0/performances/ with changed date
def test_read_performances_by_date():
    response = client.get("/v0/performances/?skip=0&limit=10000&minimum_last_changed_date=2024-04-01")
    assert response.status_code == 200
    assert len(response.json()) == 550

#test /v0/leagues/
def test_read_leagues():
    response = client.get("/v0/leagues/?skip=0&limit=500")
    assert response.status_code == 200
    assert len(response.json()) == 5

#test /v0/teams/
def test_read_teams():
    response = client.get("/v0/teams/?skip=0&limit=500")
    assert response.status_code == 200
    assert len(response.json()) == 20

#test the count functions
def test_counts():
    response = client.get("/v0/counts/")
    response_data = response.json()
    assert response.status_code == 200    
    assert response_data['league_count'] == 5
    assert response_data['team_count'] == 20
    assert response_data['player_count'] == 550


