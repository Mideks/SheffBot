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
from state_data import StateData

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SearchByProductList))
async def search_handler(callback: CallbackQuery, state: FSMContext, callback_data: NavigateButton) -> None:
    send_as_new = callback_data.data == 'new'
    await send_search_by_product_list_message(callback.message, state, send_as_new)
    await callback.answer()


async def send_search_by_product_list_message(message: Message, state: FSMContext, send_as_new=False):
    data = await state.get_data()
    state_data: StateData = data['state_data']

    if send_as_new:
        bot_message = await message.answer(
            texts.search_by_product_list, reply_markup=keyboards.get_waiting_for_food_list_keyboard())
        await message.delete()
        state_data.bot_message = bot_message
    else:
        await message.edit_text(
            texts.search_by_product_list, reply_markup=keyboards.get_waiting_for_food_list_keyboard())

    state_data.search_filters = SearchFilters()
    await state.set_state(states.Search.waiting_food_list)
    await state.update_data(state_data=state_data)


@router.message(states.Search.waiting_food_list)
async def food_list_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    state_data: StateData = data['state_data']

    bot_message: Message = state_data.bot_message
    product_list = message.text
    await bot_message.edit_text(
        texts.food_list_entering.format(product_list=product_list),
        reply_markup=keyboards.get_food_list_entering_keyboard()
    )
    products = product_list.split('\n')
    state_data.search_filters = SearchFilters(products)
    await state.update_data(state_data=state_data)
    await message.delete()


async def send_search_result_message(
        message: Message, state: FSMContext, recipe: dict, send_as_new: bool = False):
    state_data: StateData = (await state.get_data())['state_data']
    ingredients = [
        f"{i['name']} - {str(i.get('quantity', '')).lower()} {i['unit'].lower()}"
        for i in recipe['ingredients']
    ]

    text = texts.search_result.format(
        name=recipe['name'],
        cookingTime=recipe['cookingTime'],
        calories=recipe['calories'],
        ingredients='\n'.join(ingredients)
    )

    photo_path = f'recipes/photos/{recipe["photo"]}'
    if not os.path.exists(photo_path):
        await message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {photo_path} не существует")
        return

    photo = FSInputFile(photo_path)
    if send_as_new:
        bot_message = await message.answer_photo(
            photo, text, reply_markup=keyboards.get_search_result_keyboard())
        await message.delete()
        state_data.bot_message = bot_message
    else:
        await message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=keyboards.get_search_result_keyboard()
        )

    await state.update_data(state_data=state_data)

@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(None)
    await send_waiting_message(callback)

    data = await state.get_data()
    state_data: StateData = data['state_data']

    recipes = db_functions.search_recipes_by_filters(state_data.search_filters)
    random.shuffle(recipes)
    selected_recipe = random.choice(recipes)
    recipes.remove(selected_recipe)
    state_data.selected_recipe = selected_recipe
    state_data.search_result = recipes

    await state.update_data(state_data=state_data)

    await send_search_result_message(callback.message, state, selected_recipe, True)
    await callback.answer()


async def send_waiting_message(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(texts.wait_for_result)
    await callback.message.chat.do('typing')
    await sleep(3)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.NewSearch))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    state_data: StateData = data['state_data']

    recipes = state_data.search_result
    if len(recipes) == 0:
        await callback.answer('Упс, рецепты кончились!')
        return

    selected_recipe = random.choice(recipes)
    recipes.remove(selected_recipe)
    state_data.selected_recipe = selected_recipe

    await state.update_data(state_data=state_data)

    await send_search_result_message(callback.message, state, selected_recipe)
    await callback.answer()


async def format_recipe_stage_text(message: Message, state_data: StateData):
    stage_count = len(state_data.selected_recipe['recipe'])
    stage = state_data.selected_recipe['recipe'][state_data.current_stage - 1]
    text = texts.recipe_stage.format(
        current_stage=state_data.current_stage,
        stage_count=stage_count,
        title=stage.get('title', None),
        description=stage.get('description', None)
    )

    await message.edit_caption(
        caption=text,
        reply_markup=keyboards.get_stages_menu_keyboard(state_data.current_stage, stage_count))


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.RecipeStages))
async def recipe_stages_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    state_data: StateData = data['state_data']
    state_data.current_stage = 1
    await format_recipe_stage_text(callback.message, state_data)
    await state.update_data(state_data=state_data)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.RecipeStage))
async def recipe_stages_selector_handler(
        callback: CallbackQuery, state: FSMContext, callback_data: NavigateButton) -> None:
    data = await state.get_data()
    state_data: StateData = data['state_data']
    state_data.current_stage = int(callback_data.data)
    await format_recipe_stage_text(callback.message, state_data)
    await state.update_data(state_data=state_data)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.RecipeCard))
async def recipe_card_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    state_data: StateData = data['state_data']

    await send_search_result_message(callback.message, state, state_data.selected_recipe)
    await callback.answer()
