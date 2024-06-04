class SWCConfig:
    """Configuration class containing arguments for the SDK client.

    Contains configuration for the base URL and progressive backoff.
    """

    DEFAULT_URL = "https://api.sportsworldcentral.com"

    swc_base_url: str
    swc_backoff: bool
    swc_backoff_max_time: int

    def __init__(
        self, url: str = DEFAULT_URL, backoff: bool = True, backoff_max_time: int = 30
    ):
        """Constructor for configuration class.

        Contains initialization values to overwrite defaults.

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