import sqlite3

class Database:
    def create_connection(self):
        """
        Creates and returns a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The connection object to the SQLite database.
        """
        return sqlite3.connect("../../littleBigDatabase.db")  # Your actual database path

class LevelingSystem:
    def __init__(self, db):
        """
        Initializes a new instance of the LevelingSystem class.

        Args:
            db (Database): The database instance to use for database operations.
        """
        self.db = db

    def add_xp(self, char_id, xp_gain):
        """
        Adds XP to a character and checks for level-up.

        Args:
            char_id (int): The ID of the character to add XP to.
            xp_gain (int): The amount of XP to add.

        Returns:
            tuple: A tuple containing a boolean indicating success and a boolean indicating if a level-up occurred.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Retrieve current XP and level of the character
            cursor.execute("SELECT xp, level FROM charStat WHERE charID = ?", (char_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Character with ID {char_id} does not exist.")
                return False, False  # No success, no level-up

            current_xp, level = result

            # Calculate new XP
            new_xp = current_xp + xp_gain
            level_up = False

            # Check for level-up
            if new_xp >= 100:
                new_xp -= 100
                level += 1
                level_up = True
                print(f"Character {char_id} leveled up to Level {level}!")

            # Update XP and level in the database
            cursor.execute(
                "UPDATE charStat SET xp = ?, level = ? WHERE charID = ?",
                (new_xp, level, char_id)
            )
            connection.commit()
            print(f"{xp_gain} XP added to character {char_id}. New XP: {new_xp}, Level: {level}")

            return True, level_up  # Return success and level-up status

        except sqlite3.Error as e:
            print(f"An error occurred while adding XP: {e}")
            return False, False  # No success, no level-up

        finally:
            connection.close()

    def improve_stats_on_level_up(self, char_id):
        """
        Improves the stats of a character upon leveling up.

        Args:
            char_id (int): The ID of the character whose stats are to be improved.

        Returns:
            bool: True if the stats were improved successfully, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Retrieve the current level of the character
            cursor.execute("SELECT level FROM charStat WHERE charID = ?", (char_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Character with ID {char_id} does not exist.")
                return False

            # Update character stats on level up
            cursor.execute("""
                UPDATE charStat
                SET strength = strength + 1,
                    health = health + 5,
                    defense = defense + 1
                WHERE charID = ?
            """, (char_id,))
            connection.commit()
            print(f"Stats for character {char_id} improved on level up.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred while improving stats: {e}")
            return False

        finally:
            connection.close()