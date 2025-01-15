from src.operations.character_options import CharTaskOperations
from src.operations.character import Character
from src.operations.task_operations import TaskOperations

if __name__ == "__main__":
    char_ops = Character()
    task_ops = TaskOperations()
    char_task_ops = CharTaskOperations()

    # Charakter und Aufgabe erstellen
    char_id = char_ops.create_character("Thrall", "Orc", "Shaman")
    task_id = task_ops.create_task("Save the Horde", 120, "2025-03-01")

    # Aufgabe dem Charakter zuweisen
    char_task_ops.assign_task_to_character(char_id, task_id)

    # Aufgabe als abgeschlossen markieren
    char_task_ops.mark_task_as_completed(char_id, task_id)
