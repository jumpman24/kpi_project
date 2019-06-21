from datetime import date
from functools import total_ordering, reduce
from typing import List, Dict, Sequence

from database import execute_query, prep_string, prep_int, prep_float, prep_bool, prep_date


@total_ordering
class BaseModel:
    table_name = NotImplemented
    columns = NotImplemented
    columns_to_order = NotImplemented

    prepare_map = {
        str: prep_string,
        float: prep_float,
        int: prep_int,
        bool: prep_bool,
        date: prep_date,
    }

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __eq__(self, other):
        for attr in self.__dict__:
            if not getattr(self, attr) == getattr(other, attr, None):
                return False
        return True

    def __lt__(self, other):
        return getattr(self, 'id') < getattr(other, 'id')

    def __bool__(self):
        return getattr(self, 'id') is not None

    def __hash__(self):
        return self.id

    def __getattr__(self, item):
        return reduce(lambda obj, attr: obj.__getattribute__(attr), item.split('.'), self)

    def get_attrs(self, *attrs):
        return [self.__getattr__(attr) for attr in attrs]

    @classmethod
    def _prepare_value(cls, value):
        if value is None:
            return 'NULL'

        return cls.prepare_map[type(value)](value)

    @classmethod
    def prepare_where(cls, filters: Dict, table_alias=''):
        if not filters:
            return ''

        valid_filters = {}
        for col in filters:
            key = table_alias + '.' + col if table_alias else col
            value = cls._prepare_value(filters[col])
            valid_filters[key] = value

        if valid_filters:
            return '\nWHERE ' + ' AND '.join([f'{k}={v}' for k, v in valid_filters.items()]) + '\n'

        return ''

    @classmethod
    def prepare_order(cls, order_by: List[Sequence] = None, table_alias=''):
        if not order_by:
            return ''

        valid_columns = []
        for col, asc in order_by:

            if col in cls.columns_to_order:
                key = table_alias + '.' + col if table_alias else col
                if asc:
                    valid_columns.append(key + ' ASC')
                else:
                    valid_columns.append(key + ' DESC')

        if valid_columns:
            return '\nORDER BY ' + ', '.join(valid_columns) + '\n'

        return ''

    @classmethod
    def execute_insert(cls, data: List[Dict]):

        insert_values = []
        for row in data:
            values = []
            for col in cls.columns.keys():
                values.append(cls._prepare_value(row.get(col, None)))

            insert_values.append('(' + ', '.join(values) + ')')

        columns = '(' + ', '.join(cls.columns.keys()) + ')'
        insert_values = ',\n'.join(insert_values)
        query = f'INSERT INTO {cls.table_name} {columns} VALUES \n{insert_values};'
        execute_query(query)

        last_ids_query = f'SELECT id FROM {cls.table_name} ORDER BY id DESC LIMIT {len(data)}'
        last_ids = [r[0] for r in execute_query(last_ids_query)]
        last_ids.reverse()

        return last_ids

    @classmethod
    def execute_update(cls, id, data: Dict = None):
        if not id or not data:
            return

        valid_values = {}

        for col, value in data.items():
            if col in cls.columns.keys():
                valid_values[col] = cls._prepare_value(value)

        if not valid_values:
            return

        values = ',\n'.join([f'{k} = {v}' for k, v in valid_values.items()])
        query = f'UPDATE {cls.table_name} SET\n' + values + '\n' + cls.prepare_where({'id': id})

        return execute_query(query)

    @classmethod
    def execute_delete(cls, ids: List):
        if not ids:
            return

        query_ids = ', '.join(ids)
        query = f'DELETE FROM {cls.table_name} WHERE id IN ({query_ids})'

        return execute_query(query)

    @classmethod
    def select(cls, filters=None, order_by=None):
        raise NotImplementedError

    @classmethod
    def select_attrs(cls, attrs: List[str], filters: Dict = None):
        if not attrs:
            return

        result = cls.select(filters)
        return [item.get_attrs(*attrs) for item in result]
