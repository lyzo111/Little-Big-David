from src.database.database import init_db
import sqlite3

if __name__ == "__main__":
    """
    Main script to initialize the database and insert predefined races and classes.
    """

    # Initialize the database
    init_db()

    # Connect to the SQLite database
    connection = sqlite3.connect("../../littleBigDatabase.db")
    cursor = connection.cursor()

    # Insert races and classes
    races = [("Human",), ("Orc",), ("Elf",), ("Undead",)]
    classes = [("Mage",), ("Warrior",), ("Hunter",), ("Shaman",)]

    # Insert races into the race table if they do not already exist
    cursor.executemany("INSERT OR IGNORE INTO race (name) VALUES (?)", races)
    # Insert classes into the classname table if they do not already exist
    cursor.executemany("INSERT OR IGNORE INTO classname (name) VALUES (?)", classes)

    # Commit the changes to the database
    connection.commit()

    print("\nInserted races and classes successfully!")
    # Close the database connection
    connection.close()