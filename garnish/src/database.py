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

    def get_num_recipes(self):
         #counting number of unique recipes
         self.cursor.execute("SELECT MAX(id) FROM Cuisines")

         result = self.cursor.fetchone()

         return result[0]
    def add_to_cuisine(self,name):
         self.cursor.execute(
         "INSERT INTO Cuisines (name) VALUES (?)",
         (name,))
         self.conn.commit()

    def get_cuisines(self):
         self.cursor.execute("SELECT * FROM Cuisines ORDER BY id")
         return self.cursor.fetchall()

    def update_cuisine(self,cid,new_name):
         self.cursor.execute("UPDATE Cuisines SET name = ? WHERE id = ?",(new_name,cid))
         self.conn.commit()

