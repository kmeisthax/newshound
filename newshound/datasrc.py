from newshound import api
import os.path, json

CONFIG_MAJOR_VERSION = 0
CONFIG_MINOR_VERSION = 0

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
                plugin_modules += sys.modules["newshound.plugins." + entry]
            elif os.path.isfile(entry_path):
                entry_spl = os.path.splitext(entry)
                if entry_spl[1] = ".py":
                    __import__("newshound.plugins." + entry_spl[0])
                    plugin_modules += sys.modules["newshound.plugins." + entry_spl[0]]
        
        for module in plugin_modules:
            try:
                for source_class in module.NEWS_PROVIDERS:
                    self.module_index[source_class] = module
                    new_module = True

                    for source_instance in self.sources:
                        if isinstance(source_instance, source_class):
                            new_module = False

                    if new_module:
                        try:
                            self.sources += source_class.default_source
                        except newsmodel.GenericSourcePlugin:
                            pass
                
                self.source_classes.extend(module.NEWS_PROVIDERS)
            except:
                pass
                
    def store_config(self):
        """Form all the data in the source down to a data dictonary to be serialized to a file somehow."""
        source_config_object = {"version":[CONFIG_MAJOR_VERSION, CONFIG_MINOR_VERSION], "src_classes":[], "sources":[]}

        #gather up all the source classes
        for source_class in self.source_classes:
            module = self.module_index[source_class].__name__
            classname = ".".join([source_class.__module__, source_class.__name__])

            src_class = {"module":module, "class":classname}
            source_config_object["src_classes"] += src_class

        #gather up all the source class instances
        for source in self.sources:
            classname = source.__class__.__name__
            config = source.store_config()

            inst_class = {"class":classname, "data":config}
            source_config_object["sources"] += inst_class

    def load_config(self, input_config):
        """The opposite of store_config, this function loads source config data from a dictionary."""

        #Since we want to be able to load as much of the user's configuration as possible,
        #let's store exception objects here and raise them after everything's done.
        delay_exception = None

        for class_config in input_config["src_classes"]:
            try:
                #Used to detect classes imported from one module that come from another module.
                containment = class_config["class"].split('.')
                __import__(class_config["module"])
                __import__(".".join(containment[0:-1]))
                class_module = sys.modules[class_config["module"]]
                class_object = sys.modules[containment[0:-1]].__dict__[containment[-1]]

                self.source_classes += class_object
                self.module_index[class_object] = class_module
