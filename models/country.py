from .base import BaseModel


class Country(BaseModel):
    table_name = 'country'
    columns = (
        'id',
        'name',
        'code',
    )

    def __init__(self, id, name, code):
        if len(code) != 2:
            raise ValueError

        self.id = id
        self.name = name
        self.code = code

    def __str__(self):
        return self.name
