import sqlite3

conn = sqlite3.connect("flight.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    city TEXT PRIMARY KEY,
    price TEXT
)
""")

cities = [
    ("london", "$799"),
    ("paris", "$899"),
    ("tokyo", "$1400"),
    ("berlin", "$499")
]

cursor.executemany(
    "INSERT OR REPLACE INTO tickets VALUES (?, ?)",
    cities
)

conn.commit()
conn.close()

print("Database created!")