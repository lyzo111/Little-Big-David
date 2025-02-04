import sqlite3
from datetime import datetime

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
        """
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO task (description, XP, expirationDate) VALUES (?, ?, ?)",
            (description, xp, expiration_date)
        )
        connection.commit()
        connection.close()
        print(f"Task '{description}' created with {xp} XP and expiration date {expiration_date}.")

    def get_task(self, task_id):
        """
        Retrieves a task from the database by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            tuple: The task details, or None if no task is found.
        """
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM task WHERE taskID = ?", (task_id,))
        task = cursor.fetchone()
        connection.close()

        if task:
            print(f"Task found: {task}")
            return task
        else:
            print(f"No task found with ID {task_id}.")
            return None

    def update_task(self, task_id, description=None, xp=None, expiration_date=None):
        """
        Updates the details of an existing task.

        Args:
            task_id (int): The ID of the task to update.
            description (str, optional): The new description of the task.
            xp (int, optional): The new XP value of the task.
            expiration_date (str, optional): The new expiration date of the task.
        """
        connection = self.db.create_connection()
        cursor = connection.cursor()

        updates = []
        values = []
        if description:
            updates.append("description = ?")
            values.append(description)
        if xp:
            updates.append("XP = ?")
            values.append(xp)
        if expiration_date:
            updates.append("expirationDate = ?")
            values.append(expiration_date)

        if updates:
            update_query = f"UPDATE task SET {', '.join(updates)} WHERE taskID = ?"
            values.append(task_id)
            cursor.execute(update_query, values)
            connection.commit()

        connection.close()
        print(f"Task {task_id} updated successfully.")

    def delete_task(self, task_id):
        """
        Deletes a task from the database by its ID.

        Args:
            task_id (int): The ID of the task to delete.
        """
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM task WHERE taskID = ?", (task_id,))
        connection.commit()
        connection.close()
        print(f"Task {task_id} deleted successfully.")