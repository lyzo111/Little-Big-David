from src.database.database import Database
from src.operations.stage_operations import StageOperations

if __name__ == "__main__":
    """
    Main script to create, retrieve, update, and delete a stage using the StageOperations class.
    """

    # Initialize the database object
    db = Database()

    # Pass the database object to StageOperations
    stage_ops = StageOperations(db)

    # Create a stage
    stage_id = stage_ops.create_stage("Naxxramas", "/assets/naxxramas.png")

    # Retrieve the stage
    if stage_id:
        stage_ops.get_stage(stage_id)

    # Update the stage
    if stage_id:
        stage_ops.update_stage(stage_id, stage_name="Icecrown Citadel", stage_path="/assets/icecrown_citadel.png")

    # Retrieve the stage again
    if stage_id:
        stage_ops.get_stage(stage_id)

    # Delete the stage
    if stage_id:
        stage_ops.delete_stage(stage_id)

    # Retrieve the deleted stage
    if stage_id:
        stage_ops.get_stage(stage_id)