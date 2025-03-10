from tutorial import Tutorial
from src.database.database import init_db, populate_database, db


def is_first_time() -> bool:
    """
    Check if this is the first time the application is being run by querying the database.

    Returns:
        bool: True if this is the first time (no characters exist), False otherwise.
    """
    conn = db.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM char)")
    result = bool(cursor.fetchone()[0])

    # Invert bool to make name of method correspond to value of bool
    return not result if result is not None else False


if __name__ in {"__main__", "__mp_main__"}:
    """
    Main entry point of the application. Initializes the database and populates it with initial data.
    If this is the first time the application is run, it shows the tutorial.
    """
    print("Initializing database...")
    init_db(db)
    populate_database(db)

    # Uncomment the following lines to show the tutorial if this is the first time
    if is_first_time():
        Tutorial().show()

    from src.gui import gui

    if not is_first_time():
        gui.initialize_gui()
