import sqlite3

class CharTaskOperations:
    def __init__(self, db):
        """
        Initializes a new instance of the CharTaskOperations class.

        Args:
            db (Database): The database instance to use for database operations.
        """
        self.db = db

    def assign_task_to_character(self, char_id, task_id):
        """
        Assigns a task to a character.

        This function checks if the character and task exist, and then assigns the task to the character.

        Args:
            char_id (int): The ID of the character.
            task_id (int): The ID of the task.

        Returns:
            bool: True if the task was successfully assigned, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM char WHERE charID = ?", (char_id,))
            character = cursor.fetchone()
            if not character:
                print(f"Character with ID {char_id} does not exist.")
                return False

            cursor.execute("SELECT * FROM task WHERE taskID = ?", (task_id,))
            task = cursor.fetchone()
            if not task:
                print(f"Task with ID {task_id} does not exist.")
                return False

            cursor.execute(
                "INSERT INTO charTask (charID, taskID) VALUES (?, ?)",
                (char_id, task_id)
            )
            connection.commit()
            print(f"Task {task_id} successfully assigned to character {char_id}.")
            return True

        except sqlite3.IntegrityError:
            print(f"Task {task_id} is already assigned to character {char_id}.")
            return False

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()

    def get_tasks_for_character(self, char_id):
        """
        Retrieves tasks assigned to a character.

        This function fetches all tasks assigned to the specified character.

        Args:
            char_id (int): The ID of the character.

        Returns:
            list: A list of tasks assigned to the character.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT t.taskID, t.description, t.XP, t.expirationDate 
                FROM charTask ct
                JOIN task t ON ct.taskID = t.taskID
                WHERE ct.charID = ?
            """, (char_id,))
            tasks = cursor.fetchall()
            connection.close()

            if tasks:
                print(f"Tasks for character {char_id}: {tasks}")
                return tasks
            else:
                print(f"No tasks found for character {char_id}.")
                return []

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def mark_task_as_completed(self, char_id, task_id):
        """
        Marks a task as completed for a character.

        This function removes the task assignment from the character.

        Args:
            char_id (int): The ID of the character.
            task_id (int): The ID of the task.

        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM charTask WHERE charID = ? AND taskID = ?",
                (char_id, task_id)
            )
            assignment = cursor.fetchone()
            if not assignment:
                print(f"Task {task_id} is not assigned to character {char_id}.")
                return False

            cursor.execute(
                "DELETE FROM charTask WHERE charID = ? AND taskID = ?",
                (char_id, task_id)
            )
            connection.commit()
            print(f"Task {task_id} marked as completed for character {char_id}.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()