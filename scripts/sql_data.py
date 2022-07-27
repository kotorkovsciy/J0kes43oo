from aiosqlite import connect, Row
from asyncinit import asyncinit


@asyncinit
class Database():
    async def __init__(self, db_file):
        self.db_file = db_file
        async with connect(self.db_file) as db:
            db.row_factory = Row
            await db.execute("""CREATE TABLE IF NOT EXISTS jokes (
                                user_id INTEGER,
                                joke TEXT,
                                author TEXT
                            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS newJokes (
                                user_id INTEGER,
                                joke TEXT,
                                author TEXT
                            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER 
                            )""")

    async def recordJoke(self, joke, author, user_id):
        """Запись шутки"""
        async with connect(self.db_file) as db:
            rowid = await self.rowid(user_id)
            moreShows = [(rowid, joke, author)]
            await db.executemany(
                "INSERT INTO jokes (user_id,joke,author) VALUES (?, ?, ?)", moreShows)
            await db.executemany(
                "INSERT INTO newJokes (user_id,joke,author) VALUES (?, ?, ?)", moreShows)
            await db.commit()

    async def randomJoke(self):
        """Отправка рандомной шутки от пользователей бота"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute(
                    "SELECT joke, author FROM jokes ORDER BY RANDOM() LIMIT 1") as cursor:
                async for row in cursor:
                    if not bool(len(row)):
                        return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
                    return f'{row["joke"]} Автор: {row["author"]}'

    async def myJoke(self, user_id):
        """Просмотр своих шуток"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            rowid = await self.rowid(user_id)
            async with db.execute(
                    f"SELECT joke, author FROM jokes WHERE user_id = '%s'" % rowid) as cursor:
                msg = ''
                async for row in cursor:
                    msg += f'{row["joke"]}\n\n'
        if not bool(len(msg)):
            return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
        return msg

    async def newsJoke(self):
        """Вывод последней шутки"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute(
                    "SELECT * FROM newJokes LIMIT 1") as cursor:
                async for row in cursor:
                    return row

    async def deleteOldJoke(self):
        """Удаление старой шутки"""
        async with connect(self.db_file) as db:
            await db.execute(
                "DELETE FROM newJokes where ROWID = 1")
            await db.commit()

    async def newsJokesExists(self):
        """Проверка шуток"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute(
                    "SELECT count(*) FROM newJokes") as cursor:
                async for row in cursor:
                    if row["count(*)"] < 1:
                        return False
                    return True

    async def quantityUsers(self):
        """Количество пользователей"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute("SELECT count(*) FROM users") as cursor:
                async for row in cursor:
                    return row["count(*)"]

    async def quantityJokesUser(self, user_id):
        """Количество шуток у пользователя"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            rowid = await self.rowid(user_id)
            async with db.execute("SELECT count(*) FROM jokes WHERE user_id = ?", (rowid,)) as cursor:
                async for row in cursor:
                    return row["count(*)"]

    async def userExists(self, user_id):
        """Проверка пользовотеля"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute(
                    "SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                async for row in cursor:
                    return bool(len(row))

    async def userAdd(self, user_id):
        """Добавление пользователя"""
        async with connect(self.db_file) as db:
            await db.execute(
                "INSERT INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def infoId(self, id):
        """Просмотр пользователя"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            async with db.execute("SELECT * FROM users WHERE ROWID = ?", (id,)) as cursor:
                async for row in cursor:
                    return row["user_id"]

    async def rowid(self, user_id):
        """Поиск пользователя"""
        async with connect(self.db_file) as db:
            db.row_factory = Row
            if not await self.userExists(user_id):
                await self.userAdd(user_id)
            async with db.execute(
                    f"SELECT rowid FROM users WHERE user_id = '%s'" % user_id) as cursor:
                async for row in cursor:
                    return row["rowid"]

    async def deleteJokes(self):
        """Удаление всех шуток"""
        async with connect(self.db_file) as db:
            await db.executescript("""DELETE FROM jokes;
                                        DELETE FROM newJokes
                                    """)
            await db.commit()

    async def deleteJokesUser(self, user_id):
        """Удаление своих шуток"""
        async with connect(self.db_file) as db:
            rowid = await self.rowid(user_id)
            await db.execute(
                f"DELETE FROM jokes WHERE user_id = '%s'" % rowid)
            await db.commit()

    async def dump(self, user_id):
        """Дамп бд"""
        async with connect(self.db_file) as db:
            with open(f"{user_id}.sql", "w", encoding='utf 8') as file:
                async for sql in db.iterdump():
                    file.write(sql)
