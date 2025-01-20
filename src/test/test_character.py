from src.database.database import Database

from src.operations.task_operations import TaskOperations

if __name__ == "__main__":
    # Erstelle die Datenbankinstanz
    db = Database()

    # Übergib die Datenbankinstanz an TaskOperations
    task_ops = TaskOperations(db)

    # Test: Aufgabe erstellen
    task_id = task_ops.create_task("Testaufgabe", 50, "2025-01-31")
    print(f"Erstellte Task-ID: {task_id}")
