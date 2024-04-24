import enum

from aiogram.filters.callback_data import CallbackData


class NavigateButtonLocation(enum.Enum):
    NewSearch = "NewSearch"
    StartSearch = "StartSearch"
    Search = "Search"


class NavigateButton(CallbackData, prefix="navigate"):
    location: NavigateButtonLocation
