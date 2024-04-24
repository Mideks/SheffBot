from aiogram.fsm.state import StatesGroup, State


class Search(StatesGroup):
    waiting_food_list = State()

