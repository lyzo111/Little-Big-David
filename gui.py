from nicegui import ui
import sqlite3
from pathlib import Path
from tutorial import Tutorial

# Global variables
current_screen = "main_menu"

# !!! Get path for .png from littleBigDatabase.db
def load_profile_picture():
    try:
        conn = sqlite3.connect("littleBigDatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT profile_picture FROM user_profile LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result and result[0] else "default_profile.png"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "default_profile.png"
    finally:
        conn.close()

def toggle_profile_menu():
    with ui.menu(close_on_trigger=True):
        ui.menu_item("Einstellungen", on_click=lambda: ui.notify("Einstellungen öffnen"))
        ui.menu_item("Tutorial erneut starten", on_click=lambda: Tutorial().show())
        ui.menu_item("Disclaimer", on_click=lambda: ui.notify("Little Big David ist ein Spiel..."))

def profile_picture_menu():
    profile_pic = load_profile_picture()
    with ui.row().classes("absolute top-4 right-4"):
        profile_avatar = ui.avatar(img=profile_pic).classes("w-16 h-16 cursor-pointer")
        profile_avatar.on_click(toggle_profile_menu)

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
        ui.label("Noch keine Anpassungsoptionen implementiert...").classes("mb-2")

# !!! Get path for .png from littleBigDatabase.db
def overworld():
    with ui.column().classes("items-center justify-center"):
        ui.label("Overworld - Deine Reise").classes("text-2xl font-bold mb-4")
        with ui.card().classes("items-center justify-center p-4"):
            ui.label("Hier siehst du David auf seiner Reise:")
            ui.image("david_sprite.png").classes("w-16 h-16")
            ui.label("Gegner: Böser Boss").classes("mt-4")
            ui.image("enemy_sprite.png").classes("w-16 h-16")

def switch_screen(direction):
    global current_screen
    screens = ["main_menu", "character_customization", "overworld"]
    current_index = screens.index(current_screen)

    if direction == "right":
        current_screen = screens[(current_index + 1) % len(screens)]
    elif direction == "left":
        current_screen = screens[(current_index - 1) % len(screens)]

    update_screen()

def update_screen():
    ui.clear()  # Clear all
    profile_picture_menu()  # Always show profile picture
    if current_screen == "main_menu":
        main_menu()
    elif current_screen == "character_customization":
        character_customization()
    elif current_screen == "overworld":
        overworld()

# Key and swipe events
ui.on_key("ArrowRight", lambda: switch_screen("right"))
ui.on_key("ArrowLeft", lambda: switch_screen("left"))
ui.on_swipe("left", lambda: switch_screen("left"))
ui.on_swipe("right", lambda: switch_screen("right"))

# Home screen
update_screen()

ui.run()