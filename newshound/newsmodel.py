from newshound.util import classproperty

class BaseSource(object):
    @classproperty
    def config_options(cls):
        """Return the information needed to configure a source."""
        return {"url":{"type":"string/url"}}
    
    @classproperty
    def account_class(cls):
        return BaseAccount
    
class BaseAccount(object):
    pass
