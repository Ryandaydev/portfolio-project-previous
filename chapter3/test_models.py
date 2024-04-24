"""Testing SQLAlchemy Models"""
import pytest
from database import SessionLocal, engine
import models

from datetime import date, timedelta

@pytest.fixture(scope="function")
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()


def test_player_query(db_session):
    """Tests that the count of players in the database is what is expected"""
    players = db_session.query(models.Player).all()
    assert len(players) == 160

def test_performances_query(db_session):
    """Tests that the count of performances in the database is what is expected"""
    performances = db_session.query(models.Performance).all()
    assert len(performances) == 320


def test_performances_date_query(db_session):
    """Tests that the count of performances newer than a date"""
    date_query = db_session.query(models.Performance).filter(
        models.Performance.last_changed_date >= '2024-04-01'
    )
    performances = date_query.all()
    assert len(performances) == 160
    


def test_leagues_query(db_session):
    """Tests that the count of leagues in the database is what is expected"""
    leagues = db_session.query(models.League).all()
    assert len(leagues) == 5
    
def test_teams_query(db_session):
    """Tests that the count of teams in the database is what is expected"""
    teams = db_session.query(models.Team).all()
    assert len(teams) == 20

def test_team_player_query(db_session):
    """Tests that the count of team_player records in the database is what is expected"""
    team_players = db_session.query(models.TeamPlayer).all()
    assert len(team_players) == 160


