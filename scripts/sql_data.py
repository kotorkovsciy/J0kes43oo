from sqlite3 import connect


class Database:
    def __init__(self, db_file):
        self.connection = connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.execute("""CREATE TABLE IF NOT EXISTS jokes (
                                user_id INTEGER,
                                joke TEXT,
                                author TEXT
                            )""")
        self.connection.execute("""CREATE TABLE IF NOT EXISTS newJokes (
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
            self.cursor.executemany(
                "INSERT INTO jokes (user_id,joke,author) VALUES (?, ?, ?)", moreShows)
            self.cursor.executemany(
                "INSERT INTO newJokes (user_id,joke,author) VALUES (?, ?, ?)", moreShows)

    async def randomJoke(self):
        """Отправка рандомной шутки от пользователей бота"""
        with self.connection:
            records = self.cursor.execute(
                "SELECT joke, author FROM jokes ORDER BY RANDOM() LIMIT 1").fetchmany(1)
        if not bool(len(records)):
            return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
        for row in records:
            return f'{row[0]} Автор: {row[1]}'
        

    async def myJoke(self, user_id):
        """Просмотр своих шуток"""
        with self.connection:
            rowid = await self.rowid(user_id)
            records = self.cursor.execute(
                f"SELECT joke, author FROM jokes WHERE user_id = '%s'" % rowid).fetchall()
            msg = ''
        if not bool(len(records)):
            return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
        for row in records:
            msg += f'{row[0]}\n\n'
        return msg

    async def newsJoke(self):
        """Вывод последней шутки"""
        with self.connection:
            records = self.cursor.execute(
                "SELECT * FROM newJokes LIMIT 1").fetchmany(1)
        for row in records:
            return row

    async def deleteOldJoke(self):
        """Удаление старой шутки"""
        with self.connection:
            self.cursor.execute(
                "DELETE FROM newJokes where ROWID = 1")

    async def newsJokesExists(self):
        """Проверка шуток"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT count(*) FROM newJokes").fetchone()[0]
            if result < 1:
                return False
            return True

    async def quantityUsers(self):
        """Количество пользователей"""
        with self.connection:
            return self.cursor.execute("SELECT count(*) FROM users").fetchone()[0]

    async def quantityJokesUser(self, user_id):
        """Количество шуток у пользователя"""
        with self.connection:
            rowid = await self.rowid(user_id)
            return self.cursor.execute("SELECT count(*) FROM jokes WHERE user_id = ?", (rowid,)).fetchone()[0]

    async def userExists(self, user_id):
        """Проверка пользовотеля"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    async def userAdd(self, user_id):
        """Добавление пользователя"""
        with self.connection:
            self.cursor.execute(
                "INSERT INTO users (user_id) VALUES (?)", (user_id,))

    async def infoId(self, id):
        """Просмотр пользователя"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE ROWID = ?", (id,)).fetchone()[0]

    async def rowid(self, user_id):
        """Поиск пользователя"""
        with self.connection:
            if not await self.userExists(user_id):
                await self.userAdd(user_id)
            return self.cursor.execute(
                f"SELECT rowid FROM users WHERE user_id = '%s'" % user_id).fetchone()[0]

    async def deleteJokes(self):
        """Удаление всех шуток"""
        with self.connection:
            self.cursor.execute("DELETE FROM jokes")
            self.cursor.execute("DELETE FROM newJokes")

    async def deleteJokesUser(self, user_id):
        """Удаление своих шуток"""
        with self.connection:
            rowid = await self.rowid(user_id)
            self.cursor.execute(
                f"DELETE FROM jokes WHERE user_id = '%s'" % rowid)
