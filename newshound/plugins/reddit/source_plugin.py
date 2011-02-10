from newshound import newsmodel
from newshound.util import classproperty
import urllib2, urlparse, json

def Subreddit(newsmodel.BaseSection):
    def __init__
    def list_sections(self):
        #there are no sub-subreddits
        return []

def RedditSource(newsmodel.BaseSource, Subreddit):
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
        
    SUBREDDIT_LISTING_URL = "/reddits/.json"
    
    KIND_LIST = "Listing"
    KIND_SUBREDDIT = "t5"
    KIND_SUBMISSION = "t3"
    def list_sections(self):
        sec_url = urlparse.urljoin(self.url, self.SUBREDDIT_LISTING_URL)
        urlfile = urllib2.urlopen(sec_url)
        
        sections_json = json.load(urlfile)
