import datetime
import sqlite3


class Database:

    def __init__(self, path: str = "littleBigDatabase.db"):
        """
        Initializes the Database class with the path to the SQLite database file.

        Args:
            path (str): The path to the SQLite database file.
        """
        self.path = path

    def create_connection(self):
        """
        Creates and returns a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The connection object to the SQLite database.
        """
        return sqlite3.connect(self.path)


def init_db(db: Database):
    """
    Initializes the database by creating necessary tables if they do not exist.
    """
    # Connect to database and create if non-existing
    connection = db.create_connection()

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
                        description VARCHAR(255) NOT NULL UNIQUE,
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

    # Connect stages and tasks
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


# TODO: fix characters not being inserted into table on creation
def populate_database(db: Database):
    """
    Populates the database with initial data for classes, races, and tasks.
    """
    connection = db.create_connection()
    cursor = connection.cursor()

    # Add classes
    classes = [
        ('Warrior',),
        ('Mage',),
        ('Rogue',),
        ('Thief',),
        ('Paladin',),
        ('Ranger',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO classname (name) VALUES (?)", classes)

    # Add races
    races = [
        ('Human',),
        ('Fairy',),
        ('Dwarf',),
        ('Goblin',),
        ('Centaur',),
        ('Giant',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO race (name) VALUES (?)", races)

    # Add template tasks if table is empty
    cursor.execute("SELECT COUNT(*) FROM task")
    if cursor.fetchone()[0] == 0:
        tasks = [
            ('Workout for 30 minutes', 50, datetime.date.today().strftime("%d.%m.%Y")),
            ('Read a chapter of any book', 30, datetime.date.today().strftime("%d.%m.%Y")),
            ('Drink 2 liters of water', 20, datetime.date.today().strftime("%d.%m.%Y")),
            ('Meditate for 10 minutes', 40, datetime.date.today().strftime("%d.%m.%Y")),
            ('Create a learning protocol', 70,
             (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d.%m.%Y")),
            ('Learn a new skill', 100, (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d.%m.%Y"))
        ]
        cursor.executemany("INSERT OR IGNORE INTO task (description, XP, expirationDate) VALUES (?, ?, ?)", tasks)

    # Save changes and close connection
    connection.commit()
    connection.close()

    print("Database was populated successfully.")


db = Database()
