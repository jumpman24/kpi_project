from .base import BaseModel


class Rank(BaseModel):
    table_name = 'rank'
    columns = (
        'id',
        'name',
        'abbreviate',
    )

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def info(cls):
        query = 'SELECT id, name FROM rank'

        return cls.execute_query(query)
