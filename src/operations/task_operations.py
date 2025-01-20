import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../littleBigDatabase.db")

class TaskOperations:
    def __init__(self, db):
        self.db = db

    def create_task(self, description, xp, expiration_date):
        try:
            # Eingabevalidierung
            if not description or xp < 0 or not expiration_date:
                print("Invalid task input: Description, XP, and expiration date are required.")
                return None

            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Aufgabe erstellen
            cursor.execute(
                "INSERT INTO task (description, XP, expirationDate) VALUES (?, ?, ?)",
                (description, xp, expiration_date)
            )
            task_id = cursor.lastrowid
            connection.commit()
            print(f"Task '{description}' created with ID {task_id}, {xp} XP, and expiration date {expiration_date}.")
            return task_id

        except sqlite3.Error as e:
            print(f"Error creating task: {e}")
            return None

        finally:
            connection.close()

    def get_task(self, task_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Aufgabe abrufen
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
                return True
            else:
                print("No updates were provided.")
                return False

        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False

        finally:
            connection.close()

    def delete_task(self, task_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Aufgabe löschen
            cursor.execute("DELETE FROM task WHERE taskID = ?", (task_id,))
            connection.commit()
            print(f"Task {task_id} deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False

        finally:
            connection.close()
