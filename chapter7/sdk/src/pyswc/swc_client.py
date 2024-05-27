import httpx
import pyswc.swc_config as config
import logging


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
        """Class constructor that sets varibles from configuration object."""

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Input config: " + str(input_config))

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time

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
