# This is a Little Big David.
import sqlite3

def invert_bool(my_bool: bool) -> bool:
    return not my_bool

def first_time() -> bool:
    conn = sqlite3.connect('littleBigDatabase.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM char)")
        result = bool(cursor.fetchone()[0])
    finally:
        invert_bool(result if result is not None else False)

if __name__ == '__main__':
    if first_time():
        # Add character creation
        # Add tutorial (skippable)
        print()
