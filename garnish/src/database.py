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

    # --- Cuisine Methods ---
    def add_cuisine(self, name):
        try:
            self.cursor.execute('INSERT INTO Cuisines (name) VALUES (?)', (name,))
            self.conn.commit()
            return self.cursor.lastrowid # Return the ID of the new cuisine
        except sqlite3.IntegrityError:
            return None # Cuisine already exists

    def get_all_cuisines(self):
        self.cursor.execute('SELECT id, name FROM Cuisines')
        return self.cursor.fetchall()
    
    def update_cuisine_name(self, old_name, new_name):
        self.cursor.execute('UPDATE Cuisines SET name = ? WHERE name = ?', (new_name, old_name))
        self.conn.commit()

    # --- Recipe Methods ---
    def add_recipe(self, cuisine_id, name):
        self.cursor.execute('''
            INSERT INTO Recipes (cuisine_id, name, ingredients, process, tips)
            VALUES (?, ?, ?, ?, ?)
        ''', (cuisine_id, name, "", "", "")) # Initialize empty fields
        self.conn.commit()
        return self.cursor.lastrowid

    def update_recipe_name(self, recipe_id, new_name):
        self.cursor.execute('UPDATE Recipes SET name = ? WHERE id = ?', (new_name, recipe_id))
        self.conn.commit()

    def get_recipes_by_cuisine(self, cuisine_id):
        self.cursor.execute('SELECT id, name FROM Recipes WHERE cuisine_id = ?', (cuisine_id,))
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
