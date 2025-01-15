import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../littleBigDatabase.db")  # Path of database


class Character:
    def __init__(self):
        self.db = Database()

    def create_character(self, name, race, roll):
        try:

            if not name or not race or not roll:
                print("Name, Race, and Roll cannot be empty.")
                return None

            connection = self.db.create_connection()
            cursor = connection.cursor()


            cursor.execute(
                "INSERT INTO char (name, race, roll) VALUES (?, ?, ?)",
                (name, race, roll)
            )
            char_id = cursor.lastrowid


            cursor.execute(
                "INSERT INTO charStat (charID, level, charisma, crafting, health, strength, defense, intelligence, luck) "
                "VALUES (?, 1, 10, 10, 10, 10, 10, 10, 10)",
                (char_id,)
            )

            connection.commit()
            print(f"Character '{name}' was created successfully with ID {char_id}.")
            return char_id

        except sqlite3.IntegrityError:
            print(f"A character with the name '{name}' already exists.")
            return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            connection.close()

    def read_character_by_id(self, char_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()


            cursor.execute("SELECT * FROM char WHERE charID = ?", (char_id,))
            user = cursor.fetchone()

            connection.close()

            if user:
                print(f"ID: {user[0]}, Name: {user[1]}, Race: {user[2]}, Roll: {user[3]}")
                return user
            else:
                print(f"No character found with ID {char_id}.")
                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def update_character(self, char_id, new_name=None, new_race=None, new_roll=None):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            updates = []
            values = []
            if new_name:
                updates.append("name = ?")
                values.append(new_name)
            if new_race:
                updates.append("race = ?")
                values.append(new_race)
            if new_roll:
                updates.append("roll = ?")
                values.append(new_roll)

            if updates:
                query = f"UPDATE char SET {', '.join(updates)} WHERE charID = ?"
                values.append(char_id)
                cursor.execute(query, values)
                connection.commit()
                print(f"Character with ID {char_id} was updated successfully.")
                return True
            else:
                print("No updates were provided.")
                return False

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()

    def delete_character(self, char_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()


            cursor.execute("DELETE FROM char WHERE charID = ?", (char_id,))
            connection.commit()
            print(f"Character with ID {char_id} was deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()
