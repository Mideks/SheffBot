import enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class NavigateButtonLocation(enum.Enum):
    RecipeStage = "RecipeStage"
    RecipeCard = "RecipeCard"
    RecipeStages = "RecipeStages"
    NewSearch = "NewSearch"
    StartSearch = "StartSearch"
    SearchByProductList = "SearchByProductList"


class NavigateButton(CallbackData, prefix="navigate"):
    location: NavigateButtonLocation
    data: Optional[str] = None
