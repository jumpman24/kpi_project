from collections import defaultdict

from .base import BaseModel
from .country import Country
from .city import City
from .rank import Rank
from .national_rank import NationalRank
from .player import Player
from .tournament import Tournament


class Participant(BaseModel):
    def __init__(self, participant_id, player: Player, tournament: Tournament, place, rank: Rank,
                 rating_start=None,
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
    def __init__(self, pairing_id, player: Participant, round, opponent: Participant = None,
                 color=None, handicap=None,
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
