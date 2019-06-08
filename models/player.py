from database import execute_query, prep_value, prep_string, prep_float, prep_int, prep_bool
from models.models import Country, City, Rank, NationalRank, Player
from typing import List


def select_player_query(pid: int = None, order_by='rating', desc=True) -> List[Player]:
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
        query += f"WHERE p.id = {pid}\n"

    query += f"ORDER BY {order_by}{' DESC' if desc else ''}"

    result = execute_query(query)

    players = []
    for (
            player_id, last_name, first_name, PIN, rating, is_active,
            city_id, city_name, country_id,
            country_name, country_code,
            rank_id, rank_name, rank_abbreviate,
            national_rank_id, national_rank_name, national_rank_abbreviate
    ) in result:
        country = Country(country_id, country_name, country_code)
        city = City(city_id, city_name, country)
        rank = Rank(rank_id, rank_name, rank_abbreviate)
        national_rank = NationalRank(national_rank_id, national_rank_name, national_rank_abbreviate)

        player = Player(player_id, last_name, first_name, PIN, rating, is_active, city, rank, national_rank)
        players.append(player)

    return players


def insert_player_query(last_name, first_name, pin: str = None, rating: float = None, is_active: str = None,
                        city_id: int = None, rank_id: int = None, national_rank_id: int = None):
    last_name = prep_string(last_name)
    first_name = prep_string(first_name)
    pin = prep_string(pin)
    rating = prep_float(rating)
    is_active = prep_bool(is_active)
    city_id = prep_int(city_id)
    rank_id = prep_int(rank_id)
    national_rank_id = prep_int(national_rank_id)
    query = f"""
INSERT INTO player
    (last_name, first_name, PIN, rating, is_active, city_id, rank_id, national_rank_id)
VALUES
    ({last_name}, {first_name}, {pin}, {rating}, {is_active}, {city_id}, {rank_id}, {national_rank_id})
"""

    return execute_query(query)


def update_player_query(player_id: int, last_name: str = None, first_name: str = None, pin: str = None, rating: float = None,
                        is_active: str = None, city_id: int = None, rank_id: int = None, national_rank_id: int = None):
    player = select_player_query(player_id)[0]

    last_name = prep_string(last_name, player.last_name)
    first_name = prep_string(first_name, player.first_name)
    pin = prep_string(pin, player.pin)
    rating = prep_float(rating, player.rating)
    is_active = prep_bool(is_active, player.is_active)
    city_id = prep_int(city_id)
    rank_id = prep_int(rank_id)
    national_rank_id = prep_int(national_rank_id)
    query = f"""
UPDATE player SET
last_name = {last_name},
first_name = {first_name},
pin = {pin},
rating = {rating},
is_active = {is_active},
city_id = {city_id},
rank_id = {rank_id},
national_rank_id = {national_rank_id}
WHERE id = {player_id}
"""

    return execute_query(query)


def delete_player_query(player_id: int):
    query = f"DELETE FROM player WHERE id = {player_id}"

    return execute_query(query)
