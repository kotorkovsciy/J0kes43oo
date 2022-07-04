from pyjokes import get_joke
from googletrans import Translator


def getanekdot():
    translator = Translator()
    joke = get_joke()
    result = translator.translate(str(joke), dest='ru')
    return result.text
