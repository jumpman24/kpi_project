from .base import BaseModel


class Rank(BaseModel):
    table_name = 'rank'
    columns = (
        'id',
        'name',
        'abbreviate',
    )

    def __init__(self, id, name, abbreviate):
        self.id = id
        self.name = name
        self.abbreviate = abbreviate

    def __str__(self):
        return f"{self.abbreviate}"
