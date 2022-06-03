import sqlite3 as sql


class Database:
    def __init__(self, db_file):
        self.connection = sql.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.execute("""CREATE TABLE IF NOT EXISTS joker (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                joke TEXT,
                                author TEXT,
                                user_id TEXT
                            )""")
        self.connection.execute("""CREATE TABLE IF NOT EXISTS users (
                                user_id TEXT 
                            )""")

    async def record(self, joke, author, user_id):
        with self.connection:
            moreShows = [(joke, author, user_id)]
            return self.cursor.executemany("INSERT INTO joker (joke,author,user_id) VALUES (?, ?, ?)", moreShows)

    async def send_u(self):
        with self.connection:
            records = self.cursor.execute("SELECT joke, author FROM joker ORDER BY RANDOM() LIMIT 1").fetchall()
        for row in records:
            return f'{row[0]} Автор: {row[1]}'

    async def my_joke(self, user_id):
        with self.connection:
            records = self.cursor.execute(f"SELECT joke FROM joker WHERE user_id = '%s'" % user_id).fetchall()
            msg = ''
        for row in records:
            msg += f'{row[0]}\n\n'
        return msg

    async def delet_jokes(self, user_id):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM joker WHERE user_id = '%s'" % user_id)
    
    async def quantityJokes(self):
        with self.connection:
            return self.cursor.execute("SELECT count(*) FROM joker").fetchall()

    async def quantityUsers(self):
        with self.connection:
            return self.cursor.execute("SELECT count(*) FROM users").fetchall()
    
    async def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    async def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    async def info_id(self, id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE ROWID = ?", (id,))

    async def delete_jokes(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM joker")

    async def quantityJokesUser(self, id):
        with self.connection:
            return self.cursor.execute("SELECT count() FROM joker WHERE user_id = ?", (id,))
