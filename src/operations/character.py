import sqlite3
from src.database import utils
from src.database.database import Database


class Character:
    def __init__(self, db):
        """
        Initializes a new instance of the Character class.
        """
        self.db = db

    def create_character(self, name, race, classname, profile_image=None):
        """
        Creates a new character with the given name, race, class, and optional profile image.

        This function inserts a new character into the database and sets default values for the character's stats.

        Args:
            name (str): The name of the character.
            race (str): The race of the character.
            classname (str): The class of the character.
            profile_image (str, optional): The path to the profile image of the character. Defaults to "utils/default_pfp.jpg".

        Returns:
            dict: A dictionary containing the success status and a message or character ID.
        """
        try:
            if not name or not race or not classname:
                return {"success": False, "message": "Name, Race, and Class cannot be empty."}

            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Check if name already exists
            cursor.execute("SELECT 1 FROM char WHERE name = ?", (name,))
            if cursor.fetchone():
                return {"success": False, "message": f"A character with the name '{name}' already exists."}

            # Validating race and class
            cursor.execute("SELECT 1 FROM race WHERE name = ?", (race,))
            if not cursor.fetchone():
                return {"success": False, "message": f"Race '{race}' does not exist in the database."}

            cursor.execute("SELECT 1 FROM classname WHERE name = ?", (classname,))
            if not cursor.fetchone():
                return {"success": False, "message": f"Class '{classname}' does not exist in the database."}

            # Insert character into database
            cursor.execute(
                "INSERT INTO char (name, race, classname, profile_image) VALUES (?, ?, ?, ?)",
                (name, race, classname, profile_image or utils.default_pfp)
            )
            char_id = cursor.lastrowid

            # Setting default values for character
            cursor.execute(
                "INSERT INTO charStat (charID, level, charisma, crafting, health, strength, defense, intelligence, luck) "
                "VALUES (?, 1, 10, 10, 10, 10, 10, 10, 10)",
                (char_id,)
            )

            connection.commit()
            connection.close()
            return {"success": True, "message": f"Character '{name}' was created successfully.", "char_id": char_id}

        except sqlite3.Error as e:
            return {"success": False, "message": f"An error occurred: {e}"}

    def read_character_by_id(self, char_id):
        """
        Retrieves a character from the database by its ID.

        Args:
            char_id (int): The ID of the character to retrieve.

        Returns:
            dict: A dictionary containing the success status and the character data or an error message.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            # Call character values by ID
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
        """
        Updates the details of an existing character.

        Args:
            char_id (int): The ID of the character to update.
            new_name (str, optional): The new name of the character.
            new_race (str, optional): The new race of the character.
            new_classname (str, optional): The new class of the character.

        Returns:
            bool: True if the character was updated successfully, False otherwise.
        """
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
                connection.close()
                print(f"Character with ID {char_id} was updated successfully.")
                return True
            else:
                connection.close()
                print("No updates were provided.")
                return False

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

    def delete_character(self, char_id):
        """
        Deletes a character from the database by its ID.

        Args:
            char_id (int): The ID of the character to delete.

        Returns:
            bool: True if the character was deleted successfully, False otherwise.
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM char WHERE charID = ?", (char_id,))
            connection.commit()
            connection.close()
            print(f"Character with ID {char_id} was deleted successfully.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False