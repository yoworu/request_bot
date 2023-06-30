from string import ascii_letters

from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsValidName(BaseFilter):
    __VALID_CHARS = '\'-'
    __ENG_LETTERS = ascii_letters 
    __RUS_LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    async def __call__(self, message: Message) -> bool:
        text = message.text
        
        if 1 > len(text) > 30:
            return False
        
        current_register = None
        
        if text[0] in self.__ENG_LETTERS:
            current_register = self.__ENG_LETTERS
        elif text[0] in self.__RUS_LETTERS:
            current_register = self.__RUS_LETTERS
        else:
            return False
        
        valid_characters = current_register + self.__VALID_CHARS
        for el in text:
            if el not in valid_characters:
                return False
            
        return True               
