from models import BaseModel
from utils import mysql_execute


class Player(BaseModel):
    table_name = 'player'
    columns = (
        'id',
        'PIN',
        'last_name',
        'first_name',
        'rating',
        'city_id',
        'rank_id',
        'national_rank_id',
        'is_active',
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @staticmethod
    def get_player_info(*ids):
        id_string = ', '.join([str(id) for id in ids])
        query = (
            f"SELECT p.last_name, p.first_name, p.PIN, p.rating, c.name, r.name, nr.name "
            f"FROM player as p "
            f"INNER JOIN city as c "
            f"ON p.city_id=c.id "
            f"INNER JOIN rank as r "
            f"ON p.rank_id=r.id "
            f"INNER JOIN national_rank as nr "
            f"ON p.national_rank_id=nr.id "
            f"WHERE p.id IN ({id_string})"
        )

        return mysql_execute(query)
