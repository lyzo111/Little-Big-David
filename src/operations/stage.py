import sqlite3
from datetime import datetime

class TaskOperations:
    def __init__(self, db):
        self.db = db

    def create_task(self, description, xp, expiration_date):
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
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM task WHERE taskID = ?", (task_id,))
        connection.commit()
        connection.close()
        print(f"Task {task_id} deleted successfully.")
