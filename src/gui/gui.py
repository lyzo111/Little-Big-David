import sqlite3
import datetime

from nicegui import ui

from src.database import utils
from pathlib import Path

from src.database.database import db
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from types import SimpleNamespace

"""
This module contains the GUI implementation for the Little Big RPG game.
It uses the NiceGUI framework to create and manage the user interface.
"""

default_pfp = utils.default_pfp
content_row = ui.row().classes("w-full flex justify-center")  # Container for centering content horizontally

# State Objects
state = SimpleNamespace(name='', race='', classname='', description='', xp=0, expiration_date='', stage_name='',
                        stage_path='')
dark_mode = ui.dark_mode()
is_dark_mode = False  # Website starts in light mode

# Operation Instances
char_ops = Character(db)
task_ops = TaskOperations(db)

# Change switch style
ui.add_css('''
.dark .custom-dark-mode-switch div::before, .dark .custom-dark-mode-switch div::after {
    background-color: black !important;
}
.dark .custom-dark-mode-switch .q-toggle__track {
    background-color: white !important;
}
''')


def toggle_mode():
    """
    Toggles the website's mode between dark and light.

    This function switches the global `is_dark_mode` variable between True and False,
    toggles the `dark_mode` UI element, and updates the `mode_label` text to reflect
    the current mode.
    """
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    dark_mode.toggle()
    mode_label.set_text('Dark Mode' if is_dark_mode else 'Light Mode')


with ui.header().style('color: white; display: flex; align-items: center;'):
    ui.label('Little Big David').classes('text-h6')
    with ui.row().style('margin-left: auto; align-items: center; gap: 8px;'):
        mode_label = ui.label('Light Mode')
        brightness_switch = ui.switch(on_change=(lambda e: toggle_mode())).classes('custom-dark-mode-switch')


# Character Management
def characters_dialog():
    """
   Creates and returns a dialog for character management.

   This function retrieves available classes and races using utility functions,
   and constructs a dialog with input fields for character name, race, and class.
   It also includes an upload button for profile pictures and a button to create
   a new character.

   Returns:
       ui.dialog: The constructed character management dialog.
    """
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
                options=classes, label='Classes', value=classes[0]).bind_value(state, 'classes')
            ui.upload(on_upload=(lambda e: ui.notify(f'Uploaded: {e.name}')),
                      on_rejected=lambda e: ui.notify('Rejected!')
                      ).props('accept="image/*"')

            ui.button('Create Character',
                      on_click=lambda: create_character(state.name, state.races, state.classes, character_dialog))
    return character_dialog


def date_input():
    """
    Creates and returns a date input field with a custom date format.

    This function constructs a date input field that displays dates in 'dd.mm.yyyy'
    format and converts them back to 'yyyy-mm-dd' format for internal storage. It
    includes a calendar icon to open a date picker menu.

    Returns:
        ui.input: The constructed date input field.
    """

    def format_date(value):
        """
        Converts a date from 'yyyy-mm-dd' format to 'dd.mm.yyyy' format.

        Args:
            value (str): The date in 'yyyy-mm-dd' format.

        Returns:
            str: The date in 'dd.mm.yyyy' format, or an empty string if the input is None.
        """
        if value:
            return datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
        return ""

    def reformat_date(value):
        """
        Converts a date from 'dd.mm.yyyy' format to 'yyyy-mm-dd' format.
        Args:
            value (str): The date in 'dd.mm.yyyy' format.
        Returns:
            str: The date in 'yyyy-mm-dd' format, or an empty string if the input is invalid.
        """
        try:
            return datetime.datetime.strptime(value, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            return ""

    with ui.input('Date') as date:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date, forward=format_date, backward=reformat_date):
                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close).props('flat')

        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

    return date


# Task Management
def tasks_dialog():
    """
    Creates and returns a dialog for task management.

    This function constructs a dialog with input fields for task description, XP,
    and expiration date. It includes a button to create a new task.

    Returns:
        ui.dialog: The constructed task management dialog.
    """
    with ui.dialog() as task_dialog, ui.card():
        with ui.row():
            ui.label('Tasks Management').classes('text-h5')
        with ui.card():
            ui.input('Description').bind_value(state, 'description')
            ui.number(label='XP', format='%.0f', max=150
                      ).bind_value(state, 'xp')
            date_input().bind_value(state, 'expiration_date')
            ui.button('Create Task',
                      on_click=lambda: create_task(state.description, state.xp, state.expiration_date, task_dialog))
    return task_dialog


