import sqlite3


class DataBase:
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO Users (user_id) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            r = self.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchall()
            return r

    def set_nickname(self, user_id, nickname):
        if self.user_exists(user_id):
            with self.connection:
                return self.cursor.execute("UPDATE Users SET nickname = ? WHERE user_id = ?",
                                           (nickname, user_id))

    def add_count(self, user_id, count, type: str):
        with self.connection:
            current = self.cursor.execute(f"SELECT {type} FROM Users WHERE user_id = ?",
                                          (user_id,)).fetchall()[0][0]
            return self.cursor.execute(f"UPDATE Users SET {type} = ? WHERE user_id = ?",
                                       (int(current) + count, user_id))


if __name__ == '__main__':
    db = DataBase('database_info.db')
    if not db.user_exists(123456789):
        db.add_user(123456789)

    db.set_nickname(123456789, 'first_name')
    db.add_count(123456789, 10, 'count_of_all_answers')
    db.add_count(123456789, 2, 'count_of_quizes')
    db.add_count(123456789, 5, 'count_of_cor_answers')
