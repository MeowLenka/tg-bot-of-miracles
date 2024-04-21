import sqlite3


class DataBase:
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO Users(user_id) VALUE (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            r = self.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchall()
            return r

    def set_nickname(self, user_id, nickname):
        if self.user_exists(user_id):
            with self.connection:
                r = self.cursor.execute("UPDATE Users SET nickname = ? WHERE user_id = ?",
                                        (nickname, user_id))
                return r
