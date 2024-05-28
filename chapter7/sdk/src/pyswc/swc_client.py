import httpx
import pyswc.swc_config as config
import logging
from urllib.parse import urlencode
from .schemas import League
from typing import List
import backoff


class SWCClient:
    """Interacts with the Sports World Central API.

        This SDK class simplifies the process of using the SWC fantasy
        football API. It supports all the functions of SWC API and returns
        validated datatypes.

    Typical usage example:

        client = SWCClient()
        response = client.get_health_check()

    """

    HEALTH_CHECK_ENDPOINT = "/"
    GET_LEAGUES_ENDPOINT = "/v0/leagues/"

    BULK_FILE_BASE_URL = ("https://raw.githubusercontent.com/ryandaydev" + 
                            "/portfolio-project/main/chapter7/sdk/bulk/")

    BULK_FILE_NAMES = {
        "players": "player_data.csv",
        "leagues": "league_data.csv",
        "performances": "performance_data.csv",
        "teams": "team_data.csv",
        "team_players": "team_player_data.csv"
    }

    def __init__(self, input_config: config.SWCConfig):
        """Class constructor that sets varibles from configuration object."""

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Input config: " + str(input_config))

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time

        if self.backoff:
            self.get_url = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.get_url)

    def get_url(self, url: str) -> httpx.Response:
        """Makes API call and logs errors."""
        try:
            with httpx.Client(base_url=self.swc_base_url) as client:
                response = client.get(url)
                self.logger.debug(response.json())
                return response
        except httpx.HTTPStatusError as e:
            self.logger.error(
                f"HTTP status error occurred: {e.response.status_code} {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            self.logger.error(f"Request error occurred: {str(e)}")
            raise

    def get_health_check(self) -> httpx.Response:
        """Checks if API is running and healthy.

        Calls the API health check endpoint and returns a standard
        message if the API is running normally. Can be used to check
        status of API before making more complicated API calls.

        Returns:
          An httpx.Response object that contains the HTTP status,
          JSON response and other information received from the API.

        """
        self.logger.debug("Entered health check")
        endpoint_url = self.HEALTH_CHECK_ENDPOINT
        return self.get_url(endpoint_url)

    def build_url(self, endpoint, params=None) -> str:
        """Converts dictionary of parameters to query string and appends to URL"""
        if params:
            params_dict = {
                key: value for (key, value) in params.items() if value is not None
            }
            query_string = urlencode(params_dict)
            full_url = endpoint + "?" + query_string
        else:
            full_url = endpoint
        return full_url

    def get_leagues(
        self,
        skip: int = 0,
        limit: int = 100,
        minimum_last_changed_date: str = None,
        league_name: str = None,
    ) -> List[League]:
        """Returns a List of Leagues filtered by parameters.

        Calls the API v0/leagues endpoint and returns a list of
        League objects.

        Returns:
        A List of schemas.League objects. Each represents one
        SportsWorldCentral fantasy league.

        """
        self.logger.debug("Entered get leagues")

        params = {
            "skip": skip,
            "limit": limit,
            "minimum_last_changed_date": minimum_last_changed_date,
            "league_name": league_name,
        }

        endpoint_url = self.build_url(self.GET_LEAGUES_ENDPOINT, params)
        
        response = self.get_url(endpoint_url)
        return [League(**league) for league in response.json()]

    def get_bulk_players(self) -> bytes:
        """Returns a CSV file with player data"""

        self.logger.debug("Entered get bulk players")

        player_file_path = (self.BULK_FILE_BASE_URL + self.BULK_FILE_NAMES["players"])
        
        response = httpx.get(player_file_path)

        if response.status_code == 200:
            self.logger.debug("File downloaded successfully")
            return response.content