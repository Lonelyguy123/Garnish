
from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/org/codeberg/spaciouscoder78/garnish/window.ui')
class GarnishWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GarnishWindow'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
