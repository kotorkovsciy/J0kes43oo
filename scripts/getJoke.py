import pyjokes
from googletrans import Translator 


def getanekdot():
    translator = Translator()
    joke = pyjokes.get_joke()
    result = translator.translate(str(joke), dest='ru')
    return result.text
