from urlparse import urlparse, urlunparse

class Reddit(object):
    def __init__(self, url = "http://reddit.com"):
        self.url = urlparse(url)

    def login(self, account):
