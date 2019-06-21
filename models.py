from collections import defaultdict
from functools import total_ordering, reduce
from database import execute_query, prep_string, prep_int, prep_float, prep_bool, prep_date
from datetime import date
from typing import List, Dict, Sequence


@total_ordering
class BaseModel:
    table_name = NotImplemented
    columns = {}

    prepare_map = {
        str: prep_string,
        float: prep_float,
        int: prep_int,
        bool: prep_bool,
        date: prep_date,
    }

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __eq__(self, other):
        for attr in self.__dict__:
            if not getattr(self, attr) == getattr(other, attr, None):
                return False
        return True

    def __lt__(self, other):
        return getattr(self, 'id') < getattr(other, 'id')

    def __bool__(self):
        return getattr(self, 'id') is not None

    def __hash__(self):
        return self.id

    def __getattr__(self, item):
        return reduce(lambda obj, attr: obj.__getattribute__(attr), item.split('.'), self)

    def get_attrs(self, *attrs):
        return [self.__getattr__(attr) for attr in attrs]

    @classmethod
    def _prepare_value(cls, value):
        if value is None:
            return 'NULL'

        return cls.prepare_map[type(value)](value)

    @classmethod
    def prepare_where(cls, filters: Dict, table_alias=''):
        if not filters:
            return ''

        valid_filters = {}
        for col, type_ in cls.columns.items():
            if filters.get(col):
                key = table_alias + '.' + col if table_alias else col
                value = cls._prepare_value(filters[col])
                valid_filters[key] = value

        if valid_filters:
            return 'WHERE ' + ' AND '.join([f'{k}={v}' for k, v in valid_filters.items()])

        return ''

    @classmethod
    def prepare_order(cls, order_by: List[Sequence] = None):
        if not order_by:
            return ''

        valid_columns = []
        for col, asc in order_by:
            if col in cls.columns.keys():
                if asc:
                    valid_columns.append(col + ' ASC')
                else:
                    valid_columns.append(col + ' DESC')

        if valid_columns:
            return 'ORDER BY ' + ', '.join(valid_columns)

    @classmethod
    def execute_insert(cls, data: List[Dict]):

        insert_values = []
        for row in data:
            values = []
            for col in cls.columns.keys():
                values.append(cls._prepare_value(row.get(col, None)))

            insert_values.append('(' + ', '.join(values) + ')')

        columns = '(' + ', '.join(cls.columns.keys()) + ')'
        insert_values = ',\n'.join(insert_values)
        query = f'INSERT INTO {cls.table_name} {columns} VALUES \n{insert_values};'
        execute_query(query)

        last_ids_query = f'SELECT id FROM {cls.table_name} ORDER BY id DESC LIMIT {len(data)}'
        last_ids = [r[0] for r in execute_query(last_ids_query)]
        last_ids.reverse()

        return last_ids

    @classmethod
    def execute_update(cls, id, data: Dict = None):
        if not id or not data:
            return

        valid_values = {}

        for col, value in data.items():
            if col in cls.columns.keys():
                valid_values[col] = cls._prepare_value(value)

        if not valid_values:
            return

        values = ',\n'.join([f'{k} = {v}' for k, v in valid_values.items()])
        query = f'UPDATE {cls.table_name} SET\n' + values + '\n' + cls.prepare_where({'id': id})

        return execute_query(query)

    @classmethod
    def select(cls, filters=None, order_by=None):
        raise NotImplementedError

    @classmethod
    def select_attrs(cls, attrs: List[str], filters: Dict = None):
        if not attrs:
            return

        result = cls.select(filters)
        return [item.get_attrs(*attrs) for item in result]


class Country(BaseModel):
    table_name = 'country'
    columns = {
        'id': int,
        'name': str,
        'code': str,
    }

    def __init__(self, country_id, name, code):
        self.id = country_id
        self.name = name
        self.code = code

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, None)

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = "SELECT id, name, code FROM country "
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        return [Country(*row) for row in result]


