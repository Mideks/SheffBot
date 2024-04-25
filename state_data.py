from aiogram.types import Message
from tinydb.table import Document

from search_filters import SearchFilters


class StateData:
    search_filters: SearchFilters
    search_result: list[Document]
    selected_recipe: dict
    current_stage: int
    bot_message: Message
