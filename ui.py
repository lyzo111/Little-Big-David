from nicegui import ui
import sqlite3
from pathlib import Path

# Global variables
current_screen = "main_menu"
profile_picture = None

# Database connection and loading profile picture
def load_profile_picture():
    global profile_picture
    try:
        conn = sqlite3.connect("littleBigDatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT profile_picture FROM user_profile LIMIT 1")
        result = cursor.fetchone()
        if result and result[0]:
            profile_picture = result[0]  # Path or Base64 from database
        else:
            profile_picture = None
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        conn.close()
