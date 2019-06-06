from database import execute_query


class BaseModel:
    table_name = NotImplemented
    columns = NotImplemented

    def __init__(self, *args):
        for column, value in zip(self.columns, args):
            setattr(self, column, value)

    @staticmethod
    def execute_query(query):
        return execute_query(query)

    @classmethod
    def get_columns(cls, *columns):
        query = f"SELECT {', '.join(columns)} FROM {cls.table_name}"

        return cls.execute_query(query)

    @classmethod
    def get_by_column_value(cls, column, value):
        query = (f"SELECT {', '.join(cls.columns)} "
                 f"FROM {cls.table_name} "
                 f"WHERE {column} = {value}")

        results = []
        for item in cls.execute_query(query):
            results.append(cls(*item))

        return results

    @classmethod
    def column_string(cls):
        return ', '.join([f"'{column}'" for column in cls.columns])

    @classmethod
    def get_by_id(cls, value):
        result = cls.get_by_column_value('id', value)[0]
        return result

    def select(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass
