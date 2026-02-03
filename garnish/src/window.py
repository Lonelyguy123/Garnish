
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

    def populate_container(self, cuisine_name):
        expander = Adw.ExpanderRow(
            title=cuisine_name,
            expanded=False,
        )

        add_row = Adw.ActionRow(title="➕ Add Recipe")
        add_row.set_activatable(True)
        add_row.connect("activated", self.on_add_recipe_clicked, expander)

        edit_btn = Gtk.Button(icon_name="edit-symbolic")
        edit_btn.add_css_class("flat")

        expander.add_suffix(edit_btn)
        edit_btn.connect("clicked", self.on_edit_cuisine, expander)


        expander.add_row(add_row)

        self.menu.append(expander)

    def on_start_clicked(self, _button):
        self.populate_container("FirstCuisine")

    def on_add_recipe_clicked(self, row, expander):
        new_recipe = Adw.ActionRow(title="New Recipe")
        new_recipe.set_activatable(True)
        new_recipe.connect("activated", self.on_recipe_clicked)

        expander.add_row(new_recipe)


    def on_recipe_clicked(self, row):
        print("Selected recipe:", row.get_title())

    def on_edit_cuisine(self, _btn, expander):
        entry = Gtk.Entry(text=expander.get_title())

        dialog = Adw.AlertDialog(
            heading="Edit Cuisine",
            body="Change the cuisine name",
        )

        dialog.set_extra_child(entry)
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("save", "Save")
        dialog.set_default_response("save")

        def on_response(dlg, response):
            if response == "save":
                new_name = entry.get_text().strip()
                if new_name:
                    expander.set_title(new_name)
                    # TODO: update DB here

        dialog.connect("response", on_response)
        dialog.present(self)




