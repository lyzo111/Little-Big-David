from src.operations.char_task_operations import CharTaskOperations
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from src.database.database import db

if __name__ == "__main__":
    """
    Main script to create a character, create a task, assign the task to the character,
    retrieve tasks for the character, mark the task as completed, and retrieve tasks again.
    """

    char_ops = Character(db)
    task_ops = TaskOperations(db)
    char_task_ops = CharTaskOperations(db)

    # Create a character and a task
    char_id = char_ops.create_character("Jaina", "Human", "Mage")
    task_id = task_ops.create_task("Gather magical herbs", 25, "2025-02-01")

    # Assign the task to the character
    char_task_ops.assign_task_to_character(char_id, task_id)

    # Retrieve tasks for the character
    char_task_ops.get_tasks_for_character(char_id)

    # Mark the task as completed
    char_task_ops.mark_task_as_completed(char_id, task_id)

    # Retrieve tasks again
    char_task_ops.get_tasks_for_character(char_id)