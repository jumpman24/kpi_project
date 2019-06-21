from typing import Dict
from datetime import date

from database import execute_query
from . import BaseModel, Country, City


class Tournament(BaseModel):
    table_name = 'tournament'
    columns = {
        'id': int,
        'name': str,
        'pin': str,
        'date_start': date,
        'date_end': date,
        'is_ranked': bool,
        'city_id': int,
    }
    columns_to_order = columns.keys()

    def __init__(self, tournament_id, name, pin, date_start, date_end, is_ranked,
                 city: City):
        self.id = tournament_id
        self.name = name
        self.pin = pin
        self.date_start = date_start
        self.date_end = date_end
        self.is_ranked = is_ranked
        self.city = city

    def __str__(self):
        return self.name

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None, None, City.empty())

    @classmethod
    def select(cls, filters: Dict = None, order_by: Dict = None):
        query = """SELECT
    t.id, t.name, t.PIN, t.date_start, t.date_end, t.is_ranked,
    c.id, c.name,
    c2.id, c2.name, c2.code
FROM tournament t
LEFT JOIN city c ON t.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id"""
        query += cls.prepare_where(filters, 't')
        query += cls.prepare_order(order_by or [['date_start', False]], 't')

        result = execute_query(query)

        tournaments = []
        for row in result:
            tournament_values = row[:6]
            city_values = row[6:8]
            country_values = row[8:]

            country = Country(*country_values)
            city = City(*city_values, country=country)
            tournament = Tournament(*tournament_values, city=city)
            tournaments.append(tournament)

        return tournaments
