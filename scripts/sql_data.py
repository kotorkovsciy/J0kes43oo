from os import getenv
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UndefinedTable


load_dotenv()


class PostDatabase:
    __user = None
    __host = None
    __password = None
    __port = None
    __connection = None

    def __init__(self, database):
        self.__user = getenv("POSTGRES_USER")
        self.__host = getenv("POSTGRES_HOST")
        self.__password = getenv("POSTGRES_PASSWORD")
        self.__port = getenv("POSTGRES_PORT")
        self.database = database.lower()

    def __open__(self):
        self.__connection = connect(user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)
        self.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.__connection.cursor(cursor_factory=RealDictCursor)

    def __close__(self):
        self.__connection.close()


class Database(PostDatabase):
    def __init__(self, database):
        super(Database, self).__init__(database)
        self.__open__()
        self.cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.database}'")
        exists = self.cursor.fetchone()
        if not exists:
            self.cursor.execute(f'CREATE DATABASE {self.database}')
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                id BIGSERIAL NOT NULL PRIMARY KEY,
                                user_id BIGINT NOT NULL
                            )""")
        self.__close__()

    async def userExists(self, user_id):
        """Проверка пользовотеля"""
        self.__open__()
        self.cursor.execute(
            f"SELECT * FROM users WHERE user_id = {user_id}")
        result = self.cursor.fetchmany(1)
        self.__close__()
        if not bool(len(result)):
            await self.userAdd(user_id)

    async def userAdd(self, user_id):
        """Добавление пользователя"""
        self.__open__()
        self.cursor.execute(
            f"INSERT INTO users (user_id) VALUES ({user_id})")
        self.__close__()

    async def rowid(self, user_id):
        """Поиск пользователя"""
        await self.userExists(user_id)
        self.__open__()
        self.cursor.execute(
            f"SELECT row_number() over()  FROM users WHERE user_id = {user_id}")
        result = self.cursor.fetchone()["row_number"]
        self.__close__()
        return result


class JokesDatabase(Database):
    def __init__(self, database):
        super(JokesDatabase, self).__init__(database)
        self.__open__()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS jokes (
                                    user_id INTEGER,
                                    joke TEXT,
                                    author TEXT
                                )""")
        self.__close__()

    async def recordJoke(self, joke, author, user_id):
        """Запись шутки"""
        rowid = await self.rowid(user_id)
        self.__open__()
        self.cursor.execute(
            f"INSERT INTO jokes (user_id,joke,author) VALUES ({rowid}, \'{joke}\', \'{author}\')")
        self.cursor.execute(
            f"INSERT INTO newJokes (user_id,joke,author) VALUES ({rowid}, \'{joke}\', \'{author}\')")
        self.__close__()

    async def randomJoke(self):
        """Отправка рандомной шутки от пользователей бота"""
        self.__open__()
        self.cursor.execute(
            "SELECT joke, author FROM jokes ORDER BY RANDOM() LIMIT 1")
        records = self.cursor.fetchmany(1)
        self.__close__()
        if not bool(len(records)):
            return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
        for row in records:
            return f'{row["joke"]} Автор: {row["author"]}'

    async def myJoke(self, user_id):
        """Просмотр своих шуток"""
        rowid = await self.rowid(user_id)
        self.__open__()
        self.cursor.execute(
            f"SELECT joke, author FROM jokes WHERE user_id = '%s'" % rowid)
        records = self.cursor.fetchall()
        self.__close__()
        msg = ''
        if not bool(len(records)):
            return "Нету шуток 😞, но ты можешь записать свою шутку 😉"
        for row in records:
            msg += f'{row["joke"]}\n\n'
        return msg

    async def quantityJokesUser(self, user_id):
        """Количество шуток у пользователя"""
        rowid = await self.rowid(user_id)
        self.__open__()
        self.cursor.execute(
            f"SELECT COUNT(*) FROM jokes WHERE user_id = '%s'" % rowid)
        result = self.cursor.fetchone()["count"]
        self.__close__()
        return result

    async def deleteJokesUser(self, user_id):
        """Удаление своих шуток"""
        rowid = await self.rowid(user_id)
        self.__open__()
        self.cursor.execute(
            f"DELETE FROM jokes WHERE user_id = '%s'" % rowid)
        self.__close__()


