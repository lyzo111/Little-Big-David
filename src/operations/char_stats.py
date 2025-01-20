import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../littleBigDatabase.db")  # Your actual database path

class CharacterOperations:
    def __init__(self, db):
        self.db = db

    def create_character(self, name, race, classname):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Insert character details
            cursor.execute("INSERT INTO char (name, race, classname) VALUES (?, ?, ?)", (name, race, classname))
            connection.commit()

            # Get the ID of the newly created character
            char_id = cursor.lastrowid

            # Insert initial stats for the character in charStat
            cursor.execute("INSERT INTO charStat (charID) VALUES (?)", (char_id,))
            connection.commit()

            connection.close()
            print(f"Character {name} created successfully with ID {char_id}.")
            return char_id

        except sqlite3.IntegrityError:
            print(f"A character with the name {name} already exists.")
            return None

    def read_character_by_name(self, name):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM char WHERE name = ?", (name,))
            character = cursor.fetchone()
            connection.close()

            if character:
                print(f"Found character: ID: {character[0]}, Name: {character[1]}, Race: {character[2]}, Class: {character[3]}")
                return character
            else:
                print(f"No character found with the name {name}")
                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def update_character(self, char_id, new_name, new_race, new_classname):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("UPDATE char SET name = ?, race = ?, classname = ? WHERE charID = ?",
                           (new_name, new_race, new_classname, char_id))
            connection.commit()
            connection.close()
            print(f"Character with ID {char_id} updated successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

    def delete_character(self, char_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM char WHERE charID = ?", (char_id,))
            connection.commit()
            connection.close()
            print(f"Character with ID {char_id} deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False


class CharacterStatsOperations:
    def __init__(self, db):
        self.db = db

    def update_stats(self, char_id, **stats):
        """Updates character stats."""
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            for stat, value in stats.items():
                cursor.execute(f"UPDATE charStat SET {stat} = ? WHERE charID = ?", (value, char_id))

            connection.commit()
            connection.close()
            print(f"Stats for character with ID {char_id} updated successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

    def read_stats(self, char_id):
        """Reads the stats of a specific character."""
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM charStat WHERE charID = ?", (char_id,))
            stats = cursor.fetchone()
            connection.close()

            if stats:
                print(f"Stats for character ID {char_id}: {stats}")
                return stats
            else:
                print(f"No stats found for character with ID {char_id}")
                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    db = Database()

    # Character operations
    char_ops = CharacterOperations(db)
    char_ops.create_character("Arthas", "Human", "Warrior")
    char_ops.read_character_by_name("Arthas")

    # Character stats operations
    stats_ops = CharacterStatsOperations(db)
    stats_ops.read_stats(1)
    stats_ops.update_stats(1, health=10, strength=15)
    stats_ops.read_stats(1)
