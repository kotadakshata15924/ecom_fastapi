class CategoryNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class CategoryAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
