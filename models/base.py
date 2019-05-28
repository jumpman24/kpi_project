from utils import mysql_execute


class BaseModel:
    table_name = NotImplemented
    columns = NotImplemented

    def __init__(self, *args):
        for column, value in zip(self.columns, args):
            setattr(self, column, value)

    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT {', '.join(cls.columns)} FROM {cls.table_name} WHERE `id` = {id}"
        results = mysql_execute(query)

        for row in results:
            return cls(*row)
