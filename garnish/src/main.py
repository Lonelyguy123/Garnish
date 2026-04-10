
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk
from .window import GarnishWindow

class GarnishApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.codeberg.spaciouscoder78.garnish',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/org/codeberg/spaciouscoder78/garnish')
        self.create_action('quit', lambda *_: self.quit(), ['<control>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = GarnishWindow(application=self)
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='garnish',
                                application_icon='org.codeberg.spaciouscoder78.garnish',
                                developer_name='Lonelyguy123 & spaciouskarter78',
                                version='0.1.0',
                                developers=['Lonelyguy123','spaciouskarter78'],
                                copyright='© 2026 Lonelyguy123 & spaciouskarter78')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def load_css():
    provider = Gtk.CssProvider()
    provider.load_from_path("style.css")

    Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(),
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)



def main(version):
    load_css()
    """The application's entry point."""
    app = GarnishApplication()
    return app.run(sys.argv)
