from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import NavigateButton, NavigateButtonLocation


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="👀 Давай начнём!",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SearchByProductList))

    return builder.as_markup()


def get_food_list_entering_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Да, всё верно",
                   callback_data=NavigateButton(location=NavigateButtonLocation.StartSearch))

    return builder.as_markup()


def get_waiting_for_food_list_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔎 Продолжить без списка",
                   callback_data=NavigateButton(location=NavigateButtonLocation.StartSearch))

    return builder.as_markup()


def get_search_result_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🎲 Другой рецепт",
                   callback_data=NavigateButton(location=NavigateButtonLocation.NewSearch))
    builder.button(text="🥕 Другие продукты",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SearchByProductList, data='new'))

    builder.adjust(1)
    return builder.as_markup()