# Functions
def create_character(name, race, classname, character_dialog):
    """
    Creates a new character with the given name, race, and class.

    This function uses the `char_ops` instance to create a new character. If the
    character is created successfully, it displays a success notification and closes
    the character dialog. Otherwise, it displays an error notification.

    Args:
        :param name: The name of the character.
        :param race: The race of the character.
        :param classname: The class of the character.
        :param character_dialog: The dialog for character management.
    """
    result = char_ops.create_character(name, race, classname, default_pfp)
    if result and result.get('success'):
        ui.notify('Character created successfully!')
        character_dialog.close()
    else:
        ui.notify('An error occurred while creating the character.')


def create_task(description, xp, expiration_date, task_dialog):
    """
    Creates a new task with the given description, XP, and expiration date.

    This function uses the `task_ops` instance to create a new task. If the task is
    created successfully, it displays a success notification and closes the task
    dialog. Otherwise, it displays an error notification.

    Args:
        :param description: The description of the task.
        :param xp: The XP value of the task.
        :param expiration_date: The expiration date of the task in 'yyyy-mm-dd' format.
        :param task_dialog: The dialog for task management.
    """
    if task_ops.create_task(description, xp, expiration_date):
        ui.notify('Task created successfully!')
        task_dialog.close()
    else:
        ui.notify('An error occurred while creating the task.')


def load_profile_picture():
    """
    Loads the profile picture for the user.

    This function connects to the database to retrieve the profile picture path for the user.
    If the profile picture is not found or the file does not exist, it returns the default profile picture path.

    Returns:
        str: The path to the profile picture.
    """
    try:
        conn = db.create_connection()
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


# TODO: Either implement the following functions later on or discard them
def toggle_profile_menu():
    """
    Toggles the profile menu.

    This function creates a menu with options for settings, restarting the tutorial, and displaying a disclaimer.
    """
    with ui.menu():
        ui.menu_item("Settings", on_click=lambda: ui.notify("Opening settings"))
        ui.menu_item("Restart Tutorial", on_click=lambda: ui.notify("Tutorial was restarted"))
        ui.menu_item("Disclaimer", on_click=lambda: ui.notify("Little Big David is just a game..."))


def profile_picture_menu():
    """
    Displays the profile picture menu.

    This function loads the profile picture and creates a button with the profile picture.
    Clicking the button toggles the profile menu.
    """
    profile_pic = load_profile_picture()
    with ui.row().classes("absolute top-4 right-4"):
        with ui.button(on_click=toggle_profile_menu).classes("rounded-full p-0 w-16 h-16 cursor-pointer shadow-lg"):
            with ui.avatar():
                ui.image(load_profile_picture())


# TODO: Establish connection to charTasks here. Tasks here are just wild cards
def quests():
    """
    Displays the quests section.

    This function creates a section in the UI to display the user's quests and includes a button to add new tasks.
    """
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
    """
    Displays the character customization section.

    This function creates a section in the UI for character customization, including an image of the profile picture
    and a button to open the character management dialog.
    """
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Character Editor").classes("text-2xl font-bold mb-4")
            ui.label("Here you can configure your character!").classes("mb-4")
            ui.image(load_profile_picture()).classes("w-16 h-16 cursor-pointer"
                                                     ).on('click', characters_dialog
                                                          ).style(
                'border-color: black; border-width: 2px; border-style: solid; border-radius: 50%;')


# TODO: Get path for .png from littleBigDatabase.db
def journey():
    """
    Displays the journey section.

    This function creates a section in the UI to display the user's journey, including images of the character and enemy.
    """
    with content_row:
        with ui.column().classes("items-center justify-center"):
            ui.label("Your Journey").classes("text-2xl font-bold mb-4")
            ui.label("Here you can see David on his journey:").classes("mb-4")
            with ui.card().classes("items-center justify-center p-4"):
                ui.image("david_sprite.png").classes("w-16 h-16")
                ui.label("Enemy: Big Boss >:c").classes("mt-4")
                ui.image("enemy_sprite.png").classes("w-16 h-16")


def layout():
    """
    Sets up the layout of the application.

    This function calls the functions to display the quests, character customization, and journey sections.
    """
    quests()
    character_customization()
    journey()


layout()


def initialize_gui():
    """
    Initializes and runs the GUI.

    This function sets the title and port for the NiceGUI application and starts the UI.
    """
    ui.run(title='Little Big RPG', port=8080)
