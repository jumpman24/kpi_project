from models import Country, City, Tournament
from database import execute_query, prep_string, prep_int, prep_bool, prep_date
from models import Country, City, Tournament


def select_tournament_query(tid=None):
    query = """
SELECT
    t.id, t.name, t.PIN, t.date_start, t.date_end, t.is_ranked,
    c.id, c.name,
    c2.id, c2.name, c2.code
FROM tournament t
LEFT JOIN city c ON t.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id
"""
    if tid:
        query += f"WHERE t.id = {tid}"

    result = execute_query(query)

    tournaments = []
    for (
            tournament_id, name, pin, date_start, date_end, is_ranked,
            city_id, city_name, country_id,
            country_name, country_code
    ) in result:
        country = Country(country_id, country_name, country_code)
        city = City(city_id, city_name, country)

        tournament = Tournament(tournament_id, name, pin, date_start, date_end, is_ranked, city)
        tournaments.append(tournament)

    return tournaments


def update_tournament_query(tournament_id, name=None, pin=None, date_start=None, date_end=None, is_ranked=None,
                            city_id=None):
    name = prep_string(name)
    pin = prep_string(pin)
    date_start = prep_date(date_start)
    date_end = prep_date(date_end)
    is_ranked = prep_bool(is_ranked)
    city_id = prep_int(city_id)
    query = f"""
UPDATE tournament SET
name = {name},
PIN = {pin}, 
date_start = {date_start}, 
date_end = {date_end}, 
is_ranked = {is_ranked},
city_id = {city_id}
WHERE id= {tournament_id}
"""

    return execute_query(query)


def insert_tournament_query(name, pin, date_start, date_end, is_ranked, city_id):
    name = prep_string(name)
    pin = prep_string(pin)
    date_start = prep_date(date_start)
    date_end = prep_date(date_end)
    is_ranked = prep_bool(is_ranked)
    city_id = prep_int(city_id)

    query = f"""
INSERT INTO tournament
    (name, PIN, date_start, date_end, is_ranked, city_id)
VALUES
    ({name}, {pin}, {date_start}, {date_end}, {is_ranked}, {city_id})
"""

    return execute_query(query)
