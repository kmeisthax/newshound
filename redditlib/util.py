class HTTPRequestHack(object):
    """Wrap an httplib request in a way that CookieLib will accept it."""
    def __init__(self, location, 
