# This is a Little Big David.
import sqlite3

def first_time() -> bool:
    conn = sqlite3.connect('littleBigDatabase.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM char)")
        result = bool(cursor.fetchone()[0])
    finally:
        return result if result is not None else False

if __name__ == '__main__':
    first_time()
