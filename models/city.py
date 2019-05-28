from .base import BaseModel
from .country import Country


class City(BaseModel):
    table_name = 'city'
    columns = (
        'id',
        'name',
        'country_id',
    )

    def __init__(self, id, name, country_id):
        self.id = id
        self.name = name
        self.country_id = country_id

    def __str__(self):
        country = Country.get_by_id(self.country_id)
        return f"{self.name} ({country.code})"
