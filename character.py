import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("littleBigDatabase.db")  # Path of database

class Character:
    def __init__(self):
        self.db = Database()

    def create_character(self, name, race, roll):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Insert character basic info in chars table
            cursor.execute(
                "INSERT INTO chars (name, race, roll) VALUES (?, ?, ?)",
                (name, race, roll)
            )
            char_id = cursor.lastrowid  # Get the character's ID

            # Insert default stats in charStats for the new character
            cursor.execute(
                "INSERT INTO charStats (charID, level, charisma, crafting, health, strength, defense, intelligence, luck) "
                "VALUES (?, 1, 1, 1, 1, 1, 1, 1, 1)",
                (char_id,)
            )

            connection.commit()
            print(f"User {name} was created successfully with ID {char_id}.")
            return char_id  # Returns character ID

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            connection.close()

    def read_character_by_id(self, user_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM chars WHERE charID = ?", (user_id,))
            user = cursor.fetchone()

            connection.close()

            if user:
                print(f"ID: {user[0]}, Name: {user[1]}, Race: {user[2]}, Roll: {user[3]}")
                return user
            else:
                print(f"No user found with ID {user_id}")
                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def update_user(self, user_id, new_name, new_race, new_roll):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE chars SET name = ?, race = ?, roll = ? WHERE charID = ?",
                (new_name, new_race, new_roll, user_id)
            )

            connection.commit()
            print(f"User {user_id} was updated successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()

    def delete_user(self, user_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM chars WHERE charID = ?", (user_id,))
            connection.commit()
            print(f"User {user_id} was deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            connection.close()
