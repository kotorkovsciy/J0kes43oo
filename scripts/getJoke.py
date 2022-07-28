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
        return await eval(f"self.Anekdot{randint(1, 2)}")()

    async def Anekdot1(self):
        translator = Translator()
        joke = get_joke()
        result = translator.translate(str(joke), dest='ru')
        return result.text

    async def Anekdot2(self):
        async with ClientSession(trust_env=True) as session:
            async with session.get('http://anecdotica.ru/', ssl=False) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                result = soup.find_all('div', class_='item_text')[0]
                return result.text
