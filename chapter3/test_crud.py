"""Testing SQLAlchemy Models"""
import pytest
from sqlalchemy.orm import Session

import crud, models
from database import SessionLocal, engine

from datetime import date, timedelta

test_date = date(2024,4,4)

@pytest.fixture(scope="function")
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()

def test_get_players(db_session):
    """Tests that the count of players in the database is what is expected"""
    players = crud.get_players(db_session, skip=0, limit=500, min_last_changed_date=test_date)
    assert len(players) == 160

def test_get_performances(db_session):
    """Tests that the count of performances in the database is what is expected - half the performances"""
    performances = crud.get_performances(db_session, skip=0, limit=500, min_last_changed_date=test_date)
    assert len(performances) == 160

def test_get_performances_by_earlier_date(db_session):
    """Tests that the count of performances in the database is what is expected - all the performances"""
    performances = crud.get_performances(db_session, skip=0, limit=500, min_last_changed_date=date(2024,1,1))
    assert len(performances) == 320

def test_get_leagues(db_session):
    """Tests that the count of leagues in the database is what is expected"""
    leagues = crud.get_leagues(db_session, skip=0, limit=500, min_last_changed_date=test_date)
    assert len(leagues) == 5

def test_get_teams(db_session):
    """Tests that the count of teams in the database is what is expected"""
    teams = crud.get_teams(db_session, skip=0, limit=500, min_last_changed_date=test_date)
    assert len(teams) == 20


def test_get_team_players(db_session):
    """Tests that a team record can retrieve players, and that 8 players are on the first team"""
    first_team = crud.get_teams(db_session, skip=0, limit=500, min_last_changed_date=test_date)[0]
    assert len(first_team.players) == 8