from typing import Optional, Set


class SearchFilters:
    products: list[str]

    def __init__(self, products=None):
        if products is None:
            products = list()
        self.products = products

    def __eq__(self, other):
        if isinstance(other, SearchFilters):
            return self.products == other.products
        return False
