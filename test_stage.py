from stage_operations import StageOperations

if __name__ == "__main__":
    stage_ops = StageOperations()

    # Stage erstellen
    stage_id = stage_ops.create_stage("Frostmourne Cavern", "/assets/frostmourne_cavern.png")

    # Stage abrufen
    stage_ops.get_stage(stage_id)

    # Stage aktualisieren
    stage_ops.update_stage(stage_id, stage_name="Icecrown Citadel", stage_path="/assets/icecrown_citadel.png")

    # Stage erneut abrufen
    stage_ops.get_stage(stage_id)

    # Stage löschen
    stage_ops.delete_stage(stage_id)

    # Gelöschte Stage abrufen
    stage_ops.get_stage(stage_id)
