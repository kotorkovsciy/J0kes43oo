from unittest import main, IsolatedAsyncioTestCase
from scripts import Database, AdminDatabase, NotificationsDatabase, JokesDatabase
from asyncio import run
from os import remove


class TestDatabase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.Database = run(Database("test.db"))
        self.AdminDatabase = run(AdminDatabase("test.db"))
        self.NotificationsDatabase = run(NotificationsDatabase("test.db"))
        self.JokesDatabase = run(JokesDatabase("test.db"))

    def __del__(self):
        remove("test.db")

    async def test_ReadWriteDatabase(self):
        self.assertEqual(await self.Database.userExists(1), None)
        await self.Database.userAdd(1)
        self.assertEqual(await self.Database.userExists(1), 1)

    async def test_ReadWriteJokesDatabase(self):
        await self.JokesDatabase.recordJoke("Meow", "Cat", 1)
        self.assertEqual(await self.JokesDatabase.randomJoke(), 'Meow Автор: Cat')
        self.assertEqual(await self.JokesDatabase.myJoke(1), 'Meow\n\n')
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 1)
        await self.JokesDatabase.deleteJokesUser(1)
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 0)

    async def test_ReadWriteNotificationsDatabase(self):
        self.assertEqual(await self.NotificationsDatabase.newsJokesExists(), 0)
        await self.JokesDatabase.recordJoke("Meow", "Cat", 1)
        self.assertEqual(await self.NotificationsDatabase.newsJokesExists(), 1)
        self.assertEqual(await self.NotificationsDatabase.quantityUsers(), 1)
        row = await self.NotificationsDatabase.newsJoke()
        self.assertEqual(row["user_id"], 1)
        self.assertEqual(row["joke"], "Meow")
        self.assertEqual(row["author"], "Cat")
        self.assertEqual(await self.NotificationsDatabase.infoId(1), 1)
        await self.NotificationsDatabase.deleteOldJoke()
        self.assertEqual(await self.NotificationsDatabase.newsJokesExists(), 0)

    async def test_ReadWriteAdminDatabase(self):
        await self.JokesDatabase.recordJoke("Meow", "Cat", 1)
        await self.AdminDatabase.deleteJokes()
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 0)
        self.assertEqual(await self.NotificationsDatabase.newsJokesExists(), 0)
        self.assertEqual(await self.AdminDatabase.adminExists(1), None)
        self.assertEqual(await self.AdminDatabase.nameAdminExists("Cat"), None)
        await self.AdminDatabase.adminAdd(1, "Cat", 1)
        self.assertEqual(await self.AdminDatabase.nameAdminExists("Cat"), 1)
        self.assertEqual(await self.AdminDatabase.allAdmins(), "id: 1, name: Cat, inviting: 1\n\n")
        await self.AdminDatabase.adminDel(1)
        self.assertEqual(await self.AdminDatabase.adminExists(1), None)
        self.assertEqual(await self.AdminDatabase.allAdmins(), "Нету админов")
