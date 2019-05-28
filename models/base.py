from utils import mysql_execute


class BaseModel:
    table_name = NotImplemented
    columns = NotImplemented

    @classmethod
    def get_by_id(cls, id):
        query = 'SELECT {} FROM {} WHERE `id` = {}'.format(', '.join(cls.columns), cls.table_name, id)
        results = mysql_execute(query)

        for row in results:
            return cls(*row)
