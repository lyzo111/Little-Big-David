from src.database.database import init_db
import sqlite3

if __name__ == "__main__":
    init_db()

    connection = sqlite3.connect("../../littleBigDatabase.db")
    cursor = connection.cursor()

    # Rassen und Klassen einfügen
    races = [("Human",), ("Orc",), ("Elf",), ("Undead",)]
    classes = [("Mage",), ("Warrior",), ("Hunter",), ("Shaman",)]

    cursor.executemany("INSERT OR IGNORE INTO race (name) VALUES (?)", races)
    cursor.executemany("INSERT OR IGNORE INTO class (name) VALUES (?)", classes)

    connection.commit()

    print("\nInserted races and classes successfully!")
    connection.close()
