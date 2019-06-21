from database import execute_query
from . import BaseModel, Country


class City(BaseModel):
    table_name = 'city'
    columns = {
        'id': int,
        'name': str,
        'country_id': str,
    }

    def __init__(self, city_id, name, country: Country):
        self.id = city_id
        self.name = name
        self.country = country

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, Country.empty())

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = """SELECT
    c.id, c.name,
    c2.id, c2.name, c2.code
FROM city c
LEFT JOIN country c2 ON c.country_id=c2.id
"""
        query += cls.prepare_where(filters, 'c')
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        cities = []
        for row in result:
            city_values = row[:2]
            country_values = row[2:]
            country = Country(*country_values)
            city = City(*city_values, country=country)
            cities.append(city)

        return cities

