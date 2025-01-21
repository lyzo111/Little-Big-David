from src.database.database import Database

db = Database()

def get_classes_and_races():
    connection = db.create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM classname")
    classes = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM race")
    races = [row[0] for row in cursor.fetchall()]

    connection.close()
    return classes, races

