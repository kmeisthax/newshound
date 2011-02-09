from newshound import newsmodel
from newshound.util import classproperty

def RedditSource(newsmodel.BaseSource):
    @classproperty
    def config_options(cls):
        defaults = super(RedditSource, cls).config_options
        defaults["url"]["default"] = "http://reddit.com"
        
        return defaults
        
    @classproperty
    def account_class(cls):
        """We currently don't support accounts"""
        return None
        
    def write_config_data(self, config_data):
        self.url = config_data["url"]
        
    def list_sections(self):
        
