import sqlite3
import datetime

from nicegui import ui

from src.database import utils
from pathlib import Path

from src.database import database
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from types import SimpleNamespace

# Global Variables
default_pfp = "default_pfp.jpg"
current_screen = "main_menu"
screens = ["overworld", "main_menu", "character_customization"]
content_row = ui.row().classes("w-full flex justify-center")  # Container for centering content horizontally
left_button_container = ui.row().classes("absolute left-4 top-1/2 transform -translate-y-1/2")  # Left button container
right_button_container = ui.row().classes(
    "absolute right-4 top-1/2 transform -translate-y-1/2")  # Right button container

# State Objects
state = SimpleNamespace(name='', race='', classname='', description='', xp=0, expiration_date='', stage_name='',
                        stage_path='')
dark_mode = ui.dark_mode()
is_dark_mode = False  # Website starts in light mode

# Operation Instances
char_ops = Character()
task_ops = TaskOperations(database)

# Change switch style
ui.add_css('''
.dark .custom-dark-mode-switch div::before, .dark .custom-dark-mode-switch div::after {
    background-color: black !important;
}
.dark .custom-dark-mode-switch .q-toggle__track {
    background-color: white !important;
}
''')


# Navigation
def toggle_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    dark_mode.toggle()
    mode_label.set_text('Dark Mode' if is_dark_mode else 'Light Mode')


with ui.header().style('color: white; display: flex; align-items: center;'):
    ui.label('Little Big David')
    ui.link('Characters', '/characters').style('color: white;')
    ui.link('Tasks', '/tasks').style('color: white;')
    ui.link('Tutorial', '/tutorial').style('color: white;')
    with ui.row().style('margin-left: auto; align-items: center; gap: 8px;'):
        mode_label = ui.label('Light Mode')
        brightness_switch = ui.switch(on_change=(lambda e: toggle_mode())).classes('custom-dark-mode-switch')


# Character Management
def characters_dialog():
    classes = utils.get_classes()
    races = utils.get_races()

    with ui.dialog() as character_dialog, ui.card():
        with ui.row():
            ui.label('Characters Management').classes('text-h5')
        with (ui.card()):
            ui.input('Name').bind_value(state, 'name')
            ui.select(
                options=races, label='Races', value=races[0]).bind_value(state, 'races')
            ui.select(
                options=classes, label='Classes', value=classes[0]).bind_value(state, 'class')
            ui.upload(on_upload=(lambda e: ui.notify(f'Uploaded: {e.name}')), on_rejected=lambda e: ui.notify('Rejected!')
                      ).props('accept="image/*"')

            ui.button('Create Character', on_click=lambda: create_character(state.name, state.race, state.classname))
    return character_dialog


# Date Input
def date_input():
    def format_date(value):
        # Convert 'yyyy-mm-dd' to 'dd.mm.yyyy' for display
        if value:
            return datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
        return ""

    def parse_date(value):
        # Convert 'dd.mm.yyyy' back to 'yyyy-mm-dd' for internal storage
        try:
            return datetime.datetime.strptime(value, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            return ""

    with ui.input('Date') as date:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date, forward=format_date, backward=parse_date):

                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close).props('flat')

        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

    return date


# Task Management
def tasks_dialog():
    with ui.dialog() as task_dialog, ui.card():
        with ui.row():
            ui.label('Tasks Management').classes('text-h5')
        with ui.card():
            ui.input('Description').bind_value(state, 'description')
            ui.input('XP').bind_value(state, 'xp')
            date_input().bind_value(state, 'expiration_date')
            ui.button('Create Task',
                      on_click=lambda: create_task(state.description, state.xp, state.expiration_date))
    return task_dialog


# Functions
def create_character(name, race, classname):
    char_ops.create_character(name, race, classname)
    ui.notify('Character created successfully!')


def create_task(description, xp, expiration_date):
    task_ops.create_task(description, xp, expiration_date)
    ui.notify('Task created successfully!')


def load_profile_picture():
    try:
        conn = sqlite3.connect("../../littleBigDatabase.db")
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
        ui.menu_item("Settings", on_click=lambda: ui.notify("Opening settings"))
        ui.menu_item("Restart Tutorial", on_click=lambda: ui.notify("Tutorial was restarted"))
        ui.menu_item("Disclaimer", on_click=lambda: ui.notify("Little Big David is just a game..."))


def profile_picture_menu():
    profile_pic = load_profile_picture()
    with ui.row().classes("absolute top-4 right-4"):
        with ui.button(on_click=toggle_profile_menu).classes("rounded-full p-0 w-16 h-16 cursor-pointer shadow-lg"):
            with ui.avatar():
                ui.image(f"img:{profile_pic}")


# !!! Establish connection to charTasks here. Tasks here are just wild cards
def quests():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Quests").classes("text-2xl font-bold mb-4")
            ui.label("Here are your quests:").classes("mb-4")
            with ui.card():
                ui.label("1. Train for 30 minutes").classes("mb-2")
                ui.label("2. Read a chapter of any book").classes("mb-2")
                ui.label("3. Drink 2 liters of water").classes("mb-2")
                ui.button('Add Task', on_click=tasks_dialog).style('display: block; align-self: center;')


def character_customization():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Character Editor").classes("text-2xl font-bold mb-4")
            ui.label("Here you can configure your character!").classes("mb-4")
            ui.image(load_profile_picture()).classes("w-16 h-16 cursor-pointer"
            ).on('click', characters_dialog
                 ).style('border-color: black; border-width: 2px; border-style: solid; border-radius: 50%;')


# !!! Get path for .png from littleBigDatabase.db
def journey():
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Your Journey").classes("text-2xl font-bold mb-4")
            ui.label("Here you can see David on his journey:").classes("mb-4")
            with ui.card().classes("items-center justify-center p-4"):
                ui.image("david_sprite.png").classes("w-16 h-16")
                ui.label("Enemy: Big Boss >:c").classes("mt-4")
                ui.image("enemy_sprite.png").classes("w-16 h-16")


def layout():
    quests()
    character_customization()
    journey()


layout()


def initialize_gui():
    ui.run(title='Little Big RPG', port=8080)
