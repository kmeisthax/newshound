import gtk

class BaseWindow(object):
    def __init__(self):
        print "Starting up!"
        self.builder = gtk.Builder()
        self.builder.add_from_file("/usr/share/newshound/BaseWindow.glade")

        self.window = self.builder.get_object("BaseWindow")

        self.builder.connect_signals(self)
        self.window.show()

    def onClosed(self, widget, event, data=None):
        return False

    def onExit(self, widget, data=None):
        if widget == self.window:
            gtk.main_quit()
