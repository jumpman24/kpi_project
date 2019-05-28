from .base import BaseModel


class Country(BaseModel):
    table_name = 'country'
    columns = (
        'id',
        'name',
        'code',
    )

    def __str__(self):
        return self.name
