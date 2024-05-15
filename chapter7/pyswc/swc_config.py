#configuration file
import logging

class SWC_Config:
    swc_base_url: str
    swc_timeout: int
    swc_backoff: bool
    swc_backoff_max_time: int

    def __init__(self, url: str = "https://api.sportsworldcentral.com", timeout: float = 5.0, backoff: bool = True, backoff_max_time: int = 30):
        self.swc_base_url = url
        self.swc_timeout = timeout
        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time

    def __str__(self):
         return f"{self.swc_base_url} {self.swc_timeout} {self.swc_backoff} {self.swc_backoff_max_time}"


