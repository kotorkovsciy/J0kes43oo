from unittest import IsolatedAsyncioTestCase
from scripts import AdminDatabase, NotificationsDatabase, JokesDatabase


class Testing(AdminDatabase, NotificationsDatabase, JokesDatabase):
    def __init__(self, database):
        super(Testing, self).__init__(database)

    async def clearDatabase(self):
        """Полная очистка бд"""
        self._open()
        self._cursor.execute(
            f"DROP TABLE users")
        self._cursor.execute(
            f"DROP TABLE admins")
        self._cursor.execute(
            f"DROP TABLE jokes")
        self._close()


class TestDatabase(IsolatedAsyncioTestCase):
    """
    Warning, when testing the database, a complete check is performed
    """

    def setUp(self):
        self.Testing = Testing("test")

    async def test_ReadWriteJokesDatabase(self):
        await self.Testing.deleteJokes()
        await self.Testing.recordJoke("Meow", "Cat", 1)
        self.assertEqual(await self.Testing.randomJoke(), 'Meow Автор: Cat')
        self.assertEqual(await self.Testing.myJoke(1), 'Meow\n\n')
        self.assertEqual(await self.Testing.quantityJokesUser(1), 1)
        await self.Testing.deleteJokesUser(1)
        self.assertEqual(await self.Testing.quantityJokesUser(1), 0)
        await self.Testing.clearDatabase()

    async def test_ReadWriteNotificationsDatabase(self):
        await self.Testing.deleteJokes()
        self.assertEqual(await self.Testing.newsJokesExists(), 0)
        await self.Testing.recordJoke("Meow", "Cat", 1)
        self.assertEqual(await self.Testing.newsJokesExists(), 1)
        self.assertEqual(await self.Testing.quantityUsers(), 1)
        row = await self.Testing.newsJoke()
        self.assertEqual(row["user_id"], 1)
        self.assertEqual(row["joke"], "Meow")
        self.assertEqual(row["author"], "Cat")
        self.assertEqual(await self.Testing.infoId(1), 1)
        await self.Testing.deleteOldJoke()
        self.assertEqual(await self.Testing.newsJokesExists(), 0)
        await self.Testing.clearDatabase()

    async def test_ReadWriteAdminDatabase(self):
        await self.Testing.recordJoke("Meow", "Cat", 1)
        await self.Testing.deleteJokes()
        self.assertEqual(await self.Testing.quantityJokesUser(1), 0)
        self.assertEqual(await self.Testing.newsJokesExists(), 0)
        self.assertEqual(await self.Testing.adminExists(1), 0)
        self.assertEqual(await self.Testing.nameAdminExists("Cat"), 0)
        await self.Testing.adminAdd(1, "Cat", 1)
        self.assertEqual(await self.Testing.nameAdminExists("Cat"), 1)
        self.assertEqual(await self.Testing.allAdmins(), "id: 1, name: Cat, inviting: 1\n\n")
        await self.Testing.adminDel(1)
        self.assertEqual(await self.Testing.adminExists(1), 0)
        self.assertEqual(await self.Testing.allAdmins(), "Нету админов")
        await self.Testing.clearDatabase()
