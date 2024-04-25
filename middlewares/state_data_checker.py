from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from search_filters import SearchFilters
from state_data import StateData


class StateDataChecker(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        state: FSMContext = data["state"]
        data_ = await state.get_data()
        if "state_data" not in data_:
            await state.update_data(state_data=StateData())

        return await handler(event, data)