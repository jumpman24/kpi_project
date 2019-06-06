from database import execute_query
from models import BaseModel
from models.models import Country, City, Rank, NationalRank, Player


def select_player(pid: int = None):
    query = """
SELECT 
    p.id, p.last_name, p.first_name, p.PIN, p.rating, p.is_active, 
    c.id, c.name, 
    c2.id, c2.name, c2.code,
    r.id, r.name, r.abbreviate, 
    nr.id, nr.name, nr.abbreviate 
FROM player p
LEFT JOIN city c ON p.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id 
LEFT JOIN rank r ON p.rank_id=r.id
LEFT JOIN national_rank nr ON p.national_rank_id=nr.id
"""
    if pid:
        query += f"WHERE p.id = {pid}"

    result = execute_query(query)

    players = []
    for row in result:
        player_id, last_name, first_name, PIN, rating, is_active = row[:6]
        city_id, city_name = row[6:8]
        country_id, country_name, country_code = row[8:11]
        rank_id, rank_name, rank_abbreviate = row[11:14]
        national_rank_id, national_rank_name, national_rank_abbreviate = row[14:]

        country = Country(country_id, country_name, country_code)
        city = City(city_id, city_name, country)
        rank = Rank(rank_id, rank_name, rank_abbreviate)
        national_rank = NationalRank(national_rank_id, national_rank_name, national_rank_abbreviate)

        player = Player(player_id, last_name, first_name, PIN, rating, is_active, city, rank, national_rank)
        players.append(player)

    return players


def update_player(player_id: int, last_name: str = None, first_name: str = None, pin: str = None, rating: float = None,
                  is_active: bool = None):
    player = select_player(player_id)[0]
    last_name = last_name.replace("'", "\\'") if last_name else player.last_name
    first_name = first_name.replace("'", "\\'") if first_name else player.first_name
    pin = pin or player.pin
    rating = rating or player.rating
    is_active = int(is_active or player.is_active)
    query = f"""
UPDATE player SET
last_name = '{last_name}',
first_name = '{first_name},'
pin = '{pin}',
rating = {rating},
is_active = {is_active}
WHERE id = {player_id}
"""
    return execute_query(query)


class PlayerModel(BaseModel):
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
        last_name = last_name.replace("'", "\\'")
        first_name = first_name.replace("'", "\\'")
        rating = float(rating)
        query = (
            f"UPDATE player SET "
            f"last_name='{last_name}', "
            f"first_name='{first_name}', "
            f"rating={rating}, "
            f"city_id={city_id}, "
            f"rank_id={rank_id}, "
            f"national_rank_id={national_rank_id} "
            f"WHERE id={player_id}"
        )
        print(query)

        return cls.execute_query(query)
