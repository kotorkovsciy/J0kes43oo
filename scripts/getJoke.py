from pyjokes import get_joke
from googletrans import Translator
from random import randint
from requests import get
from bs4 import BeautifulSoup


async def getAnekdot():
    fuck = randint(1, 2)
    match fuck:
        case 1:
            return await Anekdot1()
        case 2:
            return await Anekdot2()


async def Anekdot1():
    translator = Translator()
    joke = get_joke()
    result = translator.translate(str(joke), dest='ru')
    return result.text


async def Anekdot2():
    url = 'http://anecdotica.ru/'
    response = get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find_all('div', class_='item_text')[0]
    return result.text
