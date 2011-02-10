from newshound.util import classproperty

class InvalidAccountException(Exception):
    pass

class BaseSection(object):
    SECTION_SUBSCRIBED = 0
    SECTION_SUGGESTED = 50
    SECTION_UNSUBSRIBED = 100
    def list_sections(self, status=SECTION_SUBSCRIBED):
        """Return the currently available sections in a particular source.
        
        The status parameter filters what sections are returned. SUBSCRIBED
        sections should appear in the home view, while SUGGESTED sections are
        ones that the news source has specifically suggested but are not subscribed.
        
        UNSUBSCRIBED sections will not appear in the home view, and may or may not
        also be SUGGESTED. A source may return UNSUBSCRIBED sections other than
        SUGGESTED sections, but must return SUGGESTED sections, if there are any,
        in the UNSUBSCRIBED list.
        
        Sections are themselves Source objects, and can have sub-sections, if that
        makes sense for the underlying news Source."""
        
        return []
    
    STORY_SORT_DEFAULT = 0
    STORY_SORT_NEW = 1
    STORY_SORT_POPULAR = 2
    def list_stories(self, count=20, start=None):
        """Retrieve stories from the source.
        
        The count parameter determines how many stories to request, and the start
        parameter determines from when to request them. The count parameter is a
        suggestion and may not be honored. The start parameter must be a story from
        this source, and may also not be honored, in which returned stories will
        start from the latest story."""
        
        return []
        
    def register_story_callback(self, func, *data_args, **data_kwargs):
        """Register a callback to recieve notification of new stories.
        
        The story callback is called whenever this source recieves a new story.
        It is not guaranteed to list all new stories.
        
        The story callback signature is as follows:
        
        callback(source, stories, *data_args, **data_kwargs)"""
        
        self.callbacks["story"] += (func, data_args, data_kwargs)
        
    def refresh(self):
        """Refresh the source.
        
        What this means is that it will check for new content and call any
        appropriate callbacks."""
        
        return


class BaseSource(BaseSection):
    def __init__(self, *args, **kwargs):
        self.callbacks = {"story":[]}
        
        super(BaseSection, self).__init__(*args, **kwargs)

    @classproperty
    def config_options(cls):
        """Return the information needed to configure a source."""
        return {"url":{"type":"string/url"}}
    
    @classproperty
    def account_class(cls):
        return BaseAccount
        
    @classproperty
    def allow_anonymous_reading(cls):
        return True
        
    def write_config_data(self, config_data):
        #if type(account) != self.account_class:
        #    if account != None and not self.allow_anonymous_reading:
        #        raise InvalidAccountException
            
        #self.account = account
        self.url = config_data["url"]
    
class BaseAccount(object):
    pass
