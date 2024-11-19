class CharTaskOperations:
    def __init__(self, db):
        self.db = db

    def assign_task_to_character(self, char_id, task_id):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO charTask (charID, taskID) VALUES (?, ?)",
            (char_id, task_id)
        )
        connection.commit()
        connection.close()
        print(f"Task {task_id} assigned to character {char_id}.")

    def get_tasks_for_character(self, char_id):
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

    def remove_task_from_character(self, char_id, task_id):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM charTask WHERE charID = ? AND taskID = ?", (char_id, task_id))
        connection.commit()
        connection.close()
        print(f"Task {task_id} removed from character {char_id}.")
