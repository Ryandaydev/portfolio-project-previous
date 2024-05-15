#configuration file
import logging

class SWC_Config:
    swc_base_url = "https://api.sportsworldcentral-false.com"
    swc_timeout = 5.0
    swc_backoff = True
    swc_backoff_max_time=30

    
    def __init__(self, url: str = None, timeout: float = None, backoff: bool = None, backoff_max_time: int = None):
        if url:
                self.swc_base_url = url
        if timeout:
                self.swc_timeout = timeout
        if backoff:
                self.swc_backoff = backoff
        if backoff_max_time:
                self.swc_backoff_max_time = backoff_max_time



