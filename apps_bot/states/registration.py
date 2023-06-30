from aiogram.fsm.state import State, StatesGroup

class RegSG(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()

