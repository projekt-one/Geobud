import sqlite3

DB_FILE = "projekty.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projekty (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazwa TEXT,
                        lokalizacja TEXT,
                        projekt_link TEXT,
                        obrazek TEXT
                    )''')
    conn.commit()
    conn.close()
    print("Baza danych została zainicjalizowana!")

if __name__ == "__main__":
    init_db()
