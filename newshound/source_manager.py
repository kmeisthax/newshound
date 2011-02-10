from newshound import newsmodel
import os.path

class SourceManager(object):
    def __init__(self):
        self.sources = []
        self.moduleIndex = {}
        
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
            self.moduleIndex[module] = []
            try:
                self.moduleIndex[module].extend(module.NEWS_PROVIDERS)
                self.sources.extend(module.NEWS_PROVIDERS)
