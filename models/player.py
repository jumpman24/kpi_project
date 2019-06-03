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
    def info(cls, player_id=None, concat_name=True, concat_city=False):
        if concat_name:
            name_columns = "CONCAT(p.last_name, ' ', p.first_name), "
        else:
            name_columns = "p.last_name, p.first_name, "

        if concat_city:
            city_column = "CONCAT(c.name, ' (', c2.code, ')'), "
        else:
            city_column = "c.name, "

        query = (
            f"SELECT "
            f"p.id, "
            f"{name_columns}"
            f"{city_column}"
            f"COALESCE(p.rating, ''), "
            f"COALESCE(r.name, ''), "
            f"COALESCE(nr.abbreviate, ''), "
            f"COALESCE(p.PIN, '') "
            f"FROM player as p "
            f"LEFT JOIN city as c "
            f"ON p.city_id=c.id "
            f"LEFT JOIN country as c2 "
            f"ON c.country_id=c2.id "
            f"LEFT JOIN `rank` as r "
            f"ON p.rank_id=r.id "
            f"LEFT JOIN national_rank as nr "
            f"ON p.national_rank_id=nr.id "
        )
        if player_id:
            query += 'WHERE p.id =' + player_id

        return cls.execute_query(query)

    @classmethod
    def update(cls, player_id, last_name, first_name, city_id, rating, rank_id, national_rank_id):
        query = (
            f"UPDATE player "
            f"SET last_name='{last_name}', first_name='{first_name}', rating={rating}, city_id={city_id}, "
            f"rank_id={rank_id}, national_rank_id={national_rank_id} "
            f"WHERE id={player_id}"
        )
        print(query)
