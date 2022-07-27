from pyjokes import get_joke
from googletrans import Translator
from random import randint
from bs4 import BeautifulSoup
from asyncinit import asyncinit
from aiohttp import ClientSession


@asyncinit
class getAnekdot:
    async def __init__(self):
        pass

    async def getAnekdot(self):
        match randint(1, 2):
            case 1:
                return await self.Anekdot1()
            case 2:
                return await self.Anekdot2()

    async def Anekdot1(self):
        translator = Translator()
        joke = get_joke()
        result = translator.translate(str(joke), dest='ru')
        return result.text

    async def Anekdot2(self):
        async with ClientSession() as session:
            async with session.get('http://anecdotica.ru/') as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                result = soup.find_all('div', class_='item_text')[0]
                return result.text
