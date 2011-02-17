import gtk, cairo
from newshound import datasrc

class BaseWindow(object):
    MENU_ITEM_QUIT = "Quit"

    def __init__(self, core):
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

    def onDrawBackground(self, widget, event, *data_args):
        win = widget.window
        Xr = win.cairo_create()
        
        fillall = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
        Xr.set_source(fillall)
        Xr.paint()
        
        rect = win.get_frame_extents()
        grad = cairo.LinearGradient(0, 0, 0, 250)
        
        grad.add_color_stop_rgba(0.0, 0.70, 0.70, 1.0, 1.0)
        grad.add_color_stop_rgba(1.0, 0.70, 0.70, 1.0, 0.0)
        
        Xr.set_source(grad)
        
        Xr.move_to(0, 0)
        Xr.line_to(rect.width, 0)
        Xr.line_to(rect.width, rect.height)
        Xr.line_to(0, rect.height)
        Xr.line_to(0, 0)
        
        Xr.fill()
        return False

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
