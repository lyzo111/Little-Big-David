from nicegui import ui
from src.operations.character import Character
from src.operations.task_operations import TaskOperations
from src.operations.stage_operations import StageOperations
from types import SimpleNamespace

# State-Objekte
state = SimpleNamespace(name='', race='', roll='', description='', xp=0, expiration_date='', stage_name='', stage_path='')

# Operationen-Instanzen
char_ops = Character()
task_ops = TaskOperations()
stage_ops = StageOperations()

# Navigation
with ui.header():
    ui.label('Little Big RPG')
    ui.link('Characters', '/characters')
    ui.link('Tasks', '/tasks')
    ui.link('Stages', '/stages')

# Charakter-Management
@ui.page('/characters')
def characters_page():
    with ui.row():
        ui.label('Characters Management').classes('text-h5')
    with ui.card():
        ui.input('Name').bind_value(state, 'name')
        ui.input('Race').bind_value(state, 'race')
        ui.input('Roll').bind_value(state, 'roll')
        ui.button('Create Character', on_click=lambda: create_character(state.name, state.race, state.roll))

# Aufgaben-Management
@ui.page('/tasks')
def tasks_page():
    with ui.row():
        ui.label('Tasks Management').classes('text-h5')
    with ui.card():
        ui.input('Description').bind_value(state, 'description')
        ui.input('XP').bind_value(state, 'xp')
        ui.input('Expiration Date').bind_value(state, 'expiration_date')
        ui.button('Create Task', on_click=lambda: create_task(state.description, state.xp, state.expiration_date))

# Stages-Management
@ui.page('/stages')
def stages_page():
    with ui.row():
        ui.label('Stages Management').classes('text-h5')
    with ui.card():
        ui.input('Stage Name').bind_value(state, 'stage_name')
        ui.input('Stage Path').bind_value(state, 'stage_path')
        ui.button('Create Stage', on_click=lambda: create_stage(state.stage_name, state.stage_path))

# Funktionen
def create_character(name, race, roll):
    char_ops.create_character(name, race, roll)
    ui.notify('Character created successfully!')

def create_task(description, xp, expiration_date):
    task_ops.create_task(description, xp, expiration_date)
    ui.notify('Task created successfully!')

def create_stage(stage_name, stage_path):
    stage_ops.create_stage(stage_name, stage_path)
    ui.notify('Stage created successfully!')

# Server starten
ui.run(title='Little Big RPG', port=8080)
