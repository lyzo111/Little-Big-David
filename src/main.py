# This is a Little Big David.
import sqlite3
from nicegui import ui
from tutorial import Tutorial

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


if __name__ == '__main__':
    if is_first_time():
        Tutorial().show()
        # Add character creation



    ui.run()