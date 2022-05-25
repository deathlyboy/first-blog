import sqlite3


class SQlighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE email = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, email, password):
        """Добавляем новый акаунт"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`email`, `password`) VALUES(?,?)", (email, password))

    def get_password(self, email):
        """Возвращяем пароль"""
        with self.connection:
            for i in self.cursor.execute("SELECT password FROM users WHERE email = ?", (email,)).fetchall():
                for v in i:
                    return str(v)

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

    def write_data(self, title, text, teg, preview):
        """Записываем данные поста"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `post` (`title`, `text`, `teg`, `preview`) VALUES(?,?,?,?)",
                                       (title, text, teg, preview))

    def delete_post(self, title):
        with self.connection:
            self.cursor.execute("DELETE FROM 'post' WHERE title=?", (title,))

    def title_exists(self, title):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `post` WHERE title = ?', (title,)).fetchall()
            return bool(len(result))

    def all_title_and_preview(self):
        with self.connection:
            return self.cursor.execute("SELECT title, preview FROM post").fetchall()

    def text(self, title):
        with self.connection:
            return self.cursor.execute("SELECT text FROM post WHERE title = ?", (title,)).fetchall()[0][0]

    def teg(self, title):
        with self.connection:
            return self.cursor.execute("SELECT teg FROM post WHERE title = ?", (title,)).fetchall()

    def preview(self, title):
        with self.connection:
            return self.cursor.execute("SELECT preview FROM post WHERE title = ?", (title,)).fetchall()
