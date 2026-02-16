
from gi.repository import Adw
from gi.repository import Gtk
from .database import DatabaseManager

@Gtk.Template(resource_path='/org/codeberg/spaciouscoder78/garnish/window.ui')
class GarnishWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GarnishWindow'

    make_newc= Gtk.Template.Child()
    menu = Gtk.Template.Child()
    delete_data = Gtk.Template.Child()
    ingredients_view = Gtk.Template.Child()
    process_view = Gtk.Template.Child()
    tips_view = Gtk.Template.Child()
    recipe = Gtk.Template.Child()

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
            row = self.create_recipe_row(recipe_id, recipe_name, cuisine_id)
            expander.add_row(row)

    def on_start_clicked(self, _button):
        cuisine_name = f"Cuisine {self.db.get_num_cuisines() + 1}"
        cid = self.db.add_to_cuisine(cuisine_name)   # return lastrowid
        self.populate_container(cuisine_name, cid)


    def on_add_recipe_clicked(self, row, expander):
        cid = expander.cid
        recipe_id = self.db.add_to_recipe("New Recipe", cid)

        new_row = self.create_recipe_row(recipe_id, "New Recipe",cid)
        expander.add_row(new_row)


    def create_recipe_row(self, recipe_id, recipe_name,cid):
        row = Adw.ActionRow(title=recipe_name)
        '''
        We can attach arbitary arguments like cid and recipe_id to row and pass the row object as one
        '''
        row.cid = cid
        row.recipe_id = recipe_id
        row.set_activatable(True)
        row.connect("activated", self.on_recipe_clicked)

        edit_info_btn = Gtk.Button(icon_name="document-edit-symbolic")
        edit_info_btn.add_css_class("flat")
        row.add_suffix(edit_info_btn)
        edit_info_btn.connect("clicked",self.on_save_info, row)

        edit_btn = Gtk.Button(icon_name="edit-symbolic")
        edit_btn.add_css_class("flat")
        row.add_suffix(edit_btn)
        edit_btn.connect("clicked", self.on_edit_recipe, row)

        return row


    def on_edit_recipe(self,_btn, row):
        entry = Gtk.Entry(text=row.get_title())

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
                   row.set_title(new_name)
                   self.db.update_recipe(row.recipe_id,row.cid,new_name)
                   self.recipe.set_text(new_name)

        dialog.connect("response",on_response)
        dialog.present(self)

    def on_save_info(self,_btn, row):
        dialog = Adw.AlertDialog(
        heading = "Save",
        body = "Save recipe info",
        )

        dialog.add_response("cancel","Cancel")
        dialog.add_response("save","Save")
        dialog.set_default_response("save")

        def on_response(new, response):
            if response=='save':
                inbuffer = self.ingredients_view.get_buffer()
                start_iter = inbuffer.get_start_iter()
                end_iter = inbuffer.get_end_iter()
                intext = inbuffer.get_text(start_iter, end_iter, True)

                probuffer = self.process_view.get_buffer()
                start_iter = probuffer.get_start_iter()
                end_iter = probuffer.get_end_iter()
                protext = probuffer.get_text(start_iter, end_iter, True)

                tipbuffer = self.tips_view.get_buffer()
                start_iter = tipbuffer.get_start_iter()
                end_iter = tipbuffer.get_end_iter()
                tiptext = tipbuffer.get_text(start_iter, end_iter, True)

                self.db.update_info(row.cid,row.recipe_id,intext,protext,tiptext)
        dialog.connect("response",on_response)
        dialog.present(self)



    def on_recipe_clicked(self, row):
         data = self.db.get_info(row.recipe_id,row.cid)
         ingredients = data[0]
         process = data[1]
         tips = data[2]
         recipe_name = data[3]
         inbuffer = self.ingredients_view.get_buffer()
         probuffer = self.process_view.get_buffer()
         tipbuffer = self.tips_view.get_buffer()
         inbuffer.set_text(ingredients)
         probuffer.set_text(process)
         tipbuffer.set_text(tips)
         self.recipe.set_text(recipe_name)

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




