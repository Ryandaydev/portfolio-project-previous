#configuration file
import logging

class SWC_Config:
    swc_base_url = "https://api.sportsworldcentral.com"
    swc_timeout = 5.0
    
    def __init__(self, url: str = None, timeout: float = None):
            if url:
                    self.swc_base_url = url
            if timeout:
                    self.swc_timeout = timeout


