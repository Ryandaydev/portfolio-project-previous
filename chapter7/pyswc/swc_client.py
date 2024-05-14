#SDK client
import httpx
import pyswc.swc_config as config
import logging

class SWC_Client:
    HEALTH_CHECK_ENDPOINT = "/"
    GET_LEAGUES_ENDPOINT = "/v0/leagues/"
    GET_PLAYERS_ENDPOINT = "/v0/players/"
    GET_PLAYER_BY_ID_ENDPONT = "/v0/players/{player_id}/"
    GET_PERFORMANCES_ENDPOINT = "/v0/performances/"
    GET_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    def __init__(self, input_config: config.SWC_Config = None):
        #create a config
        self.swc_base_url = input_config.swc_base_url
        self.logger = logging.getLogger(__name__)



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
        #call the API to real leagues
        response = httpx.get(self.swc_base_url + self.GET_LEAGUES_ENDPOINT)

        #what do I return if anything?
        return response

    def get_leagues(self):
        #initial logging message
        self.logger.debug("Entered get leagues")        
        #call the API to real leagues
        response = httpx.get(self.swc_base_url + self.GET_LEAGUES_ENDPOINT)
        
        #what do I return if anything?
        return response

