from newshound.util import classproperty

class InvalidAccountException(Exception):
    pass

class BadResponseException(Exception):
    pass

class BadConfigException(Exception):
    pass

class GenericSourcePlugin(Exception):
    pass

class BaseSection(object):
    def __init__(self, *args, **kwargs):
        self.callbacks = {"story":[]}
        
        super(BaseSection, self).__init__(*args, **kwargs)

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
    @classproperty
    def config_options(cls):
        """Return the information needed to configure a source."""
        return {"url":{"type":str, "ui_str":"URL", "required":True}}
    
    @classproperty
    def account_class(cls):
        return BaseAccount
        
    @classproperty
    def allow_anonymous_reading(cls):
        return True

    @classproperty
    def allow_default_source(cls):
        return True
        
    def store_config(self):
        """Implementation of config storing that uses the config_options class property to determine serializable data.

        Relies on a working config_options. If you don't want to provide one, override this function too."""
        config_dict = {}

        for config_name in self.config_options:
            if self.__dict__.keys().count(config_name) > 0:
                config_dict[config_name] = self.__dict__[config_name]

        return config_dict

    def load_config(self, input_config):
        """Restore config from the input dictionary.

        Like store_config, it operates based on config_options."""

        for pkey in input_config:
            if self.config_options.keys().count(pkey) > 0:
                if type(input_config[pkey]) is self.config_options[pkey]["type"]:
                    self.__dict__[pkey] = input_config[pkey]
                else:
                    raise BadConfigException()

    @classproperty
    def default_source(cls):
        """Return a default source for a given object, if the source supports it.

        A default source is intended for single-website plugins, such as a Reddit plugin. In these cases,
        we should just place that source on the sources list automatically and let the user configure it later.

        If a plugin's config_options specify defaults for all required options, and allow_default_source is True,
        you'll get a default source plugin."""

        if not cls.allow_default_source:
            raise GenericSourcePlugin()

        defaults = {}

        for key in self.config_options:
            if self.config_options[key].keys().count("default") > 0:
                defaults[key] = self.config_options[key]["default"]
            elif self.config_options[key].keys().count("required") > 0 and self.config_options[key]["required"]:
                raise GenericSourcePlugin()

        defsrc = cls()
        defsrc.load_config(defaults)
    
class BaseAccount(object):
    pass
