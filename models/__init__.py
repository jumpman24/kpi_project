from collections import defaultdict

from .base import BaseModel
from .country import Country
from .city import City
from .rank import Rank
from .national_rank import NationalRank
from .player import Player
from .tournament import Tournament
from .participant import Participant
from .pairing import Pairing


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
