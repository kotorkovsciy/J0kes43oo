from sqlite3 import connect


class Database:
    def __init__(self, db_file):
        self.connection = connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.execute("""CREATE TABLE IF NOT EXISTS joker (
                                user_id INTEGER,
                                joke TEXT,
                                author TEXT
                            )""")
        self.connection.execute("""CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER 
                            )""")

    async def recordJoke(self, joke, author, user_id):
        """Запись шутки"""
        with self.connection:
            rowid = await self.rowid(user_id)
            moreShows = [(rowid, joke, author)]
            return self.cursor.executemany("INSERT INTO joker (user_id,joke,author) VALUES (?, ?, ?)", moreShows)

    async def randomJoke(self):
        """Отправка рандомной шутки от пользователей бота"""
        with self.connection:
            records = self.cursor.execute(
                "SELECT joke, author FROM joker ORDER BY RANDOM() LIMIT 1").fetchall()
        for row in records:
            return f'{row[0]} Автор: {row[1]}'

    async def myJoke(self, user_id):
        """Просмотр своих шуток"""
        with self.connection:
            records = self.cursor.execute(
                f"SELECT joker.joke, joker.author FROM users, joker WHERE users.user_id = '%s'" % user_id).fetchall()
            msg = ''
        for row in records:
            msg += f'{row[0]}\n\n'
        return msg

    async def newsJoke(self):
        """Вывод последней шутки"""
        with self.connection:
            records = self.cursor.execute(
                "SELECT * FROM joker ORDER BY ROWID DESC LIMIT 1")
        for row in records:
            return row

    async def quantityJokes(self):
        """Количество всех шуток"""
        with self.connection:
            return self.cursor.execute("SELECT count(*) FROM joker").fetchmany(1)[0][0]

    async def quantityUsers(self):
        """Количество пользователей"""
        with self.connection:
            return self.cursor.execute("SELECT count(*) FROM users").fetchmany(1)[0][0]

    async def quantityJokesUser(self, user_id):
        """Количество шуток у пользователя"""
        with self.connection:
            rowid = await self.rowid(user_id)
            return self.cursor.execute("SELECT count() FROM joker WHERE user_id = ?", (rowid,))

    async def userExists(self, user_id):
        """Проверка пользовотеля"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    async def userAdd(self, user_id):
        """Добавление пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    async def infoId(self, id):
        """Просмотр пользователя"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE ROWID = ?", (id,)).fetchmany(1)[0][0]

    async def rowid(self, user_id):
        """Поиск пользователя"""
        return self.cursor.execute(
            f"SELECT rowid FROM users WHERE user_id = '%s'" % user_id).fetchmany(1)[0][0]

    async def deleteJokes(self):
        """Удаление всех шуток"""
        with self.connection:
            return self.cursor.execute("DELETE FROM joker")

    async def deleteJokesUser(self, user_id):
        """Удаление своих шуток"""
        with self.connection:
            rowid = await self.rowid(user_id)
            return self.cursor.execute(f"DELETE FROM joker WHERE user_id = '%s'" % rowid)
