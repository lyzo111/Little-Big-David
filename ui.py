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

def character_customization():
    with ui.column().classes("items-center justify-center"):
        ui.label("Charakteranpassung").classes("text-2xl font-bold mb-4")
        ui.label("Hier kannst du deinen Charakter anpassen!").classes("mb-4")
        # Examples for customization
        ui.label("Noch keine Anpassungsoptionen implementiert...").classes("mb-2")

def overworld():
    with ui.column().classes("items-center justify-center"):
        ui.label("Overworld - Deine Reise").classes("text-2xl font-bold mb-4")
        with ui.card().classes("items-center justify-center p-4"):
            ui.label("Hier siehst du David auf seiner Reise:")
            ui.image("david_sprite.png").classes("w-16 h-16")
            ui.label("Gegner: Böser Boss").classes("mt-4")
            ui.image("enemy_sprite.png").classes("w-16 h-16")

# profile picture and dropdown logic
def profile_picture_menu():
    load_profile_picture()
    profile_pic = (
        profile_picture if profile_picture and Path(profile_picture).is_file() else "default_profile.png"
    )
    with ui.row().classes("absolute top-4 right-4"):
        with ui.avatar(img=profile_pic).classes("w-16 h-16 cursor-pointer") as avatar:
            with ui.menu(trigger=avatar):
                ui.menu_item("Einstellungen", on_click=lambda: ui.notify("Einstellungen öffnen"))
                ui.menu_item("Tutorial erneut starten", on_click=lambda: Tutorial().show())
                ui.menu_item("Disclaimer", on_click=lambda: ui.notify("Little Big David ist ein Spiel..."))
