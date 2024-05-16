#SDK client
import httpx
import pyswc.swc_config as config
import logging
from .schemas import League, Player, Performance, Team, Counts
from .errors import SWCError
import backoff
from urllib.parse import urlencode


class SWC_Client:
    HEALTH_CHECK_ENDPOINT = "/"
    GET_LEAGUES_ENDPOINT = "/v0/leagues/"
    #GET_LEAGUE_BY_ID_ENDPOINT = "/v0/leagues/{league_id}/"
    GET_PLAYERS_ENDPOINT = "/v0/players/"
    #GET_PLAYER_BY_ID_ENDPOINT = "/v0/players/{player_id}/"
    GET_PERFORMANCES_ENDPOINT = "/v0/performances/"
    GET_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_PATHS = {
        "players": "https://raw.githubusercontent.com/Ryandaydev/portfolio-project/main/chapter3/data/player_data.csv",
        "leagues": "https://raw.githubusercontent.com/Ryandaydev/portfolio-project/main/chapter3/data/league_data.csv",
        "performances": "https://raw.githubusercontent.com/Ryandaydev/portfolio-project/main/chapter3/data/performance_data.csv",
        "teams": "https://raw.githubusercontent.com/Ryandaydev/portfolio-project/main/chapter3/data/team_data.csv",
        "team_players": "https://raw.githubusercontent.com/Ryandaydev/portfolio-project/main/chapter3/data/team_player_data.csv"
    }


    def __init__(self, input_config: config.SWC_Config = None):
        #create a config
        self.logger = logging.getLogger(__name__)

        #initial with config values
        self.swc_base_url = input_config.swc_base_url
        self.timeout = input_config.swc_timeout
        self.backoff =  input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time

        self.logger.debug("Input config: " + str(input_config))

        #if the client was called with backoff, decorate the get_url with backoff logic
        if self.backoff:
            self.get_url = self._apply_backoff(self.get_url)

    #the backoff logic to decorate the function with
    def _apply_backoff(self, func):
        return backoff.on_exception(backoff.expo, (httpx.RequestError, SWCError), max_time=self.backoff_max_time, jitter=backoff.random_jitter)(func)


    def build_url(self, endpoint, params=None):
        if params:
            query_string = urlencode(params)
            full_url = endpoint + "?" + query_string
        else:
            full_url = endpoint
        return full_url


    def get_url(self, url):
            try:
                with httpx.Client(base_url=self.swc_base_url, timeout=self.timeout) as client:
                        return client.get(url)
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP status error occurred: {e.response.status_code} {e.response.text}")
                return e.response
            except httpx.RequestError as e:
                self.logger.error(f"Request error occurred: {str(e)}")
                raise SWCError(f"Request error: {str(e)}") from e


#Below here are individual endpoints



    #analytics endpoints
    def health_check(self):
        #initial logging message
        self.logger.debug("Entered health check")
        #build URL
        endpoint_url = self.HEALTH_CHECK_ENDPOINT
        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return response
    
    def get_counts(self):
        #initial logging message
        self.logger.debug("Entered get counts")
        #build URL
        endpoint_url = self.GET_COUNTS_ENDPOINT
        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())
            responseCounts = Counts(** response.json())
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responseCounts


    #membership endpoints

    #standard format
    def get_league_by_id(self, league_id: int):
        #initial logging message
        self.logger.debug("Entered get league by ID - with backoff")        
        #build URL
        endpoint_url = f"{self.GET_LEAGUES_ENDPOINT}{league_id}"
        #make the API call
        response = self.get_url(endpoint_url)

        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())
            responseLeague = League(** response.json())
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responseLeague
    
    def get_leagues(self, 
                     skip: int = 0, 
                     limit: int = 100, 
                     minimum_last_changed_date: str = None, 
                     league_name: str = None):
        #initial logging message
        self.logger.debug("Entered get leagues")        

        params = { 'skip':skip, 
                        'limit':limit, 
                        'minimum_last_changed_date':minimum_last_changed_date,
                        'league_name' : league_name}
        
        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None} 

        endpoint_url = self.build_url(self.GET_LEAGUES_ENDPOINT, params)

        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())        
            responseLeagues = [League(**league) for league in response.json()]
            #wrappedResponse = LeaguesWrapper(http_response_code = response.status_code, response_leagues = responseLeagues)
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responseLeagues    

    def get_teams(self, 
                     skip: int = 0, 
                     limit: int = 100, 
                     minimum_last_changed_date: str = None, 
                     team_name: str = None,
                     league_id: int = None):
        #initial logging message
        self.logger.debug("Entered get teams")        

        params = { 'skip':skip, 
                        'limit':limit, 
                        'minimum_last_changed_date':minimum_last_changed_date,
                        'team_name' : team_name,
                        'league_id' : league_id}
        
        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None} 

        endpoint_url = self.build_url(self.GET_TEAMS_ENDPOINT, params)

        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())        
            responseTeams = [Team(**team) for team in response.json()]
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responseTeams    


#players endpoints    
    def get_players(self, 
                     skip: int = 0, 
                     limit: int = 100, 
                     minimum_last_changed_date: str = None, 
                     first_name: str = None,
                     last_name: str = None,):
        #initial logging message
        self.logger.debug("Entered get players")        

        params = { 'skip':skip, 
                        'limit':limit, 
                        'minimum_last_changed_date':minimum_last_changed_date,
                        'first_name' : first_name,
                        'last_name' : last_name}
        
        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None} 

        endpoint_url = self.build_url(self.GET_PLAYERS_ENDPOINT, params)

        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())        
            responsePlayers = [Player(**player) for player in response.json()]
            #wrappedResponse = LeaguesWrapper(http_response_code = response.status_code, response_leagues = responseLeagues)
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responsePlayers       
    
    def get_player_by_id(self, player_id: int):
        #initial logging message
        self.logger.debug("Entered get player by ID")        
        #build URL
        endpoint_url = f"{self.GET_PLAYERS_ENDPOINT}{player_id}"
        #make the API call
        response = self.get_url(endpoint_url)

        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())
            responsePlayer = Player(** response.json())
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responsePlayer

#scoring endpoints
    def get_performances(self, 
                     skip: int = 0, 
                     limit: int = 100, 
                     minimum_last_changed_date: str = None ):
        #initial logging message
        self.logger.debug("Entered get performances")        

        params = { 'skip':skip, 
                        'limit':limit, 
                        'minimum_last_changed_date':minimum_last_changed_date}
        
        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None} 

        endpoint_url = self.build_url(self.GET_PERFORMANCES_ENDPOINT, params)

        #make the API call
        response = self.get_url(endpoint_url)
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug(response.json())        
            responsePerformances = [Performance(**performance) for performance in response.json()]
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return responsePerformances       
    
#bulk endpoints
    def get_bulk_players(self):
        #initial logging message
        self.logger.debug("Entered get bulk players")
        response = httpx.get(self.BULK_FILE_PATHS["players"])
        #review status of API call
        #check if it's a 200
        if response.status_code == 200:
            self.logger.debug("File downloaded successfully")
            return response.content 
        elif response.status_code >= 400 and response.status_code < 500 or response.status_code >= 500 and response.status_code < 600:
            self.logger.exception(f"API error occurred: {response.text}")
            raise SWCError('API error occurred', response.status_code, response.text, response)
        else:
            raise SWCError('unknown status code received', response.status_code, response.text, response)
        return response
    

