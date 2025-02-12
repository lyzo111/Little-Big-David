from src.database.database import db
from src.operations.task_operations import TaskOperations

if __name__ == "__main__":
    """
    Main script to create, retrieve, update, and delete a task using the TaskOperations class.
    """

    # Pass the database object to TaskOperations
    task_ops = TaskOperations(db)

    # Create a task
    task_id = task_ops.create_task("Defeat the Lich King", 50, "2025-01-31")

    # Retrieve the task
    task_ops.get_task(task_id)

    # Update the task
    task_ops.update_task(task_id, description="Defeat Arthas", xp=75, expiration_date="2025-02-15")

    # Retrieve the task again
    task_ops.get_task(task_id)

    # Delete the task
    task_ops.delete_task(task_id)

    # Retrieve the deleted task
    task_ops.get_task(task_id)