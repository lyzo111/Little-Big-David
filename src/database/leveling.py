import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../../littleBigDatabase.db")  # Your actual database path

class LevelingSystem:
    def __init__(self, db):
        self.db = db

    def add_xp(self, char_id, xp_gain):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Aktuelle XP und Level des Charakters abrufen
            cursor.execute("SELECT xp, level FROM charStat WHERE charID = ?", (char_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Character with ID {char_id} does not exist.")
                return False, False  # Kein Erfolg, kein Level-Up

            current_xp, level = result

            # Neue XP berechnen
            new_xp = current_xp + xp_gain
            level_up = False

            # Level-Up prüfen
            if new_xp >= 100:
                new_xp -= 100
                level += 1
                level_up = True
                print(f"Character {char_id} leveled up to Level {level}!")

            # XP und Level in der Datenbank aktualisieren
            cursor.execute(
                "UPDATE charStat SET xp = ?, level = ? WHERE charID = ?",
                (new_xp, level, char_id)
            )
            connection.commit()
            print(f"{xp_gain} XP added to character {char_id}. New XP: {new_xp}, Level: {level}")

            return True, level_up  # Erfolg und Level-Up-Status zurückgeben

        except sqlite3.Error as e:
            print(f"An error occurred while adding XP: {e}")
            return False, False  # Kein Erfolg, kein Level-Up

        finally:
            connection.close()


    def improve_stats_on_level_up(self, char_id):
        try:
            connection = self.db.create_connection()
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
