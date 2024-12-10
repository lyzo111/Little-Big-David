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

# UI components
# !!! Establish connection to charTasks here. Tasks here are just wild cards
def main_menu():
    with ui.column().classes("items-center justify-center"):
        ui.label("Little Big David - Aufgaben").classes("text-2xl font-bold mb-4")
        ui.label("Hier stehen deine Aufgaben:").classes("mb-4")
        with ui.card().classes("w-1/2"):
            ui.label("1. Trainiere für 30 Minuten").classes("mb-2")
            ui.label("2. Lies ein Buchkapitel").classes("mb-2")
            ui.label("3. Trinke 2 Liter Wasser").classes("mb-2")
        ui.label("Wische nach rechts, um deinen Charakter anzupassen.")
        ui.label("Wische nach links, um in die Overworld zu gelangen.")