class City(BaseModel):
    table_name = 'city'
    columns = {
        'id': int,
        'name': str,
        'country_id': str,
    }

    def __init__(self, city_id, name, country: Country):
        self.id = city_id
        self.name = name
        self.country = country

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, Country.empty())

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = """SELECT
    c.id, c.name,
    c2.id, c2.name, c2.code
FROM city c
LEFT JOIN country c2 ON c.country_id=c2.id
"""
        query += cls.prepare_where(filters, 'c')
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        cities = []
        for row in result:
            city_values = row[:2]
            country_values = row[2:]
            country = Country(*country_values)
            city = City(*city_values, country=country)
            cities.append(city)

        return cities


class Rank(BaseModel):
    columns = {
        'id': int,
        'name': str,
        'abbreviate': str,
    }

    def __init__(self, rank_id, name, abbreviate):
        self.id = rank_id
        self.name = name
        self.abbreviate = abbreviate

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, None)

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = "SELECT id, name, abbreviate FROM `rank` "
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        return [Rank(*row) for row in result]


class NationalRank(BaseModel):
    columns = {
        'id': int,
        'name': str,
        'abbreviate': str,
    }

    def __init__(self, national_rank_id, name, abbreviate):
        self.id = national_rank_id
        self.name = name
        self.abbreviate = abbreviate

    def __str__(self):
        return self.name or ''

    @classmethod
    def empty(cls):
        return cls(None, None, None)

    @classmethod
    def select(cls, filters=None, order_by=None):
        query = "SELECT id, name, abbreviate FROM national_rank "
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

        result = execute_query(query)

        return [NationalRank(*row) for row in result]


class Player(BaseModel):
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
    def select(cls, filters=None, order_by=None):
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
        query += cls.prepare_where(filters)
        query += cls.prepare_order(order_by)

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


class Tournament(BaseModel):
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


class Participant(BaseModel):
    def __init__(self, participant_id, player: Player, tournament: Tournament, place, rank: Rank, rating_start=None,
                 rating_end=None):
        self.id = participant_id
        self.player = player
        self.tournament = tournament
        self.place = place
        self.rank = rank
        self.rating_start = rating_start
        self.rating_end = rating_end

    def __str__(self):
        if self:
            return f"{self.place} {self.player}"
        return "-- no player --"

    @classmethod
    def empty(cls):
        return cls(None, Player.empty(), Tournament.empty(), None, Rank.empty(), None, None)

    def __bool__(self):
        return bool(self.player)


class Pairing(BaseModel):
    def __init__(self, pairing_id, player: Participant, round, opponent: Participant = None, color=None, handicap=None,
                 result=None, round_skip=False, is_technical=False):
        self.id = pairing_id
        self.player = player
        self.round = round
        self.opponent = opponent or None
        self.color = color
        self.handicap = handicap
        self.result = result
        self.round_skip = round_skip
        self._is_technical = is_technical

    def __str__(self):
        return f"{self.player} {self.get_result()}"

    @classmethod
    def empty(cls):
        return cls(None, Participant.empty(), None, Participant.empty(), None, None, None)

    def get_result(self, color_and_handicap=False):
        if self.round_skip or not self.opponent:
            return '0='

        s = str(self.opponent.place)

        s += '+' if self.result == 1 else '-'
        s += '!' if self._is_technical else ''

        if color_and_handicap:
            s += '/'
            s += self.color if self.color else 'h'
            s += str(self.handicap)

        return s


class TournamentTable(BaseModel):
    def __init__(self, tournament, pairings):
        self.tournament = tournament
        self.pairings = pairings

    def get_table(self):
        result_dict = defaultdict(list)

        for pairing in self.pairings:
            result_dict[pairing.player].append(pairing.get_result())

        table_data = []
        for participant, results in result_dict.items():
            place, player_id, full_name, city, rank, rating = participant.get_attrs(
                'place',
                'player.id',
                'player.full_name',
                'player.city.name',
                'rank.name',
                'rating_start',
            )
            full_name = f'<a href="/players/{player_id}">{full_name}</a>'
            table_data.append([place, full_name, city, rank, rating] + results)

        return table_data, len(table_data[0])
