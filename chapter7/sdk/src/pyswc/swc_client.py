#SDK client
import httpx

class SWC_Client:
    HEALTH_CHECK_ENDPOINT = "/"

    def __init__(self):

        #initial with config values
        self.swc_base_url = "https://api.sportsworldcentral.com"

    #analytics endpoints
    def health_check(self):
        #make the API call
        with httpx.Client(base_url=self.swc_base_url) as client:
                        return client.get(self.HEALTH_CHECK_ENDPOINT)