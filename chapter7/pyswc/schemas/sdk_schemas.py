"""Pydantic schemas"""
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date


class Performance(BaseModel):
    #model_config = ConfigDict(from_attributes = True)
    performance_id : int
    player_id : int
    week_number : str
    fantasy_points : float
    last_changed_date : date
        
# class PerformancesWrapper(BaseModel):
#     http_response_code : int
#     response_league: list[Performance]

class PlayerBase(BaseModel):
    #model_config = ConfigDict(from_attributes = True)    
    player_id : int
    gsis_id: str
    first_name : str
    last_name : str
    position : str
    last_changed_date : date

class Player(PlayerBase):
    #model_config = ConfigDict(from_attributes = True)
    performances: List[Performance] = []

# class PlayerWrapper(BaseModel):
#     http_response_code : int
#     response_league: Player

# class PlayersWrapper(BaseModel):
#     http_response_code : int
#     response_league: list[Player]

class TeamBase(BaseModel):
    #model_config = ConfigDict(from_attributes = True)
    league_id : int
    team_id : int
    team_name : str
    last_changed_date : date

class Team(TeamBase):
    #model_config = ConfigDict(from_attributes = True)
    players: List[PlayerBase] = []

# class TeamWrapper(BaseModel):
#     http_response_code : int
#     response_league: Team

# class TeamsWrapper(BaseModel):
#     http_response_code : int
#     response_leagues: list[Team]

class League(BaseModel):
    #model_config = ConfigDict(from_attributes = True)
    league_id : int
    league_name : str
    scoring_type : str
    last_changed_date : date
    teams: List[TeamBase] = []

# class LeagueWrapper(BaseModel):
#     http_response_code : int
#     response_league: League
    
# class LeaguesWrapper(BaseModel):
#     http_response_code : int
#     response_leagues: list[League]

class Counts(BaseModel):
    league_count : int
    team_count : int
    player_count : int

# class CountsWrapper(BaseModel):
#     http_response_code : int
#     response_counts: Counts

