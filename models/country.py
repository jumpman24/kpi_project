from .base import BaseModel
import mysql.connector
from mysql.connector import errorcode


get_country_query = (
    f"SELECT id, name, code "
    f"FROM country "
    f"WHERE id = '%s'"
)


class Country(BaseModel):
    table_name = 'country'
    columns = (
        'id',
        'name',
        'code',
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Country: {self.name}"

    @classmethod
    def select(cls, id=None, name=None, code=None):
        query = "SELECT id, name, code FROM country "
        where = []
        if id:
            where.append(f"id = {id}")
        if name:
            where.append(f"name = '{name}'")
        if code:
            where.append(f"code = '{code}'")

        if where:
            query += 'WHERE ' + ' AND '.join(where)

        return cls.execute_query(query)
