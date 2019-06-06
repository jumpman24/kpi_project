from models import BaseModel
from database import execute_query


class Tournament(BaseModel):
    table_name = 'tournament'
    columns = (
        'id',
        'PIN',
        'name',
        'city_id',
        'date_start',
        'date_end',
        'is_ranked',
    )

    def __str__(self):
        return self.name

    @staticmethod
    def get_tournament_info(*ids):
        id_string = ', '.join([str(id) for id in ids])
        query = (
            f"SELECT t.name, t.PIN, c.name, t.date_start, t.date_end "
            f"FROM tournament as t "
            f"INNER JOIN city as c "
            f"ON t.city_id=c.id "
            f"WHERE t.id IN ({id_string})"
        )

        return execute_query(query)

    @classmethod
    def info(cls):
        query = (
            "SELECT t.id, t.name, c.name, t.date_start, t.date_end, t.PIN "
            "FROM tournament as t "
            "INNER JOIN city as c "
            "ON t.city_id=c.id "
            "ORDER BY t.date_start DESC"
        )

        return cls.execute_query(query)
