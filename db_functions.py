import random
import re
from collections import defaultdict, Counter
from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('recipes/info.json', encoding='utf-8')


def search_recipes_by_filters(filters: SearchFilters) -> list[Document]:
    Recipe = Query()
    products = [ingredient.lower() for ingredient in filters.products]
    if len(products) == 0:
        return db.all()

    def contains_ingredient(ingredients):
        for ingredient in ingredients:
            if ingredient['name'].lower() in products:
                return True
        return False

    recipes_with_ingredients = db.search(Recipe.ingredients.test(contains_ingredient))

    return recipes_with_ingredients
