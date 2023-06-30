from aiogram.fsm.state import State, StatesGroup

class QuestionSG(StatesGroup):
    waiting_for_question = State()
    