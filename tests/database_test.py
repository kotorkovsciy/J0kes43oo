from unittest import IsolatedAsyncioTestCase
from scripts import Database, AdminDatabase, NotificationsDatabase, JokesDatabase


class TestDatabase(IsolatedAsyncioTestCase):
    """
    Warning, when testing the database, a complete check is performed
    """
    def setUp(self):
        self.Database = Database("test")
        self.AdminDatabase = AdminDatabase("test")
        self.NotificationsDatabase = NotificationsDatabase("test")
        self.JokesDatabase = JokesDatabase("test")

    async def test_ReadWriteJokesDatabase(self):
        await self.AdminDatabase.deleteJokes()
        await self.JokesDatabase.recordJoke("Meow", "Cat", 1)
        self.assertEqual(await self.JokesDatabase.randomJoke(), 'Meow Автор: Cat')
        self.assertEqual(await self.JokesDatabase.myJoke(1), 'Meow\n\n')
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 1)
        await self.JokesDatabase.deleteJokesUser(1)
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 0)
        await self.AdminDatabase.clearDatabase()

    async def test_ReadWriteNotificationsDatabase(self):
        await self.AdminDatabase.deleteJokes()
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
        await self.AdminDatabase.clearDatabase()

    async def test_ReadWriteAdminDatabase(self):
        await self.JokesDatabase.recordJoke("Meow", "Cat", 1)
        await self.AdminDatabase.deleteJokes()
        self.assertEqual(await self.JokesDatabase.quantityJokesUser(1), 0)
        self.assertEqual(await self.NotificationsDatabase.newsJokesExists(), 0)
        self.assertEqual(await self.AdminDatabase.adminExists(1), 0)
        self.assertEqual(await self.AdminDatabase.nameAdminExists("Cat"), 0)
        await self.AdminDatabase.adminAdd(1, "Cat", 1)
        self.assertEqual(await self.AdminDatabase.nameAdminExists("Cat"), 1)
        self.assertEqual(await self.AdminDatabase.allAdmins(), "id: 1, name: Cat, inviting: 1\n\n")
        await self.AdminDatabase.adminDel(1)
        self.assertEqual(await self.AdminDatabase.adminExists(1), 0)
        self.assertEqual(await self.AdminDatabase.allAdmins(), "Нету админов")
        await self.AdminDatabase.clearDatabase()
