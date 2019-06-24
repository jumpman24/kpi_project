from database import execute_query
from . import BaseModel, Country, City, Rank, NationalRank


class Player(BaseModel):
    table_name = 'player'
    columns = [
        ('id', int),
        ('last_name', str),
        ('first_name', str),
        ('pin', str),
        ('rating', float),
        ('is_active', bool),
        ('city_id', int),
        ('rank_id', int),
        ('national_rank_id', int),
    ]

    def __init__(self, player_id, last_name, first_name, pin, rating, is_active,
                 city: City, rank: Rank, national_rank: NationalRank):
        self.id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.pin = pin
        self.rating = rating
        self.is_active = is_active
        self.city = city
        self.rank = rank
        self.national_rank = national_rank

    @classmethod
    def aliased_columns(cls):
        return cls.make_aliased_columns('p') \
               + City.make_aliased_columns('c') \
               + Country.make_aliased_columns('c2') \
               + Rank.make_aliased_columns('r') \
               + NationalRank.make_aliased_columns('nr')

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None, None,
                   City.empty(), Rank.empty(), NationalRank.empty())

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.full_name}{f' ({self.rank.name})' if self.rank else ''}"

    def __repr__(self):
        return f"Player(id = {self.id}, name = {self.full_name})"

    def __lt__(self, other):
        return self.rating < other.rating

    @classmethod
    def execute_select(cls, filters=None, order_by=None):
        query = """SELECT 
    p.id, p.last_name, p.first_name, p.PIN, p.rating, p.is_active, 
    c.id, c.name, 
    c2.id, c2.name, c2.code,
    r.id, r.name, r.abbreviate, 
    nr.id, nr.name, nr.abbreviate 
FROM player p
LEFT JOIN city c ON p.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id 
LEFT JOIN `rank` r ON p.rank_id=r.id
LEFT JOIN national_rank nr ON p.national_rank_id=nr.id"""
        query += cls.prepare_where(filters, 'p')
        query += cls.prepare_order(order_by or [['p.rating', False]])

        result = execute_query(query)

        players = []
        for row in result:
            player_values = row[:6]
            city_values = row[6:8]
            country_values = row[8:11]
            rank_values = row[11:14]
            national_rank_values = row[14:]

            country = Country(*country_values)
            city = City(*city_values, country=country)
            rank = Rank(*rank_values)
            national_rank = NationalRank(*national_rank_values)

            player = Player(*player_values, city=city, rank=rank, national_rank=national_rank)
            players.append(player)

        return players
