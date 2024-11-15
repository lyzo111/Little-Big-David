import sqlite3

# Connect to database and create if non-existing
connection = sqlite3.connect('littleBigDatabase.db')

# Create cursor object for SQL commands
cursor = connection.cursor()

# Create tables if non-existing
cursor.execute('''CREATE TABLE IF NOT EXISTS char (
                    charID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    race VARCHAR(20) NOT NULL,
                    roll VARCHAR(20) NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS charStat (
                    charID INTEGER,
                    level INT NOT NULL DEFAULT 1,
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

# stagePath -> file path to assets of said stage
cursor.execute('''CREATE TABLE IF NOT EXISTS stage (
                    stageID INTEGER PRIMARY KEY AUTOINCREMENT,
                    stageName VARCHAR(50) NOT NULL,
                    stagePath VARCHAR(255) NOT NULL
)''')

# Save changes and close connection
connection.commit()
connection.close()

print("Database and tables are set.")
