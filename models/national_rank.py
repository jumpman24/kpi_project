from database import execute_query
from . import BaseModel


class NationalRank(BaseModel):
    table_name = 'national_rank'
    columns = [
        ('id', int),
        ('name', str),
        ('abbreviate', str),
    ]

    def __init__(self, national_rank_id, name, abbreviate):
        self.id = national_rank_id
        self.name = name
        self.abbreviate = abbreviate

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, None)

    @classmethod
    def execute_select(cls, filters=None, order_by=None):
        query = "SELECT id, name, abbreviate FROM national_rank "
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        return [NationalRank(*row) for row in result]
