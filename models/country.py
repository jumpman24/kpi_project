from database import execute_query
from . import BaseModel


class Country(BaseModel):
    table_name = 'country'
    columns = {
        'id': int,
        'name': str,
        'code': str,
    }

    def __init__(self, country_id, name, code):
        self.id = country_id
        self.name = name
        self.code = code

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, None)

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = "SELECT id, name, code FROM country "
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        return [Country(*row) for row in result]
