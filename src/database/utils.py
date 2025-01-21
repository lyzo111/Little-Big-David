from src.database.database import Database

db = Database()


def get_data(table_name):
    query = f"SELECT name FROM {table_name}"
    connection = db.create_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    data = [row[0] for row in cursor.fetchall()]
    connection.close()
    return data


def get_classes():
    return get_data("classname")


def get_races():
    return get_data("race")


def get_tasks():
    return get_data("task")
