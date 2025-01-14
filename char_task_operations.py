import sqlite3

class CharTaskOperations:
    def __init__(self, db_path="littleBigDatabase.db"):
        self.db_path = db_path

    def assign_task_to_character(self, char_id, task_id):
        try:
            connection = sqlite3.connect(self.db_path)
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

