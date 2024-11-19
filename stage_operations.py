class StageOperations:
    def __init__(self, db):
        self.db = db

    def create_stage(self, stage_name, stage_path):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO stage (stageName, stagePath) VALUES (?, ?)",
            (stage_name, stage_path)
        )
        connection.commit()
        connection.close()
        print(f"Stage '{stage_name}' created with path '{stage_path}'.")

    def get_stage(self, stage_id):
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

    def update_stage(self, stage_id, stage_name=None, stage_path=None):
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
            update_query = f"UPDATE stage SET {', '.join(updates)} WHERE stageID = ?"
            values.append(stage_id)
            cursor.execute(update_query, values)
            connection.commit()

        connection.close()
        print(f"Stage {stage_id} updated successfully.")

    def delete_stage(self, stage_id):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM stage WHERE stageID = ?", (stage_id,))
        connection.commit()
        connection.close()
        print(f"Stage {stage_id} deleted successfully.")
