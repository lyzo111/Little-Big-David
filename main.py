# This is a Little Big David.
import sqlite3
from nicegui import ui
from tutorial import Tutorial

def first_time() -> bool:
    conn = sqlite3.connect('littleBigDatabase.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM char)")
        result = bool(cursor.fetchone()[0])
    finally:
        # Invert bool to make logic apply to method name
        return not result if result is not None else False


if __name__ == '__main__':
    if first_time():
        Tutorial().show()
        # Add character creation



    ui.run()