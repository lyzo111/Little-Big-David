from src.database.database import Database
from src.database.leveling import LevelingSystem

if __name__ == "__main__":
    """
    Main script to test adding XP to a character and checking for level-up,
    as well as improving stats upon level-up using the LevelingSystem class.
    """

    # Create the database instance
    db = Database()

    # Create the LevelingSystem instance
    leveling = LevelingSystem(db)

    # Test character ID (ensure this character exists)
    char_id = 1

    print("Test: Add XP and check for level-up")
    success, level_up = leveling.add_xp(char_id, 150)
    if success:
        print(f"XP successfully added. Level-Up: {level_up}")
    else:
        print("Error adding XP.")

    if level_up:
        print("Test: Improve stats on level-up")
        stats_improved = leveling.improve_stats_on_level_up(char_id)
        if stats_improved:
            print("Stats successfully improved.")
        else:
            print("Error improving stats.")