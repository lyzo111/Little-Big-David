# This is a Little Big David.
import sqlite3
from src.gui import gui
from tutorial import Tutorial
from src.database.database import init_db, populate_database


def is_first_time() -> bool:
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
    print("Initializing database...")
    init_db()
    populate_database()

    if is_first_time():
        Tutorial().show()
        # Add character creation

    gui.initialize_gui()