from newshound import newsmodel
import os.path, json

class SourceManager(object):
    def __init__(self):
        self.source_classes = []
        self.module_index = {}
        self.sources = []
        
    def find_plugins(self):
        plugins_dir = os.path.join(os.path.split(__file__)[0], "plugins")
        plugin_modules = []

        for entry in os.listdir(plugins_dir):
            entry_path = os.path.join(plugins_dir, entry)
            if os.path.isdir(entry_path):
                __import__("newshound.plugins." + entry)
                plugin_modules += sys.modules["newshound.plugins." + entry)
            elif os.path.isfile(entry_path):
                entry_spl = os.path.splitext(entry)
                if entry_spl[1] = ".py":
                    __import__("newshound.plugins." + entry_spl[0])
                    plugin_modules += sys.modules["newshound.plugins." + entry_spl[0])
        
        for module in plugin_modules:
            try:
                for source_class in module.NEWS_PROVIDERS:
                    self.module_index[source_class] = module
                
                self.source_classes.extend(module.NEWS_PROVIDERS)
            except:
                pass
                
    def store_source_configuration(self, config_path = None):
        """Form all the data in the source down to a data dictonary to be serialized to a file somehow."""
        if config_path == None:
            config_path = os.path.join(os.path.expanduser("~"), ".newshound")
            
        source_config_file = os.path.join(config_path, "sources")
        source_config_object = {"version":[0,0], "src_classes":[], "sources":[]}

        #gather up all the source classes
        for source_class in self.source_classes:
            module = self.module_index[source_class].__name__
            classname = source_class.__name__

            src_class = {"module":module, "class":classname}
            source_config_object["src_classes"] += src_class
