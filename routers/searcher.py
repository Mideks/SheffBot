from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards
import states
import texts
from keyboards import get_menu_keyboard
from callback_data import NavigateButton, NavigateButtonLocation
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.Search))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(texts.search)
    await state.set_state(states.Search.waiting_food_list)
    await state.update_data(bot_message=callback.message)
    await callback.answer()


@router.message(states.Search.waiting_food_list)
async def food_list_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    bot_message: Message = data['bot_message']
    product_list = message.text
    await bot_message.edit_text(
        texts.food_list_entering.format(product_list=product_list),
        reply_markup=keyboards.get_food_list_entering_keyboard()
    )

    products = product_list.split('\n')
    await state.update_data(search_filters=SearchFilters(products))
    await message.delete()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(None)
    await callback.message.edit_text(texts.wait_for_result)
    await callback.message.chat.do('typing')
    await sleep(3)
    await callback.message.edit_text(texts.search_result)
    await callback.answer()
