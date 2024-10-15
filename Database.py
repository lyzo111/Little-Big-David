import sqlite3

# Connect to database and create if non-existing
connection = sqlite3.connect('littleBigDatabase.db')

# Create cursor object for SQL commands
cursor = connection.cursor()

# Create tables if non-existing
cursor.execute('''CREATE TABLE IF NOT EXISTS chars (
                    charID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    race TEXT NOT NULL,
                    roll TEXT NOT NULL,
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS charStats (
                    charID INTEGER FOREIGN KEY (charID) REFERENCES chars (charID) ON DELETE CASCADE,
                    level INTEGER NOT NULL DEFAULT 1,
                    charisma INTEGER  NOT NULL DEFAULT 1,
                    crafting INTEGER  NOT NULL DEFAULT 1,
                    health INTEGER  NOT NULL DEFAULT 1,
                    strength INTEGER  NOT NULL DEFAULT 1,
                    defense INTEGER  NOT NULL DEFAULT 1,
                    intelligence INTEGER  NOT NULL DEFAULT 1,
                    luck INTEGER  NOT NULL DEFAULT 1,
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    XP INTEGER NOT NULL,
                    date DATE NOT NULL,
)''')

# Save changes and close connection
connection.commit()
connection.close()

print("Database and tables are set.")
