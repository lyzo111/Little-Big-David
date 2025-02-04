import sqlite3

def init_db():
    """
    Initializes the database by creating necessary tables if they do not exist.
    """
    # Connect to database and create if non-existing
    connection = sqlite3.connect('../../littleBigDatabase.db')

    # Create cursor object for SQL commands
    cursor = connection.cursor()

    # Create tables if non-existing
    cursor.execute('''CREATE TABLE IF NOT EXISTS char (
                        charID INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_image TEXT NOT NULL,
                        name VARCHAR(50) NOT NULL,
                        race VARCHAR(20) NOT NULL,
                        classname VARCHAR(20) NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS charStat (
                        charID INTEGER,
                        level INT NOT NULL DEFAULT 1,
                        xp INT NOT NULL DEFAULT 0, 
                        charisma INT NOT NULL DEFAULT 10,
                        crafting INT NOT NULL DEFAULT 10,
                        health INT NOT NULL DEFAULT 10,
                        strength INT NOT NULL DEFAULT 10,
                        defense INT NOT NULL DEFAULT 10,
                        intelligence INT NOT NULL DEFAULT 10,
                        luck INT NOT NULL DEFAULT 10,
                        CONSTRAINT fk_charID FOREIGN KEY (charID) REFERENCES char(charID) ON DELETE CASCADE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS task (
                        taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                        description VARCHAR(255) NOT NULL,
                        XP INT NOT NULL,
                        expirationDate DATE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS charTask (
                        charID INTEGER,
                        taskID INTEGER,
                        PRIMARY KEY (charID, taskID),
                        CONSTRAINT fk_char FOREIGN KEY (charID) REFERENCES char(charID) ON DELETE CASCADE,
                        CONSTRAINT fk_task FOREIGN KEY (taskID) REFERENCES task(taskID) ON DELETE CASCADE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS stage (
                        stageID INTEGER PRIMARY KEY AUTOINCREMENT,
                        stageName VARCHAR(50) NOT NULL,
                        stagePath VARCHAR(255) NOT NULL -- stagePath -> file path to assets of said stage
    )''')

    # Verknüpfung Stages und Aufgaben
    cursor.execute('''CREATE TABLE IF NOT EXISTS stageTask (
                          stageID INTEGER,
                          taskID INTEGER,
                          PRIMARY KEY (stageID, taskID),
                          FOREIGN KEY (stageID) REFERENCES stage(stageID) ON DELETE CASCADE,
                          FOREIGN KEY (taskID) REFERENCES task(taskID) ON DELETE CASCADE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS classname (
                          classID INTEGER PRIMARY KEY AUTOINCREMENT,
                          name VARCHAR(50) NOT NULL UNIQUE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS race (
                          raceID INTEGER PRIMARY KEY AUTOINCREMENT,
                          name VARCHAR(50) NOT NULL UNIQUE
    )''')

    # Save changes and close connection
    connection.commit()
    connection.close()

def populate_database():
    """
    Populates the database with initial data for classes, races, and tasks.
    """
    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect('../../littleBigDatabase.db')
    cursor = connection.cursor()

    # Klassen hinzufügen
    classes = [
        ('Warrior',),
        ('Mage',),
        ('Rogue',),
        ('Bard',),
        ('Paladin',),
        ('Ranger',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO classname (name) VALUES (?)", classes)

    # Rassen hinzufügen
    races = [
        ('Human',),
        ('Elf',),
        ('Dwarf',),
        ('Orc',),
        ('Tiefling',),
        ('Halfling',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO race (name) VALUES (?)", races)

    # Beispiel-Tasks hinzufügen
    tasks = [
        ('Trainiere für 30 Minuten', 50, '2025-01-20'),
        ('Lies ein Buchkapitel', 30, '2025-01-21'),
        ('Trinke 2 Liter Wasser', 20, '2025-01-20'),
        ('Mache 10 Minuten Meditation', 40, '2025-01-22'),
        ('Erstelle ein Lernprotokoll', 70, '2025-01-23'),
        ('Lerne eine neue Fähigkeit', 100, '2025-01-25')
    ]
    cursor.executemany("INSERT OR IGNORE INTO task (description, XP, expirationDate) VALUES (?, ?, ?)", tasks)

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()

    print("Datenbanken wurden erfolgreich befüllt.")

class Database:
    def create_connection(self):
        """
        Creates and returns a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The connection object to the SQLite database.
        """
        return sqlite3.connect("../../littleBigDatabase.db")

if __name__ == "__main__":
    init_db()
    populate_database()