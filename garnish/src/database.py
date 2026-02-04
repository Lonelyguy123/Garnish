import sqlite3

class DatabaseManager:
    def __init__(self, db_name='recipes.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Table for Cuisines (e.g., Italian, Mexican)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cuisines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Table for Recipes, linked to a Cuisine ID
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuisine_id INTEGER,
                name TEXT NOT NULL,
                ingredients TEXT,
                process TEXT,
                tips TEXT,
                FOREIGN KEY(cuisine_id) REFERENCES Cuisines(id)
            )
        ''')
        self.conn.commit()

    def delete(self):
         # removing all data using DELETE(Truncate is not supported in sqlite)
         self.cursor.execute("DELETE FROM Cuisines")
         self.cursor.execute("DELETE FROM Recipes")

         self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='Recipes'")
         self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='Cuisines'")

         #Removes the autoincremented ID's'

         self.conn.commit()

    def get_num_cuisines(self):
         #counting number of unique cuisines
         self.cursor.execute("SELECT COALESCE(MAX(id), 0) FROM Cuisines")
         #Coalesce makes sure we return 0 when no id's are there

         result = self.cursor.fetchone()

         return result[0]
    def get_num_recipes(self,cid):
        self.cursor.execute("SELECT MAX(id) FROM Recipes WHERE cuisine_id = ?",(cid,))

        result = self.cursor.fetchone()

        return result[0]

    def add_to_recipe(self,recipe_name,cid):
        self.cursor.execute("INSERT INTO Recipes (cuisine_id,name,ingredients,process,tips) VALUES (?,?,?,?,?)",(cid,recipe_name,"","",""))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_to_cuisine(self,name):
         self.cursor.execute(
         "INSERT INTO Cuisines (name) VALUES (?)",
         (name,))
         self.conn.commit()
         return self.cursor.lastrowid

    def get_cuisines(self):
         self.cursor.execute("SELECT * FROM Cuisines ORDER BY id")
         return self.cursor.fetchall()

    def get_recipes(self,cid):
         self.cursor.execute("SELECT id,name FROM Recipes WHERE cuisine_id = ? ORDER BY id",(cid,))
         return self.cursor.fetchall()

    def update_cuisine(self,cid,new_name):
         self.cursor.execute("UPDATE Cuisines SET name = ? WHERE id = ?",(new_name,cid))
         self.conn.commit()

    def update_recipe(self,recipe_id,cid,new_name):
         self.cursor.execute("UPDATE Recipes SET name = ? WHERE id = ? AND cuisine_id = ?",(new_name,recipe_id,cid))
         self.conn.commit()

