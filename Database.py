import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (oder erstellen, wenn sie nicht existiert)
connection = sqlite3.connect('example.db')

# Cursor-Objekt erstellen, um SQL-Abfragen auszuführen
cursor = connection.cursor()

# Tabelle erstellen (falls nicht bereits vorhanden)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    race INTEGER NOT NULL
                )''')

# Änderungen speichern
connection.commit()

# Verbindung schließen
connection.close()

print("Datenbank und Tabelle wurden erfolgreich erstellt.")
