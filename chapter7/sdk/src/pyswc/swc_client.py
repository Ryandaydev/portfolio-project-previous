import httpx


class SWC_Client:
    """Interacts with the Sports World Central API.

        This SDK class simplifies the process of using the SWC fantasy
        football API. It supports all the functions of SWC API and returns
        validated datatypes.

    Typical usage example:

        client = SWC_Client()
        response = client.get_health_check()

    """

    HEALTH_CHECK_ENDPOINT = "/"

    def __init__(self, swc_base_url: str) -> None:
        """Class constructor that sets the base URL."""
        self.swc_base_url = swc_base_url

    def get_health_check(self) -> httpx.Response:
        """Checks if API is running and healthy.

        Calls the API healtch check endpoint and returns a standard
        message if the API is running normally. Can be used to check
        status of API before making more complicated API calls.

        Returns:
          An httpx.Response object that contains the HTTP status,
          JSON response and other information received from the API.

        """
        # make the API call
        with httpx.Client(base_url=self.swc_base_url) as client:
            return client.get(self.HEALTH_CHECK_ENDPOINT)
