import os.path, json
from newshound import datasrc

class Core(object):
    def __init__(self):
        self.src = datasrc.SourceManager()
        
        self.plugins_init()
    
    def load_config(self, config_files = None):
        if config_files is None:
            config_files = os.path.expanduser(os.path.join("~", ".config", "newshound", "mana-src.json"))
            
        if os.path.exists(config_files):
            config = json.load(open(config_files))
            self.src.load_config(config)
            
    def store_config(self, config_files = None):
        if config_files is None:
            config_files = os.path.expanduser(os.path.join("~", ".config", "newshound", "mana-src.json"))
            
        if os.path.exists(config_files):
            json.dump(self.src.store_config(), open(config_files))
            
    def plugins_init(self):
        self.load_config()
        self.src.find_plugins()
        self.store_config()