class NotificationsDatabase(Database):
    def __init__(self, database):
        super(NotificationsDatabase, self).__init__(database)
        self.__open__()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS newJokes (
                                user_id INTEGER,
                                joke TEXT,
                                author TEXT
                            )""")
        self.__close__()

    def __del__(self):
        self.__open__()
        try:
            self.cursor.execute("DELETE FROM newJokes")
        except UndefinedTable:
            raise Exception("Таблицы newJokes не существует")
        self.__close__()

    async def newsJokesExists(self):
        """Проверка шуток"""
        self.__open__()
        self.cursor.execute(
            "SELECT count(*) FROM newJokes")
        result = self.cursor.fetchone()["count"]
        self.__close__()
        if result < 1:
            return False
        return True

    async def quantityUsers(self):
        """Количество пользователей"""
        self.__open__()
        self.cursor.execute("SELECT count(*) FROM users")
        result = self.cursor.fetchone()["count"]
        self.__close__()
        return result

    async def newsJoke(self):
        """Вывод последней шутки"""
        self.__open__()
        self.cursor.execute(
            "SELECT * FROM newJokes LIMIT 1")
        records = self.cursor.fetchmany(1)
        self.__close__()
        for row in records:
            return row

    async def infoId(self, id):
        """Просмотр пользователя"""
        self.__open__()
        self.cursor.execute(
            f"SELECT * FROM users WHERE id = {id}")
        result = self.cursor.fetchone()["user_id"]
        self.__close__()
        return result

    async def deleteOldJoke(self):
        """Удаление старой шутки"""
        self.__open__()
        self.cursor.execute(
            "DELETE FROM newJokes WHERE ctid IN (SELECT ctid FROM newJokes LIMIT 1)")
        self.__close__()


class AdminDatabase(Database):
    def __init__(self, database):
        super(AdminDatabase, self).__init__(database)
        self.__open__()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
                                user_id BIGINT,
                                name TEXT,
                                inviting BIGINT
                            )""")
        self.__close__()

    async def deleteJokes(self):
        """Удаление всех шуток"""
        self.__open__()
        self.cursor.execute("DELETE FROM jokes")
        self.cursor.execute("DELETE FROM newJokes")
        self.__close__()

    async def dump(self, user_id):
        """Дамп бд"""
        self.__open__()
        self.cursor.execute('SELECT * FROM users')
        with open(f"sql\dump_users_{user_id}.sql", "w", encoding='utf 8') as file:
            for row in self.cursor:
                file.write("INSERT INTO users VALUES (" + str(row) + ");")

        self.cursor.execute('SELECT * FROM jokes')
        with open(f"sql\dump_jokes_{user_id}.sql", "w", encoding='utf 8') as file:
            for row in self.cursor:
                file.write("INSERT INTO jokes VALUES (" + str(row) + ");")

        self.cursor.execute('SELECT * FROM admins')
        with open(f"sql\dump_admins_{user_id}.sql", "w", encoding='utf 8') as file:
            for row in self.cursor:
                file.write("INSERT INTO admins VALUES (" + str(row) + ");")
        self.__close__()

    async def adminExists(self, user_id):
        """Проверка админа"""
        self.__open__()
        self.cursor.execute(
            f"SELECT * FROM admins WHERE user_id = {user_id}")
        result = self.cursor.fetchmany(1)
        self.__close__()
        return bool(len(result))

    async def nameAdminExists(self, name):
        """Проверка имени админа"""
        self.__open__()
        self.cursor.execute(
            f"SELECT * FROM admins WHERE name = \'{name}\'")
        result = self.cursor.fetchmany(1)
        self.__close__()
        return bool(len(result))

    async def adminAdd(self, user_id,  name, inviting):
        """Добавление админа"""
        self.__open__()
        self.cursor.execute(
            f"INSERT INTO admins (user_id, name, inviting) VALUES ({user_id}, \'{name}\', {inviting})")
        self.__close__()

    async def adminDel(self, user_id):
        """Удаление админа"""
        self.__open__()
        self.cursor.execute(
            f"DELETE FROM admins WHERE user_id = '%s'" % user_id)
        self.__close__()

    async def allAdmins(self):
        """Просмотр список админов"""
        self.__open__()
        self.cursor.execute(
            f"SELECT user_id, name, inviting FROM admins")
        records = self.cursor.fetchall()
        msg = ''
        for row in records:
            msg += f'id: {row["user_id"]}, name: {row["name"]}, inviting: {row["inviting"]}\n\n'
        self.__close__()
        if not bool(len(msg)):
            return "Нету админов"
        return msg
