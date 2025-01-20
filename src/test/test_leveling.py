from src.database.database import Database
from src.database.leveling import LevelingSystem

if __name__ == "__main__":
    db = Database()
    leveling = LevelingSystem(db)

    # Test-Charakter-ID (stelle sicher, dass dieser Charakter existiert)
    char_id = 1

    print("Test: XP hinzufügen und Level-Up prüfen")
    success, level_up = leveling.add_xp(char_id, 150)
    if success:
        print(f"XP erfolgreich hinzugefügt. Level-Up: {level_up}")
    else:
        print("Fehler beim Hinzufügen von XP.")

    if level_up:
        print("Test: Stats bei Level-Up verbessern")
        stats_improved = leveling.improve_stats_on_level_up(char_id)
        if stats_improved:
            print("Stats erfolgreich verbessert.")
        else:
            print("Fehler beim Verbessern der Stats.")
