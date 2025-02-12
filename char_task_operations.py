import sqlite3

class CharTaskOperations:
    def __init__(self, db_path="littleBigDatabase.db"):
        """
        Initialize the CharTaskOperations class with the path to the database.

        Args:
            db_path (str): Path to the SQLite database file. Defaults to "littleBigDatabase.db".
        """
        self.db_path = db_path

    def assign_task_to_character(self, char_id, task_id):
        """
        Assign a task to a character by inserting a record into the charTask table.

        Args:
            char_id (int): The ID of the character.
            task_id (int): The ID of the task.

        Returns:
            bool: True if the task was successfully assigned, False otherwise.
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Check if the character exists
            cursor.execute("SELECT * FROM char WHERE charID = ?", (char_id,))
            character = cursor.fetchone()
            if not character:
                print(f"Character with ID {char_id} does not exist.")
                return False

            # Check if the task exists
            cursor.execute("SELECT * FROM task WHERE taskID = ?", (task_id,))
            task = cursor.fetchone()
            if not task:
                print(f"Task with ID {task_id} does not exist.")
                return False

            # Assign the task to the character
            cursor.execute(
                "INSERT INTO charTask (charID, taskID) VALUES (?, ?)",
                (char_id, task_id)
            )
            connection.commit()
            print(f"Task {task_id} successfully assigned to character {char_id}.")
            connection.close()
            return True

        except sqlite3.IntegrityError:
            print(f"Task {task_id} is already assigned to character {char_id}.")
            return False

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
