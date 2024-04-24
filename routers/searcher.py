from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import states
import texts
from keyboards import get_menu_keyboard
from callback_data import NavigateButton, NavigateButtonLocation


router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.Search))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(texts.search)
    await state.set_state(states.Search.waiting_food_list)


