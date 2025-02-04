from src.database.database import Database
from src.operations.character import Character

if __name__ == "__main__":
    """
    Main script to create, retrieve, update, and delete a character using the Character class.
    """

    # Create the database instance
    db = Database()

    # Create the Character operations instance
    char_ops = Character()

    # Create a character
    char_result = char_ops.create_character(name="Arthas", race="Human", classname="Paladin", profile_image=None)
    if char_result["success"]:
        char_id = char_result["char_id"]
        print(f"Character created with ID: {char_id}")

        # Retrieve the character
        print("\nRetrieve character:")
        char_ops.read_character_by_id(char_id)

        # Update the character
        print("\nUpdate character:")
        char_ops.update_character(char_id, new_name="Arthas Menethil", new_race="Undead", new_classname="Death Knight")

        # Retrieve the updated character
        print("\nRetrieve updated character:")
        char_ops.read_character_by_id(char_id)

        # Delete the character
        print("\nDelete character:")
        char_ops.delete_character(char_id)

        # Attempt to retrieve the deleted character
        print("\nRetrieve deleted character:")
        char_ops.read_character_by_id(char_id)
    else:
        print(f"Error creating character: {char_result['message']}")