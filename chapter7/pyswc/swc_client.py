#SDK client
import httpx

# def __init__(self):
#     #create a config
    
#     #create a session
#     session = httpx.

def health_check():
    #call the health check
    response = httpx.get("https://api.sportsworldcentral.com")
    #what do I return if anything?
    return response

