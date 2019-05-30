from models import BaseModel, Country, City
from database import mysql_execute


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

    @classmethod
    def info(cls):
        query = (
            f"SELECT "
            f"CONCAT(p.last_name, ' ', p.first_name), "
            f"COALESCE(c.name, ''), "
            f"COALESCE(p.rating, ''), "
            f"COALESCE(r.name, ''), "
            f"COALESCE(nr.abbreviate, ''), "
            f"COALESCE(p.PIN, '') "
            f"FROM player as p "
            f"LEFT JOIN city as c "
            f"ON p.city_id=c.id "
            f"LEFT JOIN `rank` as r "
            f"ON p.rank_id=r.id "
            f"LEFT JOIN national_rank as nr "
            f"ON p.national_rank_id=nr.id "
        )

        return cls.execute_query(query)
