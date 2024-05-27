class SWCConfig:
    """Configuration class containing arguments for the SDK client.

    Contains configuration for the base URL along with several
    parameters used to configure the progressive backoff feature
    of the SDK, which prevents the SDK from overwhelming the
    API with requests.

    Typical usage example with all defaults:
    config = SWC_Config("http://127.0.0.1:8000")
    client = SWC_Client(config)

    Typical usage example specifying all the parameters:
    config = SWC_Config(swc_base_url = "http://127.0.0.1:8000",
                        swc_backoff = True,
                        swc_backoff_max_time = 15)
    client = SWC_Client(config)


    """

    DEFAULT_URL = "https://api.sportsworldcentral.com"

    swc_base_url: str
    swc_backoff: bool
    swc_backoff_max_time: int

    def __init__(
        self, url: str = DEFAULT_URL, backoff: bool = True, backoff_max_time: int = 30
    ):
        """Constructor for configuration class.

        Contains configuration for the base URL along with several
        parameters used to configure the progressive backoff feature,
        which prevents the SDK from overwhelming the API with requests.

        Args:
        swc_base_url (optional):
            The base URL to use for all the API calls.
        swc_backoff:
            A boolean that determines if the SDK should
            retry the call using backoff when errors occur.
        swc_backoff_max_time:
            The max number of seconds the SDK should keep
            trying an API call before stopping."""

        self.swc_base_url = url
        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time

    def __str__(self):
         """Stringify function to return contents of config object for logging"""
         return f"{self.swc_base_url} {self.swc_backoff} {self.swc_backoff_max_time}"