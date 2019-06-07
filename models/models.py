from datetime import date
from functools import total_ordering, reduce


@total_ordering
class BaseModel:
    def __eq__(self, other):
        for attr in self.__dict__:
            if not getattr(self, attr) == getattr(other, attr, None):
                return False
        return True

    def __lt__(self, other):
        return getattr(self, 'id') < getattr(other, 'id')

    def __bool__(self):
        return getattr(self, 'id') is not None

    def __getattr__(self, item):
        return reduce(lambda obj, attr: obj.__getattribute__(attr), item.split('.'), self)

    def get_attrs(self, *attrs):
        return [self.__getattr__(attr) for attr in attrs]


class Country(BaseModel):
    def __init__(self, country_id, name, code):
        self.id = country_id
        self.name = name
        self.code = code


class City(BaseModel):
    def __init__(self, city_id, name, country: Country):
        self.id = city_id
        self.name = name
        self.country = country


class Rank(BaseModel):
    def __init__(self, rank_id, name, abbreviate):
        self.id = rank_id
        self.name = name
        self.abbreviate = abbreviate


class NationalRank(BaseModel):
    def __init__(self, national_rank_id, name, abbreviate):
        self.id = national_rank_id
        self.name = name
        self.abbreviate = abbreviate


class Player(BaseModel):
    def __init__(self, player_id: int, last_name: str, first_name: str, pin: str, rating: float,
                 is_active: bool, city: City, rank: Rank, national_rank: NationalRank):
        self.id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.pin = pin
        self.rating = rating
        self.is_active = is_active
        self.city = city
        self.rank = rank
        self.national_rank = national_rank

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.full_name}{f' ({self.rank.name})' if self.rank else ''}"

    def __repr__(self):
        return f"Player(id = {self.id}, name = {self.full_name})"

    def __lt__(self, other):
        return self.rating < other.rating


class Tournament(BaseModel):
    def __init__(self, tournament_id: int, name: str, pin: str, date_start: date, date_end: date,
                 is_ranked: bool, city: City):
        self.id = tournament_id
        self.name = name
        self.pin = pin
        self.date_start = date_start
        self.date_end = date_end
        self.is_ranked = is_ranked
        self.city = city or None


class Participant(BaseModel):
    def __init__(self, participant_id: int, player: Player, tournament: Tournament, place: int,
                 rank: Rank = None,
                 rating_start: float = None, rating_end: float = None):
        self.id = participant_id
        self.player = player
        self.tournament = tournament
        self.place = place
        self.rank = rank or None
        self.rating_start = rating_start
        self.rating_end = rating_end


class Pairing(BaseModel):
    def __init__(self, pairing_id, player: Participant, round: int, opponent: Participant = None,
                 color: str = None,
                 handicap: int = 0, result: bool = None, round_skip: bool = False,
                 is_technical: bool = False):
        self.id = pairing_id
        self.player = player
        self.round = round
        self.opponent = opponent or None
        self.color = color
        self.handicap = handicap
        self.result = result
        self.round_skip = round_skip
        self._is_technical = is_technical


class TournamentTable(BaseModel):
    def __init__(self, tournament, participants, pairings):
        self.tournament = tournament
        self.participants = participants
        self.pairings = pairings
