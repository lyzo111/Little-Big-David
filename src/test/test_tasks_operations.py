from src.operations.task_operations import TaskOperations

if __name__ == "__main__":
    task_ops = TaskOperations()

    # Aufgabe erstellen
    task_id = task_ops.create_task("Defeat the Lich King", 50, "2025-01-31")

    # Aufgabe abrufen
    task_ops.get_task(task_id)

    # Aufgabe aktualisieren
    task_ops.update_task(task_id, description="Defeat Arthas", xp=75, expiration_date="2025-02-15")

    # Aufgabe erneut abrufen
    task_ops.get_task(task_id)

    # Aufgabe löschen
    task_ops.delete_task(task_id)

    # Gelöschte Aufgabe abrufen
    task_ops.get_task(task_id)
