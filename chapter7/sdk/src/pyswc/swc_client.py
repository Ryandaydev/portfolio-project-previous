import httpx
import pyswc.swc_config as config


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

    def __init__(self, input_config: config.SWCConfig):
        """Class constructor that sets varibles from configuration object"""

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time

    def get_health_check(self) -> httpx.Response:
        """Checks if API is running and healthy.

        Calls the API health check endpoint and returns a standard
        message if the API is running normally. Can be used to check
        status of API before making more complicated API calls.

        Returns:
          An httpx.Response object that contains the HTTP status,
          JSON response and other information received from the API.

        """
        # make the API call
        with httpx.Client(base_url=self.swc_base_url) as client:
            return client.get(self.HEALTH_CHECK_ENDPOINT)
