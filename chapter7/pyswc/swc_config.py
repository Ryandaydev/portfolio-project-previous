#configuration file
import logging

class SWC_Config:
    swc_base_url = "https://api.sportsworldcentral.com"
    
    def __init__(self, url: str = None):
            if url:
                    self.swc_base_url = url



