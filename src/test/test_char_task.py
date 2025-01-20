from src.operations.char_task_operations import CharTaskOperations
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from src.database.database import Database

if __name__ == "__main__":

    db = Database()
    char_ops = Character()
    task_ops = TaskOperations(db)
    char_task_ops = CharTaskOperations(db)

    # Charakter und Aufgabe erstellen
    char_id = char_ops.create_character("Jaina", "Human", "Mage")
    task_id = task_ops.create_task("Gather magical herbs", 25, "2025-02-01")

    # Aufgabe dem Charakter zuweisen
    char_task_ops.assign_task_to_character(char_id, task_id)

    # Aufgaben des Charakters abrufen
    char_task_ops.get_tasks_for_character(char_id)

    # Aufgabe als abgeschlossen markieren
    char_task_ops.mark_task_as_completed(char_id, task_id)

    # Aufgaben erneut abrufen
    char_task_ops.get_tasks_for_character(char_id)
