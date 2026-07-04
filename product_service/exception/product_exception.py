class ProductNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class InvalidCategoryException(Exception):
    def __init__(self, name: str):
        self.name = name


class CategoryServiceUnavailableException(Exception):
    def __init__(self, name: str):
        self.name = name
