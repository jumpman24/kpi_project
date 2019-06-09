from database import execute_query
from models import Country
from typing import List


def select_country(cid: int = None) -> List[Country]:
    query = "SELECT id, name, code FROM country"

    if cid:
        query += f" WHERE id = {cid}"

    result = execute_query(query)

    countries = []
    for country_id, name, code in result:
        rank = Country(country_id, name, code)
        countries.append(rank)

    return countries
