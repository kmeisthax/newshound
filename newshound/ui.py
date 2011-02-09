import gtk

class BaseWindow(object):
    MENU_ITEM_QUIT = "Quit"

    def __init__(self):
        print "Starting up!"
        self.builder = gtk.Builder()
        self.builder.add_from_file("/usr/share/newshound/BaseWindow.glade")

        self.window_main = self.builder.get_object("BaseWindow")
        self.sourcestree = self.builder.get_object("NewsSourceTreeModel")

        self.sourcestree.append(None, ["Home"])
        self.sourcestree.append(None, ["Search"])

        self.builder.connect_signals(self)
        self.window.show()
        
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
                
        if windowCanClose(window):
            window.destroy()

    def onDestroyWindow(self, widget, *data_args):
        """Called when a toplevel window is destroyed."""
        if widget == self.window_main:
            gtk.main_quit()

    def onChangeSource(self, treeview, *data_args):
        print treeview.get_cursor()
