import sqlite3

conn = sqlite3.connect("Garnish.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine TEXT,
    recipe_name TEXT,
    ingredients TEXT,
    process TEXT
)
""")


conn.commit()
conn.close()

