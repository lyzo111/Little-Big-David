# This is a Little Big David.
import sqlite3
from src.gui import gui
from tutorial import Tutorial
from src.database.database import init_db, populate_database


def is_first_time() -> bool:
    """
    Check if this is the first time the application is being run by querying the database.

    Returns:
        bool: True if this is the first time (no characters exist), False otherwise.
    """
    conn = sqlite3.connect('../littleBigDatabase.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM char)")
        result = bool(cursor.fetchone()[0])
    finally:
        # Invert bool to make name of method correspond to value of bool
        # Returns 'True' if user exists, otherwise 'False'
        return not result if result is not None else False


if __name__ in {"__main__", "__mp_main__"}:
    """
    Main entry point of the application. Initializes the database and populates it with initial data.
    If this is the first time the application is run, it shows the tutorial.
    """
    print("Initializing database...")
    init_db()
    populate_database()

    # Uncomment the following lines to show the tutorial if this is the first time
    # if is_first_time():
    #     Tutorial().show()
    #     Add character creation

    gui.initialize_gui()