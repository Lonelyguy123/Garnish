
from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/org/codeberg/spaciouscoder78/garnish/window.ui')
class GarnishWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GarnishWindow'

    make_newc= Gtk.Template.Child()
    menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_newc.connect("clicked",self.on_start_clicked)

    def populate_container(self,label):
        item = Adw.Bin(
            margin_top=6,
            margin_bottom=6,
            margin_start=6,
            margin_end=6,
            child=Gtk.Label(
                label=label,
                width_request=1,
                height_request=1,
            ),
            css_classes=["card"],
        )
        self.menu.append(item)

    def on_start_clicked(self, _button):
        self.populate_container("FirstCuisine")


