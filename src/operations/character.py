import sqlite3

class Database:
    def create_connection(self):
        return sqlite3.connect("../../littleBigDatabase.db")  # Path of database


class Character:
    def __init__(self):
        self.db = Database()

    def create_character(self, name, race, classname, profile_image=None):
        try:
            if not name or not race or not classname:
                return {"success": False, "message": "Name, Race, and Class cannot be empty."}

            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Prüfen, ob der Name bereits existiert
            cursor.execute("SELECT 1 FROM char WHERE name = ?", (name,))
            if cursor.fetchone():
                return {"success": False, "message": f"A character with the name '{name}' already exists."}

            # Validierung von Rasse und Klasse
            cursor.execute("SELECT 1 FROM race WHERE name = ?", (race,))
            if not cursor.fetchone():
                return {"success": False, "message": f"Race '{race}' does not exist in the database."}

            cursor.execute("SELECT 1 FROM classname WHERE name = ?", (classname,))
            if not cursor.fetchone():
                return {"success": False, "message": f"Class '{classname}' does not exist in the database."}

            # Charakter einfügen
            cursor.execute(
                "INSERT INTO char (name, race, classname, profile_image) VALUES (?, ?, ?, ?)",
                (name, race, classname, profile_image or "default_pfp.jpg")
            )
            char_id = cursor.lastrowid

            # Standardwerte für Stats
            cursor.execute(
                "INSERT INTO charStat (charID, level, charisma, crafting, health, strength, defense, intelligence, luck) "
                "VALUES (?, 1, 10, 10, 10, 10, 10, 10, 10)",
                (char_id,)
            )

            connection.commit()
            return {"success": True, "message": f"Character '{name}' was created successfully.", "char_id": char_id}

        except sqlite3.Error as e:
            return {"success": False, "message": f"An error occurred: {e}"}

        finally:
            connection.close()

    def read_character_by_id(self, char_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Charakterdaten abrufen
            cursor.execute("SELECT * FROM char WHERE charID = ?", (char_id,))
            user = cursor.fetchone()

            connection.close()

            if user:
                print(f"ID: {user[0]}, Name: {user[1]}, Race: {user[2]}, Classe: {user[3]}, Profile Image: {user[4]}")
                return {"success": True, "data": user}
            else:
                print(f"No character found with ID {char_id}.")
                return {"success": False, "message": f"No character found with ID {char_id}."}

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return {"success": False, "message": f"An error occurred: {e}"}

    def update_character(self, char_id, new_name=None, new_race=None, new_classname=None):
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
            if new_classname:
                updates.append("classname = ?")
                values.append(new_classname)

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
