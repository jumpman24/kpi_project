from models import BaseModel
from database import mysql_execute


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

        return mysql_execute(query)
