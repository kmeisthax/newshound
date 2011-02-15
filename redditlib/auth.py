from urlparse import urlparse, urlunparse
import httplib, cookielib, urllib, urllib2, json

class Account(object):
    def __init__(self, user = "", auth_pass = "", reddit = "http://reddit.com"):
        self.user = user
        self.auth_pass = auth_pass
        self.reddit = urlparse(reddit)

        self.logged_in = False
        self.jar = cookielib.CookieJar()

    def login(self):
        params = urllib.urlencode({"user":self.user, "passwd":self.auth_pass})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        request = urllib2.Request(
            urlunparse((self.reddit[0], self.reddit[1], "/api/login", "", "", ""),params,headers)
        self.jar.add_cookie_header(request)
        
        conn.request("POST", "/api/login", params, headers)
        response = conn.getresponse()
        response_json = json.loads(response.read())

        self.jar.extract_cookies(response, 
