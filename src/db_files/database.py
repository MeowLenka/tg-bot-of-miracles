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

    def get_count(self, user_id, t: str):
        with self.connection:
            current = self.cursor.execute(f"SELECT {t} FROM Users WHERE user_id = ?",
                                          (user_id,)).fetchall()[0][0]
            return current

    def update_count(self, user_id, count, t: str):
        with self.connection:
            current = self.cursor.execute(f"SELECT {t} FROM Users WHERE user_id = ?",
                                          (user_id,)).fetchall()[0][0]
            return self.cursor.execute(f"UPDATE Users SET {t} = ? WHERE user_id = ?",
                                       (int(current) + count, user_id))


if __name__ == '__main__':
    db = DataBase('database_info.db')
    if not db.user_exists(123456789):
        db.add_user(123456789)

    db.update_count(123456789, 10, 'count_of_all_answers')
    db.update_count(123456789, 2, 'count_of_quizes')
    db.update_count(123456789, 5, 'count_of_cor_answers')
