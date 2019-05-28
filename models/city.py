from .base import BaseModel


class City(BaseModel):
    table_name = 'city'
    columns = (
        'id',
        'name',
        'country_id',
    )

    def __str__(self):
        return f"{self.name}"
