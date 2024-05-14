#SDK client
import httpx
import pyswc.swc_config as config
import logging
from .schemas.sdk_schemas import League, LeagueWrapper, LeaguesWrapper

class SWC_Client:
    HEALTH_CHECK_ENDPOINT = "/"
    GET_LEAGUES_ENDPOINT = "/v0/leagues/"
    #GET_LEAGUE_BY_ID_ENDPOINT = "/v0/leagues/{league_id}/"
    GET_PLAYERS_ENDPOINT = "/v0/players/"
    #GET_PLAYER_BY_ID_ENDPOINT = "/v0/players/{player_id}/"
    GET_PERFORMANCES_ENDPOINT = "/v0/performances/"
    GET_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    def __init__(self, input_config: config.SWC_Config = None):
        #create a config
        self.swc_base_url = input_config.swc_base_url
        self.logger = logging.getLogger(__name__)
        self.timeout = input_config.swc_timeout



    def health_check(self):
        #initial logging message
        self.logger.debug("Entered health check")
        #call the health check
        response = httpx.get(self.swc_base_url + self.HEALTH_CHECK_ENDPOINT)
        #what do I return if anything?
        return response

    def get_leagues(self):
        #initial logging message
        self.logger.debug("Entered get leagues")        
        #call the API to real league, raise error for non-200 response
        with httpx.Client(base_url=self.swc_base_url, timeout=self.timeout) as client:
            response = client.get(self.GET_LEAGUES_ENDPOINT)
        self.logger.debug(response.json())
        #return response
        responseLeagues = [League(**league) for league in response.json()]
        self.logger.debug(f"response code: {response.status_code}")     
        wrappedResponse = LeaguesWrapper(http_response_code = response.status_code, response_leagues = responseLeagues)
        return wrappedResponse

    def get_league_by_id(self, league_id: int):
        #initial logging message
        self.logger.debug("Entered get league by ID")        
        #call the API to real league, raise error for non-200 response
        with httpx.Client(base_url=self.swc_base_url, timeout=self.timeout) as client:
            response = client.get(f"{self.GET_LEAGUES_ENDPOINT}{league_id}")
        self.logger.debug(response.json())
        #return response
        wrappedResponse = LeagueWrapper(http_response_code = response.status_code, response_league = League(** response.json()))
        return wrappedResponse
