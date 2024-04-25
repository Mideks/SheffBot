import os
import random
from asyncio import sleep

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto

import db_functions
import keyboards
import states
import texts
from callback_data import NavigateButton, NavigateButtonLocation
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SearchByProductList))
async def search_handler(callback: CallbackQuery, state: FSMContext, callback_data: NavigateButton) -> None:
    send_as_new = callback_data.data == 'new'
    await send_search_by_product_list_message(callback.message, state, send_as_new)
    await callback.answer()


async def send_search_by_product_list_message(message: Message, state: FSMContext, send_as_new=False):
    if send_as_new:
        bot_message = await message.answer(
            texts.search_by_product_list, reply_markup=keyboards.get_waiting_for_food_list_keyboard())
        await message.delete()
        await state.update_data(bot_message=bot_message)
    else:
        await message.edit_text(
            texts.search_by_product_list, reply_markup=keyboards.get_waiting_for_food_list_keyboard())

    await state.set_state(states.Search.waiting_food_list)
    await state.update_data(search_filters=SearchFilters())


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


async def send_search_result_message(
        message: Message, state: FSMContext, recipe: dict, send_as_new: bool = False):
    ingredients = [
        f"{recipe['name']} - {recipe['quantity']} {recipe['unit']}"
        for recipe in recipe['ingredients']
    ]

    text = texts.search_result.format(
        name=recipe['name'],
        cookingTime=recipe['cookingTime'],
        calories=recipe['calories'],
        ingredients='\n'.join(ingredients)
    )

    photo_path = 'recipes/' + recipe['photo']
    if not os.path.exists(photo_path):
        await message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {photo_path} не существует")
        return

    photo = FSInputFile(photo_path)
    if send_as_new:
        bot_message = await message.answer_photo(
            photo, text, reply_markup=keyboards.get_search_result_keyboard())
        await message.delete()
        await state.update_data(bot_message=bot_message)
    else:
        await message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=keyboards.get_search_result_keyboard()
        )


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(None)
    await send_waiting_message(callback)

    data = await state.get_data()
    recipes: list[dict] = db_functions.search_recipes_by_filters(data['search_filters'])
    random.shuffle(recipes)
    selected_recipe = random.choice(recipes)
    recipes.remove(selected_recipe)
    await state.update_data(search_result=recipes)

    await send_search_result_message(callback.message, state, selected_recipe, True)
    await callback.answer()


async def send_waiting_message(callback):
    await callback.message.edit_text(texts.wait_for_result)
    await callback.message.chat.do('typing')
    await sleep(3)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.NewSearch))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    recipes = data['search_result']
    if len(recipes) == 0:
        await callback.answer('Упс, рецепты кончились!')
        return

    selected_recipe = random.choice(recipes)
    recipes.remove(selected_recipe)
    await state.update_data(search_result=recipes)

    await send_search_result_message(callback.message, state, selected_recipe)
    await callback.answer()


