"""Testing SQLAlchemy Models"""
import pytest
from database import SessionLocal, engine
import models

@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_player_query(db_session):
    players = db_session.query(models.Player).all()
    assert len(players) == 160

def test_performances_query(db_session):
    performances = db_session.query(models.Performance).all()
    assert len(performances) == 320
    
def test_leagues_query(db_session):
    leagues = db_session.query(models.League).all()
    assert len(leagues) == 5
    
def test_teams_query(db_session):
    teams = db_session.query(models.Team).all()
    assert len(teams) == 20

def test_team_player_query(db_session):
    team_players = db_session.query(models.TeamPlayer).all()
    assert len(team_players) == 160
