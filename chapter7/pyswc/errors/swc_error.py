import httpx

class SWCError(Exception):
    """Represents an error returned by the SWC API - inspired by Speakeasy SDK"""
    message: str
    status_code: int
    body: str
    raw_response: httpx.Response

    def __init__(self, message: str, status_code: int = None, body: str = None, raw_response: httpx.Response = None):
        self.message = message
        self.status_code = status_code
        self.body = body
        self.raw_response = raw_response

    def __str__(self):
        body = ''
        if len(self.body) > 0:
            body = f'\n{self.body}'

        return f'{self.message}: Status {self.status_code}{body}'