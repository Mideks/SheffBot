command_start = (
    "👋 Привет, вижу, ты сюда пришёл, чтобы покушать.\n"
    "👤 Позволь мне помочь тебе с этим."
)

search_by_product_list = (
    "Расскажи, что у тебя есть в холодильнике?\n"
    "Просто напиши продукты, из которых ты хочешь что-то приготовить\n\n"
    "Пример:<i>\n"
    "Банан\n"
    "Творог\n"
    "Сметана</i>"
)

food_list_entering = (
    'Вот ваш список продуктов. \n\n'
    '{product_list}\n\n'
    'Вы можете ввести продукты заново.\n'
    'Если всё ввели верно, нажмите кнопку ниже'
)

wait_for_result = "Подождите, готовим ваше блюдо..."

search_result = (
    "Вот что нам удалось найти:\n"
    "<b>{name}</b> - {cookingTime} мин.\n"
    "<b>Калории:</b> {calories} ккал\n\n"
    "<b>Ингридиенты:</b>\n"
    "{ingredients}\n"
)

recipe_stage = (
    'Этап {current_stage} из {stage_count}\n'
    '<b>{title}</b>\n'
    '{description}'
)
