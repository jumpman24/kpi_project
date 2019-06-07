from database import execute_query, prep_value
from .country import Country
from typing import List
from models.models import City


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


def insert_city(name: str, country_id: int = None):
    name = prep_value(name)
    country_id = prep_value(country_id)
    query = f"""
INSERT INTO city 
    (name, country_id)
VALUES 
    ({name}, {country_id})
"""

    return execute_query(query)


def update_city(city_id: int, name: str = None, country_id: int = None):
    city = select_city(city_id)[0]
    name = prep_value(name or city.name)
    country_id = prep_value(country_id or city.country.id)
    query = f"""
UPDATE city SET
name = {name}, 
country_id = {country_id}
WHERE id = {city_id}
"""

    return execute_query(query)


def delete_city(city_id: int):
    query = f"DELETE FROM city WHERE id = {city_id}"

    return execute_query(query)
