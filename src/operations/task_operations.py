import sqlite3

class Database:
    def create_connection(self):
        """
        Creates and returns a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The connection object to the SQLite database.
        """
        return sqlite3.connect("../../littleBigDatabase.db")

class TaskOperations:
    def __init__(self, db):
        """
        Initializes a new instance of the TaskOperations class.

        Args:
            db (Database): The database instance to use for database operations.
        """
        self.db = db

    def create_task(self, description, xp, expiration_date):
        """
        Creates a new task with the given description, XP, and expiration date.

        Args:
            description (str): The description of the task.
            xp (int): The XP value of the task.
            expiration_date (str): The expiration date of the task.

        Returns:
            int: The ID of the newly created task, or None if the task creation failed.
        """
        try:
            # Validate input
            if not description or xp < 0 or not expiration_date:
                print("Invalid task input: Description, XP, and expiration date are required.")
                return None

            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Create task
            cursor.execute(
                "INSERT INTO task (description, XP, expirationDate) VALUES (?, ?, ?)",
                (description, xp, expiration_date)
            )
            task_id = cursor.lastrowid
            connection.commit()
            print(f"Task '{description}' created with ID {task_id}, {xp} XP, and expiration date {expiration_date}.")
            connection.close()
            return task_id

        except sqlite3.Error as e:
            print(f"Error creating task: {e}")
            return None

    def get_task(self, task_id):
        """
        Retrieves a task from the database by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            tuple: The task details, or None if no task is found.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Call task by ID
            cursor.execute("SELECT * FROM task WHERE taskID = ?", (task_id,))
            task = cursor.fetchone()
            connection.close()

            if task:
                print(f"Task found: {task}")
                return task
            else:
                print(f"No task found with ID {task_id}.")
                return None

        except sqlite3.Error as e:
            print(f"Error retrieving task: {e}")
            return None

    def update_task(self, task_id, description=None, xp=None, expiration_date=None):
        """
        Updates the details of an existing task.

        Args:
            task_id (int): The ID of the task to update.
            description (str, optional): The new description of the task.
            xp (int, optional): The new XP value of the task.
            expiration_date (str, optional): The new expiration date of the task.

        Returns:
            bool: True if the task was updated successfully, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            updates = []
            values = []
            if description:
                updates.append("description = ?")
                values.append(description)
            if xp is not None:
                updates.append("XP = ?")
                values.append(xp)
            if expiration_date:
                updates.append("expirationDate = ?")
                values.append(expiration_date)

            if updates:
                query = f"UPDATE task SET {', '.join(updates)} WHERE taskID = ?"
                values.append(task_id)
                cursor.execute(query, values)
                connection.commit()
                print(f"Task {task_id} updated successfully.")
                connection.close()
                return True
            else:
                print("No updates were provided.")
                connection.close()
                return False

        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id):
        """
        Deletes a task from the database by its ID.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted successfully, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Delete task by ID
            cursor.execute("DELETE FROM task WHERE taskID = ?", (task_id,))
            connection.commit()
            print(f"Task {task_id} deleted successfully.")
            connection.close()
            return True

        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False