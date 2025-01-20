from src.database.database import Database
from src.operations.character import Character

if __name__ == "__main__":
    db = Database()
    char_ops = Character()

    # Charakter erstellen
    char_result = char_ops.create_character(name="Arthas", race="Human", classname="Paladin", profile_image=None)
    if char_result["success"]:
        char_id = char_result["char_id"]
        print(f"Charakter erstellt mit ID: {char_id}")

        # Charakter abrufen
        print("\nCharakter abrufen:")
        char_ops.read_character_by_id(char_id)

        # Charakter aktualisieren
        print("\nCharakter aktualisieren:")
        char_ops.update_character(char_id, new_name="Arthas Menethil", new_race="Undead", new_classname="Death Knight")

        # Aktualisierten Charakter erneut abrufen
        print("\nAktualisierter Charakter abrufen:")
        char_ops.read_character_by_id(char_id)

        # Charakter löschen
        print("\nCharakter löschen:")
        char_ops.delete_character(char_id)

        # Gelöschten Charakter abrufen
        print("\nGelöschten Charakter abrufen:")
        char_ops.read_character_by_id(char_id)
    else:
        print(f"Fehler beim Erstellen des Charakters: {char_result['message']}")
