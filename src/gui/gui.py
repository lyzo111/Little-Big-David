from nicegui import ui
from nicegui.events import KeyEventArguments
import sqlite3
from pathlib import Path

from src.database import database
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from types import SimpleNamespace

# Global Variables
default_pfp = "default_pfp.jpg"
current_screen = "main_menu"
screens = ["overworld", "main_menu", "character_customization"]
content_row = ui.row().classes("w-screen flex justify-center")  # Container for centering content horizontally
left_button_container = ui.row().classes("absolute left-4 top-1/2 transform -translate-y-1/2")  # Left button container
right_button_container = ui.row().classes(
    "absolute right-4 top-1/2 transform -translate-y-1/2")  # Right button container

# State Objects
state = SimpleNamespace(name='', race='', roll='', description='', xp=0, expiration_date='', stage_name='',
                        stage_path='')
dark_mode = ui.dark_mode()
is_dark_mode = False  # Website starts in light mode

# Operation Instances
char_ops = Character()
task_ops = TaskOperations(database)


# Navigation
def toggle_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    dark_mode.toggle()
    mode_label.set_text('Dark Mode' if is_dark_mode else 'Light Mode')


with (ui.header().style('background-color: #1e293b; color: white;')):
    with ui.row().style('display: flex; align-items: center;'):
        ui.label('Little Big David')
        ui.link('Characters', '/characters')
        ui.link('Tasks', '/tasks')
        ui.link('Tutorial', '/tutorial')
    with ui.row().style('margin-left: auto; align-items: center; gap: 8px;'):
        mode_label = ui.label('Light Mode')
        # Lambda prevents toggle method from firing when code is run -> only fires when on_change method is triggered
        brightness_switch = ui.switch(on_change=(lambda e: toggle_mode()))


# Character Management
@ui.page('/characters')
def characters_page():
    with ui.row():
        ui.label('Characters Management').classes('text-h5')
    with ui.card():
        ui.input('Name').bind_value(state, 'name')
        ui.input('Race').bind_value(state, 'race')
        ui.input('Roll').bind_value(state, 'roll')
        ui.button('Create Character', on_click=lambda: create_character(state.name, state.race, state.roll))


# Task Management
@ui.page('/tasks')
def tasks_page():
    with ui.row():
        ui.label('Tasks Management').classes('text-h5')
    with ui.card():
        ui.input('Description').bind_value(state, 'description')
        ui.input('XP').bind_value(state, 'xp')
        ui.input('Expiration Date').bind_value(state, 'expiration_date')
        ui.button('Create Task', on_click=lambda: create_task(state.description, state.xp, state.expiration_date))


# Functions
def create_character(name, race, roll):
    char_ops.create_character(name, race, roll)
    ui.notify('Character created successfully!')


def create_task(description, xp, expiration_date):
    task_ops.create_task(description, xp, expiration_date)
    ui.notify('Task created successfully!')


# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


def load_profile_picture():
    try:
        conn = sqlite3.connect("littleBigDatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT profile_picture FROM user_profile LIMIT 1")
        result = cursor.fetchone()
        profile_pic = result[0] if result and result[0] else default_pfp
        if not Path(profile_pic).is_file():
            return default_pfp
        return profile_pic
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return default_pfp


def toggle_profile_menu():
    with ui.menu():
        ui.menu_item("Einstellungen", on_click=lambda: ui.notify("Einstellungen öffnen"))
        ui.menu_item("Tutorial erneut starten", on_click=lambda: ui.notify("Tutorial wird gestartet"))
        ui.menu_item("Disclaimer", on_click=lambda: ui.notify("Little Big David ist ein Spiel..."))


def profile_picture_menu():
    profile_pic = load_profile_picture()
    with ui.row().classes("absolute top-4 right-4"):
        with ui.button(on_click=toggle_profile_menu).classes("rounded-full p-0 w-16 h-16 cursor-pointer shadow-lg"):
            with ui.avatar():
                ui.image(f"img:{profile_pic}")


def switch_screen(direction):
    global current_screen
    current_index = screens.index(current_screen)

    if direction == "right" and current_index < len(screens) - 1:
        current_screen = screens[current_index + 1]
    elif direction == "left" and current_index > 0:
        current_screen = screens[current_index - 1]

    update_screen()


def update_screen():
    content_row.clear()
    left_button_container.clear()
    right_button_container.clear()

    profile_picture_menu()

    if current_screen == "main_menu":
        main_menu()
    elif current_screen == "character_customization":
        character_customization()
    elif current_screen == "overworld":
        overworld()

    navigation_buttons()


# !!! Establish connection to charTasks here. Tasks here are just wild cards
def main_menu():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Little Big David - Aufgaben").classes("text-2xl font-bold mb-4")
            ui.label("Hier stehen deine Aufgaben:").classes("mb-4")
            with ui.card().classes("w-1/2"):
                ui.label("1. Trainiere für 30 Minuten").classes("mb-2")
                ui.label("2. Lies ein Buchkapitel").classes("mb-2")
                ui.label("3. Trinke 2 Liter Wasser").classes("mb-2")


def character_customization():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Charakteranpassung").classes("text-2xl font-bold mb-4")
            ui.label("Hier kannst du deinen Charakter anpassen!").classes("mb-4")
            ui.label("Noch keine Anpassungsoptionen implementiert...").classes("mb-2")


# !!! Get path for .png from littleBigDatabase.db
def overworld():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Overworld - Deine Reise").classes("text-2xl font-bold mb-4")
            with ui.card().classes("items-center justify-center p-4"):
                ui.label("Hier siehst du David auf seiner Reise:")
                ui.image("david_sprite.png").classes("w-16 h-16")
                ui.label("Gegner: Böser Boss").classes("mt-4")
                ui.image("enemy_sprite.png").classes("w-16 h-16")


def navigation_buttons():
    current_index = screens.index(current_screen)

    # Left button
    if current_index > 0:
        with left_button_container:
            ui.button(on_click=lambda: switch_screen("left")).props("fab icon=arrow_back").classes(
                "rounded-full shadow-lg")

    # Right button
    if current_index < len(screens) - 1:
        with right_button_container:
            ui.button(on_click=lambda: switch_screen("right")).props("fab icon=arrow_forward").classes(
                "rounded-full shadow-lg")


# Home screen
update_screen()
ui.run(title='Little Big RPG', port=8080)
