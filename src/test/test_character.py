from src.database.database import Database
from src.operations.task_operations import TaskOperations

if __name__ == "__main__":
    """
    Main script to create a task using the TaskOperations class.
    """

    # Create the database instance
    db = Database()

    # Pass the database instance to TaskOperations
    task_ops = TaskOperations(db)

    # Test: Create a task
    task_id = task_ops.create_task("Test-Task", 50, "2025-01-31")
    print(f"Created Task-ID: {task_id}")