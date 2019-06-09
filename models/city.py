from typing import List

from database import execute_query, prep_string, prep_int
from models.models import City
from .country import Country


def select_city(cid: int = None) -> List[City]:
    query = """
SELECT 
    c.id, c.name, 
    c2.id, c2.name, c2.code
FROM city c
LEFT JOIN country c2 ON c.country_id=c2.id 
"""
    if cid:
        query += f"WHERE c.id = {cid}"

    result = execute_query(query)

    cities = []
    for (
            city_id, city_name,
            country_id, country_name, country_code
    ) in result:
        country = Country(country_id, country_name, country_code)
        city = City(city_id, city_name, country)
        cities.append(city)

    return cities


def insert_city(name, country_id=None):
    name = prep_string(name)
    country_id = prep_int(country_id)
    query = f"""
INSERT INTO city 
    (name, country_id)
VALUES 
    ({name}, {country_id})
"""

    return execute_query(query)


def update_city(city_id, name=None, country_id=None):
    name = prep_string(name)
    country_id = prep_int(country_id)
    query = f"""
UPDATE city SET
name = {name}, 
country_id = {country_id}
WHERE id = {city_id}
"""

    return execute_query(query)


def delete_city(city_id):
    query = f"DELETE FROM city WHERE id = {city_id}"

    return execute_query(query)
