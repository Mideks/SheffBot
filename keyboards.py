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

    builder.button(text="🥘 Отлично, как готовить?",
                   callback_data=NavigateButton(location=NavigateButtonLocation.RecipeStages))
    builder.button(text="🎲 Другой рецепт",
                   callback_data=NavigateButton(location=NavigateButtonLocation.NewSearch))
    builder.button(text="🥕 Другие продукты",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SearchByProductList, data='new'))

    builder.adjust(1)
    return builder.as_markup()


def get_stages_menu_keyboard(current_stage: int, stage_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    navigation = InlineKeyboardBuilder()
    if current_stage != 1:
        builder.button(
            text=f"⬅️ Шаг {current_stage - 1}",
            callback_data=NavigateButton(location=NavigateButtonLocation.RecipeStage, data=str(current_stage - 1)))
    if current_stage != stage_count:
        builder.button(
            text=f"Шаг {current_stage + 1} ➡️",
            callback_data=NavigateButton(location=NavigateButtonLocation.RecipeStage, data=str(current_stage + 1)))

    builder.attach(navigation)
    builder.button(text="🔙 Назад к рецепту",
                   callback_data=NavigateButton(location=NavigateButtonLocation.RecipeCard))
    if current_stage != 1 and current_stage != stage_count:
        builder.adjust(2, 1)
    else:
        builder.adjust(1, 1)

    return builder.as_markup()