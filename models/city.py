from .base import BaseModel
from .country import Country


class City(BaseModel):
    table_name = 'city'
    columns = (
        'id',
        'name',
        'country_id',
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"City: {self.name}"

    @classmethod
    def select(cls, id=None, name=None, country_id=None):
        query = (
            "SELECT id, name, country_id FROM city "
        )
        where = []
        if id:
            where.append(f"id = {id}")
        if name:
            where.append(f"name = '{name}'")
        if country_id:
            where.append(f"country_id = '{country_id}'")

        if where:
            query += 'WHERE ' + ' AND '.join(where)

        results = []
        for row in cls.execute_query(query):
            results.append(City(*row))

        return results

    def get_country(self):
        return Country.get_by_id(self.country_id)
