from src.database.database import db

def get_data(table_name):
    """
    Retrieves data from a specified table in the database.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        list: A list of names retrieved from the specified table.
    """
    query = f"SELECT name FROM {table_name}"
    connection = db.create_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    data = [row[0] for row in cursor.fetchall()]
    connection.close()
    return data

def get_classes():
    """
    Retrieves class names from the 'classname' table in the database.

    Returns:
        list: A list of class names.
    """
    return get_data("classname")

def get_races():
    """
    Retrieves race names from the 'race' table in the database.

    Returns:
        list: A list of race names.
    """
    return get_data("race")

def get_tasks():
    """
    Retrieves task descriptions from the 'task' table in the database.

    Returns:
        list: A list of task descriptions.
    """
    return get_data("task")