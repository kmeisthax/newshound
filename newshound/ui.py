import gtk
from newshound import datasrc

class BaseWindow(object):
    MENU_ITEM_QUIT = "Quit"

    def __init__(self, core):
        print "Starting up!"
        self.core = core
        
        self.builder = gtk.Builder()
        self.builder.add_from_file("/usr/share/newshound/BaseWindow.glade")

        self.window = self.builder.get_object("BaseWindow")
        self.sourcestree = self.builder.get_object("NewsSourceTreeModel")
        self.build_tree()

        self.builder.connect_signals(self)
        self.window.show()
        
        self.sources = datasrc.SourceManager()
        
    def windowCanClose(self, window):
        return True

    def onCloseWindow(self, widget, event, *data_args):
        """Called when the user closes the window."""
        return not self.windowCanClose(widget)

    def onMenuQuit(self, widget, *data_args):
        """Called to handle the Quit menu item."""
        window = widget
        
        while True:
            newwindow = window.get_parent()
            if newwindow is None:
                break
            else:
                window = newwindow
                
        if self.windowCanClose(window):
            window.destroy()

    def onDestroyWindow(self, widget, *data_args):
        """Called when a toplevel window is destroyed."""
        if widget == self.window:
            gtk.main_quit()

    def onChangeSource(self, treeview, *data_args):
        print treeview.get_cursor()
        
    def build_tree(self):
        self.sourcestree.clear()
        
        #default options
        self.sourcestree.append(None, ["Home"])
        self.sourcestree.append(None, ["Search"])
        
        def recurse(treeiter, childArray):
            for source in childArray:
                newiter = self.sourcestree.append(treeiter, [source["object"].source_name])
                recurse(newiter, source["children"])
                
        recurse(None, self.core.src.create_source_tree())
