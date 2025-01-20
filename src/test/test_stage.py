from src.database.database import Database
from src.operations.stage_operations import StageOperations

if __name__ == "__main__":
    db = Database()
    stage_ops = StageOperations(db)

    # Stage erstellen
    stage_id = stage_ops.create_stage("Naxxramas", "/assets/naxxramas.png")

    # Stage abrufen
    if stage_id:
        stage_ops.get_stage(stage_id)

    # Stage aktualisieren
    if stage_id:
        stage_ops.update_stage(stage_id, stage_name="Icecrown Citadel", stage_path="/assets/icecrown_citadel.png")

    # Stage erneut abrufen
    if stage_id:
        stage_ops.get_stage(stage_id)

    # Stage löschen
    if stage_id:
        stage_ops.delete_stage(stage_id)

    # Gelöschte Stage abrufen
    if stage_id:
        stage_ops.get_stage(stage_id)
