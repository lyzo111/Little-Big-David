from character import Character

if __name__ == "__main__":
    char = Character()

    # Charakter erstellen
    char_id = char.create_character("Arthas", "Human", "Paladin")

    # Charakter abrufen
    char.read_character_by_id(char_id)

    # Charakter aktualisieren
    char.update_character(char_id, new_name="Arthas Menethil", new_race="Undead")

    # Charakter erneut abrufen
    char.read_character_by_id(char_id)

    # Charakter löschen
    char.delete_character(char_id)

    # Gelöschten Charakter abrufen
    char.read_character_by_id(char_id)
