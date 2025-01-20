import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../littleBigDatabase.db")

class StageOperations:
    def __init__(self, db):
        self.db = db

    def create_stage(self, stage_name, stage_path):
        try:
            if not stage_name or not stage_path:
                print("Stage name and path cannot be empty.")
                return None

            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO stage (stageName, stagePath) VALUES (?, ?)",
                (stage_name, stage_path)
            )
            stage_id = cursor.lastrowid
            connection.commit()
            print(f"Stage '{stage_name}' created with ID {stage_id} and path '{stage_path}'.")
            return stage_id

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            if 'connection' in locals():
                connection.close()

    def get_stage(self, stage_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM stage WHERE stageID = ?", (stage_id,))
            stage = cursor.fetchone()
            connection.close()

            if stage:
                print(f"Stage found: {stage}")
                return stage
            else:
                print(f"No stage found with ID {stage_id}.")
                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def update_stage(self, stage_id, stage_name=None, stage_path=None):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            updates = []
            values = []
            if stage_name:
                updates.append("stageName = ?")
                values.append(stage_name)
            if stage_path:
                updates.append("stagePath = ?")
                values.append(stage_path)

            if updates:
                query = f"UPDATE stage SET {', '.join(updates)} WHERE stageID = ?"
                values.append(stage_id)
                cursor.execute(query, values)
                connection.commit()
                print(f"Stage {stage_id} updated successfully.")
                return True
            else:
                print("No updates were provided.")
                return False

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            if 'connection' in locals():
                connection.close()

    def delete_stage(self, stage_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM stage WHERE stageID = ?", (stage_id,))
            connection.commit()
            print(f"Stage {stage_id} deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            if 'connection' in locals():
                connection.close()
