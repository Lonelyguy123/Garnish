
from gi.repository import Adw
from gi.repository import Gtk
from .database import DatabaseManager

@Gtk.Template(resource_path='/org/codeberg/spaciouscoder78/garnish/window.ui')
class GarnishWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GarnishWindow'

    make_newc= Gtk.Template.Child()
    menu = Gtk.Template.Child()
    delete_data = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.make_newc.connect("clicked",self.on_start_clicked)
        self.delete_data.connect("clicked",self.deletedata)
        self.load_initial_data()

    def deletedata(self,button):
        self.db.delete()

    def load_initial_data(self):
        cuisines = self.db.get_cuisines()
        for (id, cuisine) in cuisines:
            self.populate_container(cuisine,id)

    def populate_container(self, cuisine_name,cuisine_id):
        expander = Adw.ExpanderRow(
            title=cuisine_name,
            expanded=False,
        )
        expander.cid = cuisine_id

        # for every expander, we store its cuisine_id

        add_row = Adw.ActionRow(title="➕ Add Recipe")
        add_row.set_activatable(True)
        add_row.connect("activated", self.on_add_recipe_clicked, expander)

        edit_btn = Gtk.Button(icon_name="edit-symbolic")
        edit_btn.add_css_class("flat")

        expander.add_suffix(edit_btn)
        edit_btn.connect("clicked", self.on_edit_cuisine, expander)


        expander.add_row(add_row)

        self.menu.append(expander)

        #getting recipes for current cuisine_id which have been added before
        recipes = self.db.get_recipes(cuisine_id)
        for recipe_id, recipe_name in recipes:
            row = self.create_recipe_row(recipe_id, recipe_name)
            expander.add_row(row)

    def on_start_clicked(self, _button):
        cuisine_name = f"Cuisine {self.db.get_num_cuisines() + 1}"
        cid = self.db.add_to_cuisine(cuisine_name)   # return lastrowid
        self.populate_container(cuisine_name, cid)


    def on_add_recipe_clicked(self, row, expander):
        cid = expander.cid
        recipe_id = self.db.add_to_recipe("New Recipe", cid)

        new_row = self.create_recipe_row(recipe_id, "New Recipe")
        expander.add_row(new_row)


    def create_recipe_row(self, recipe_id, recipe_name):
        row = Adw.ActionRow(title=recipe_name)
        row.recipe_id = recipe_id
        row.set_activatable(True)
        row.connect("activated", self.on_recipe_clicked)

        edit_btn = Gtk.Button(icon_name="edit-symbolic")
        edit_btn.add_css_class("flat")
        row.add_suffix(edit_btn)
        edit_btn.connect("clicked", self.on_edit_recipe, row)

        return row


    def on_edit_recipe(self,_btn, new_recipe):
        entry = Gtk.Entry(text=new_recipe.get_title())

        dialog = Adw.AlertDialog(
        heading = "Edit Recipe",
        body = "Change the recipe name",
        )

        dialog.set_extra_child(entry)
        dialog.add_response("cancel","Cancel")
        dialog.add_response("save","Save")
        dialog.set_default_response("save")

        def on_response(new, response):
           if response=='save':
                new_name = entry.get_text().strip()
                if new_name:
                   new_recipe.set_title(new_name)

        dialog.connect("response",on_response)
        dialog.present(self)


    def on_recipe_clicked(self, row):
        print("Selected recipe:", row.get_title())

    def on_edit_cuisine(self, _btn, expander):
        cid = expander.cid
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
                    # updating cuisine name
                    self.db.update_cuisine(cid,new_name)

        dialog.connect("response", on_response)
        dialog.present(self)




