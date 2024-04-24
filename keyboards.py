from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import NavigateButton, NavigateButtonLocation


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔍👀Давай начнём!",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    return builder.as_markup()
