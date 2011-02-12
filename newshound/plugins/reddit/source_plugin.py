from newshound import api
from newshound.util import classproperty
import urllib2, urlparse, json

SUBREDDIT_LISTING_URL = "/reddits/.json"

KIND_LIST = "Listing"
KIND_SUBREDDIT = "t5"
KIND_SUBMISSION = "t3"

class Subreddit(api.BaseSection):
    def __init__(self, parent=None):
        self.parent = parent
        self.backing_data = {}

    def incorporate_json(self, secjson):
        if secjson["kind"] != KIND_SUBREDDIT:
            raise api.BadResponseException()

        for key in secjson["data"].keys():
            self.backing_data[key] = secjson["data"][key]

    def list_sections(self):
        #there are no sub-subreddits
        return []

class RedditSource(api.BaseSource, Subreddit):
    def __init__(self, *args, **kwargs):
        self.subreddits = {}

        super(RedditSource, self).__init__(*args, **kwargs)

    @classproperty
    def config_options(cls):
        defaults = super(RedditSource, cls).config_options
        defaults["url"]["default"] = "http://reddit.com/"
        
        return defaults
        
    @classproperty
    def account_class(cls):
        """We currently don't support accounts"""
        return None
        
    def write_config_data(self, config_data):
        self.url = config_data["url"]
        
    def list_sections(self):
        sec_url = urlparse.urljoin(self.url, SUBREDDIT_LISTING_URL)
        urlfile = urllib2.urlopen(sec_url)
        
        sections_json = json.load(urlfile)

        if sections_json["kind"] != KIND_LIST:
            raise api.BadResponseException()

        returns = []

        for subreddit_json in sections_json["data"]["children"]:
            sr = None
            if self.subreddits.keys().count(subreddit_json["data"]["id"]) > 0:
                sr = self.subreddits[subreddit_json["data"]["id"]]
            else:
                sr = Subreddit(self)
                self.subreddits[subreddit_json["data"]["id"]] = sr

            sr.incorporate_json(subreddit_json)
            
