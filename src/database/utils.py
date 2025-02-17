from src.database.database import db

default_pfp = "assets/default_pfp.jpg"

def get_data(attribute, table):
    """
    Retrieves data from a specified table in the database.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        list: A list of names retrieved from the specified table.
    """
    query = f"SELECT {attribute} FROM {table}"
    connection = db.create_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def get_classes():
    """
    Retrieves class names from the 'classname' table in the database.

    Args:
        attribute (str): The attribute to retrieve data from.
        table (str): The name of the table to retrieve data from.

    Returns:
        list: A list of class names.
    """
    attribute = "name"
    table = "classname"
    return get_data(attribute, table)

def get_races():
    """
    Retrieves race names from the 'race' table in the database.

    Args:
        attribute (str): The attribute to retrieve data from.
        table (str): The name of the table to retrieve data from.

    Returns:
        list: A list of race names.
    """
    attribute = "name"
    table = "race"
    return get_data(attribute, table)

def get_tasks():
    """
    Retrieves task descriptions from the 'task' table in the database.

    Args:
        attribute (str): All attributes of table.
            [0] -> ID
            [1] -> Description
            [2] -> XP
            [3] -> Expiration Date
        table (str): The name of the table to retrieve data from.

    Returns:
        list: A list of task descriptions.
    """

    attribute = "*"
    table = "task"
    return get_data(attribute, table)