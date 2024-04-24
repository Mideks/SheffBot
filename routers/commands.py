from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import get_menu_keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        f"👋 Привет, вижу, ты сюда пришёл, чтобы покушать.\n"
        f"👤 Позволь мне помочь тебе с этим.",
        reply_markup=get_menu_keyboard())
