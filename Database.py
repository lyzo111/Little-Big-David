import sqlite3

# Connect to database and create if non-existing
connection = sqlite3.connect('littleBigDatabase.db')

# Create cursor object for SQL commands
cursor = connection.cursor()

# Create tables if non-existing
cursor.execute('''CREATE TABLE IF NOT EXISTS char (
                    charID INT PRIMARY KEY AUTOINCREMENT ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    race TEXT NOT NULL,
                    roll TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS statTable (
                    charID INT FOREIGN KEY (charID) ON DELETE CASCADE,
                    level INT NOT NULL DEFAULT 10,
                    charisma INT NOT NULL DEFAULT 10,
                    crafting INT NOT NULL DEFAULT 10,
                    health INT NOT NULL DEFAULT 10,
                    strength INT NOT NULL DEFAULT 10,
                    defense INT NOT NULL DEFAULT 10,
                    intelligence INT NOT NULL DEFAULT 10,
                    luck INT NOT NULL DEFAULT 10,
                    CONSTRAINT fk_charID FOREIGN KEY (charID) REFERENCES char(charID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS task (
                    taskID INT PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    XP INT NOT NULL,
                    date DATE NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS charTask (
                    charID INT,
                    taskID INT,
                    PRIMARY KEY (charID, taskID),
                    CONSTRAINT fk_char FOREIGN KEY (charID) REFERENCES char(charID) ON DELETE CASCADE,
                    CONSTRAINT fk_task FOREIGN KEY (taskID) REFERENCES task(taskID) ON DELTETE CASCADE
)''')

# Save changes and close connection
connection.commit()
connection.close()

print("Database and tables are set.")
