import sqlite3

class LevelingSystem:
    def __init__(self, db_path="littleBigDatabase.db"):
        self.db_path = db_path

    def add_xp(self, char_id, xp_gain):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Aktuelle XP und Level des Charakters abrufen
            cursor.execute("SELECT xp, level FROM charStat WHERE charID = ?", (char_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Character with ID {char_id} does not exist.")
                return False

            current_xp, level = result


            new_xp = current_xp + xp_gain
            if new_xp >= 100:
                new_xp -= 100
                level += 1
                print(f"Character {char_id} leveled up to Level {level}!")


            cursor.execute(
                "UPDATE charStat SET xp = ?, level = ? WHERE charID = ?",
                (new_xp, level, char_id)
            )
            connection.commit()
            print(f"{xp_gain} XP added to character {char_id}. New XP: {new_xp}, Level: {level}")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred while adding XP: {e}")
            return False

        finally:
            connection.close()

    def improve_stats_on_level_up(self, char_id):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()


            cursor.execute("SELECT level FROM charStat WHERE charID = ?", (char_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Character with ID {char_id} does not exist.")
                return False


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
