import sqlite3

# Connect to database and create if non-existing
connection = sqlite3.connect('littleBigDatabase.db')

# Create cursor object for SQL commands
cursor = connection.cursor()

# Create tables if non-existing
cursor.execute('''CREATE TABLE IF NOT EXISTS chars (
                    charID INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    race INTEGER NOT NULL,
                    statsID INTEGER FOREIGN KEY (statsID) REFERENCES userStats (statsID),
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS charStats (
                    statsID INTEGER PRIMARY KEY,
                    level INTEGER NOT NULL,
                    charisma INTEGER  NOT NULL,
                    crafting INTEGER  NOT NULL,
                    health INTEGER  NOT NULL,
                    strength INTEGER  NOT NULL,
                    defense INTEGER  NOT NULL,
                    intelligence INTEGER  NOT NULL,
                    luck INTEGER  NOT NULL,
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    taskID INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    XP INTEGER NOT NULL,
                    date DATE NOT NULL,
)''')

# Save changes and close connection
connection.commit()
connection.close()

print("Database and tables are set.")
