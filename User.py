import Database

class user:
    def __init__(self):
        self.db = Database()

    def createUser(self,name, race, roll):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        cursor. execute("INSERT INTO users (name,race,roll) VALUES(?,?)", name,race,roll)

        connection.commit()
        connection.close()

        print(f"User {name} wurde erstellt.")

        def read_user_by_id(self, user_id):
            connection = self.db.create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            users = cursor.fetchall()

            connection.close()

            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]}, Race: {user[2]}, Roll: {user[3]}")

            def update_user(self, user_Id, new_name, new_race, new_roll):
                connection = self.db.create_connection();
                cursor = connection.cursor()

                cursor.execute("UPDATE users SET name = ?, race = ?, roll = ? WHERE id = ?",(new_name, new_race, new_roll, user_Id))

                connection.commit()
                connection.close()

                def delete_user(self, user_Id):
                    connection = self.db.create_connection()
                    cursor = connection.cursor()

                    cursor.execute("DELETE FROM users WHERE id = ?", (user_Id,))

                    print(f"User {user_Id} wurde gelöscht.")