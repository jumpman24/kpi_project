import re

from database import execute_procedure
from models import Country, City, Rank, Player, Participant, Pairing

RESULT_REGEX = re.compile(
    r'(?P<opponent>\d+)(?P<result>[+\-])(?P<is_technical>!)?(/(?P<color>[wbh])(?P<handicap>\d))?')
COLUMN_NAMES = {
    'place': ('№',),
    'full_name': ("Ім'я", "Имя", "Прізвище, Ім'я",),
    'country': ("Країна", "Страна",),
    'city': ("Клуб", "Місто", "Город",),
    'rank': ("Ранг",),
    'national_rank': ("Розряд", "Сп. розряд",),
    'rating': ("Рейтинг",),
}
ROUND_COLUMNS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")


class TournamentParser:
    def __init__(self, data, tournament_id):
        self.data = data.decode().split('\n')
        self.tournament_id = tournament_id
        self.slices = None
        self.indices = None
        self.participants = {}
        self.rounds = []

    def get_slices(self):
        row = self.data[0]
        start_indices = [0] + [i + 1 for i in range(len(row)) if row[i] == ' ']
        end_indices = [i for i in range(len(row)) if row[i] == ' '] + [len(row)]
        self.slices = [slice(*col) for col in zip(start_indices, end_indices)]

    def get_indices(self):
        columns = self.data[1].split()
        indices = {
            'place': None,
            'full_name': None,
            'country': None,
            'city': None,
            'rank': None,
            'national_rank': None,
            'rating': None,
            'first_round': None,
            'last_round': None,
        }
        for col, names in COLUMN_NAMES.items():
            for name in names:
                if name in columns:
                    indices[col] = columns.index(name)

        indices['first_round'] = columns.index(ROUND_COLUMNS[0])
        for rnd in ROUND_COLUMNS:
            if rnd in columns:
                indices['last_round'] = columns.index(rnd)

        self.indices = indices

    def clean_tournament_data(self):
        pairing_ids = Pairing.select_attrs(['id'], {'tp.tournament_id': self.tournament_id})
        existing_participant_ids = Participant.select_attrs(['id'], {'tournament_id': self.tournament_id})
        Pairing.execute_delete([str(p[0]) for p in pairing_ids])
        Participant.execute_delete([str(p[0]) for p in existing_participant_ids])

    def process_city(self, row):
        city_name = row[self.slices[self.indices['city']]].strip()
        cities = City.execute_select({'name': city_name})

        if cities:
            return cities[0].id

        if self.indices['country']:
            country_code = row[self.slices[self.indices['country']]].strip()
            country_id = Country.select_attrs(['id'], {'code': country_code})[0]
        else:
            country_id = 1

        return City.execute_insert([{'name': city_name, 'country_id': country_id}])[0]

    def process_rank(self, row):
        rank_name = row[self.slices[self.indices['rank']]].strip()

        rank = Rank.execute_select({'name': rank_name})

        if rank:
            return rank[0].id

        rank = Rank.execute_select({'abbreviate': rank_name})

        if rank:
            return rank[0].id

    def process_player(self, row, city_id, rank_id):
        last_name, first_name = row[self.slices[self.indices['full_name']]].split(',')
        last_name = last_name.strip()
        first_name = first_name.strip()
        rating = row[self.slices[self.indices['rating']]].strip()
        rating = float(rating) if rating else None

        players = Player.execute_select({'last_name': last_name, 'first_name': first_name})
        if len(players) == 1:
            return players[0].id

        players = [p for p in players if p.city.id == city_id]
        if len(players) == 1:
            return players[0].id

        players = [p for p in players if p.rank.id == rank_id]
        if len(players) == 1:
            return players[0].id

        player_data = {
            'last_name': last_name,
            'first_name': first_name,
            'rating': rating,
            'city_id': city_id,
            'rank_id': rank_id,
            'is_active': False,
        }
        return Player.execute_insert([player_data])[0]

    def process_participant(self, row, player_id, rank_id):
        place = int(row[self.slices[self.indices['place']]])
        rating = row[self.slices[self.indices['rating']]].strip()
        rating = float(rating) if rating else None

        participant_data = {
            'player_id': player_id,
            'tournament_id': self.tournament_id,
            'rank_id': rank_id,
            'place': place,
            'rating_start': rating,
            'rating_end': None,
        }
        participant_id = Participant.execute_insert([participant_data])[0]
        self.participants[place] = participant_id

        self.rounds.append((participant_id, [row[self.slices[i]].strip() for i in
                                             range(self.indices['first_round'], self.indices['last_round'] + 1)]))

        return participant_id

    def process_row(self, row):
        city_id = self.process_city(row)
        rank_id = self.process_rank(row)
        player_id = self.process_player(row, city_id, rank_id)
        self.process_participant(row, player_id, rank_id)

    def process_pair(self, participant_id, rnd, pair):
        round_skip = pair in ('--', '+-')

        if not round_skip:
            re_match = RESULT_REGEX.match(pair)
            opponent_place = int(re_match.group('opponent'))
            result = re_match.group('result') == '+'
            is_technical = bool(re_match.group('is_technical'))
            if (re_match.group('color') or '') in 'bw':
                color = re_match.group('color')
            else:
                color = None
            handicap = re_match.group('handicap') or 0
            opponent_id = self.participants[opponent_place]
        else:
            is_technical = result = pair == '+-'
            color = None
            handicap = None
            opponent_id = None

        pairing_data = {
            'player_id': participant_id,
            'opponent_id': opponent_id,
            'round': rnd,
            'result': result,
            'color': color,
            'handicap': handicap,
            'round_skip': round_skip,
            'is_technical': is_technical,
        }
        return pairing_data

    def process_rounds(self, participant_id, rounds):
        insert_data = []
        for rnd, pair in enumerate(rounds, start=1):
            insert_data.append(self.process_pair(participant_id, rnd, pair))
        Pairing.execute_insert(insert_data)

    def run(self):
        self.get_slices()
        self.get_indices()

        self.clean_tournament_data()

        for row in self.data[3:]:
            if row:
                self.process_row(row)

        for participant_id, rounds in self.rounds:
            self.process_rounds(participant_id, rounds)

        execute_procedure('remove_incorrect_pairings')
