"""Testing SQLAlchemy Helper Functions"""
import pytest
from datetime import date

import crud
from database import SessionLocal

# use a test date of 4/1/2024 to test the min_last_changed_date.
test_date = date(2024,4,1)

@pytest.fixture(scope="function")
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()

def test_get_player(db_session):
    """Tests you can get the first player"""
    player = crud.get_player(db_session, player_id = 101)
    assert player.player_id == 101

def test_get_players(db_session):
    """Tests that the count of players in the database is what is expected"""
    players = crud.get_players(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(players) == 550

def test_get_all_performances(db_session):
    """Tests that the count of performances in the database is what is expected - all the performances"""
    performances = crud.get_performances(db_session, skip=0, limit=10000)
    assert len(performances) == 1100

def test_get_half_performances(db_session):
    """Tests that the count of performances in the database is what is expected - half the performances"""
    performances = crud.get_performances(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(performances) == 550

def test_get_leagues(db_session):
    """Tests that the count of leagues in the database is what is expected"""
    leagues = crud.get_leagues(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(leagues) == 5

def test_get_teams(db_session):
    """Tests that the count of teams in the database is what is expected"""
    teams = crud.get_teams(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(teams) == 20


def test_get_team_players(db_session):
    """Tests that a team record can retrieve players, and that 8 players are on the first team"""
    first_team = crud.get_teams(db_session, skip=0, limit=1000, min_last_changed_date=test_date)[0]
    assert len(first_team.players) == 7