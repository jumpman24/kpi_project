import re

from models import Rank, Pairing
from queries import (
    select_rank,
    select_country,
    select_city,
    insert_city,
    select_player_query,
    insert_player_query,
    select_participant_query,
    insert_participant_query,
    delete_participant_query,
    insert_pairing_query,
    delete_pairing_query,
)

RESULT_REGEX = re.compile(r'(?P<opponent>\d+)(?P<result>[+\-])(?P<is_technical>!)?(/(?P<color>[wbh])(?P<handicap>\d))?')


def parse_tournament_table(data, tournament_id, place_idx, full_name_idx, country_idx, city_idx, rank_idx, rating_idx,
                           first_round_idx,
                           last_round_idx):
    data = data.decode().split('\n')
    delete_pairing_query(tournament_id)
    delete_participant_query(tournament_id=tournament_id)
    start_indices = [0] + [i + 1 for i in range(len(data[0])) if data[0][i] == ' ']
    end_indices = [i for i in range(len(data[0])) if data[0][i] == ' '] + [len(data[0])]
    column_slices = [slice(*col) for col in zip(start_indices, end_indices)]

    all_countries = select_country()
    all_cities = select_city()
    all_ranks = select_rank()
    all_players = select_player_query()
    participant_list = select_participant_query(tournament_id=tournament_id)

    rounds = {}

    table_data = []
    for row in data[3:]:
        country_code = row[column_slices[country_idx]].strip()
        city_name = row[column_slices[city_idx]].strip()

        rank_name = row[column_slices[rank_idx]].strip()

        last_name, first_name = row[column_slices[full_name_idx]].split(',')
        last_name = last_name.strip()
        first_name = first_name.strip()

        rating_start = row[column_slices[rating_idx]].strip()
        rating_start = float(rating_start) if rating_start else None

        cities = [c for c in all_cities if c.name == city_name]
        if len(cities) > 1:
            cities = [c for c in all_cities if c.country.code.lower() == country_code.lower()]
        if not cities:
            country_id = [c.id for c in all_countries if c.code.lower() == country_code.lower()][0]
            city_id = insert_city(city_name, country_id)
            city = select_city(city_id)[0]
        else:
            city = cities[0]

        ranks = [r for r in all_ranks if r.name == rank_name]
        rank = ranks[0] if ranks else Rank(None, None, None)

        players = [p for p in all_players if
                   p.last_name.lower() == last_name.lower() and p.first_name.lower() == first_name.lower()]

        if len(players) > 1:
            players = [p for p in players if p.city.name == city_name]

        if not players:
            player_id = insert_player_query(last_name, first_name, None, rating_start, False, city.id, rank.id, None)
            player = select_player_query(player_id)
        else:
            player = players[0]

        place = int(row[column_slices[place_idx]])
        participants = [p for p in participant_list if p.player.id == player.id]

        if participants:
            participant = participants[0]
        else:
            participant_id = insert_participant_query(player.id, tournament_id, place, rank.id, rating_start, None)
            participant = select_participant_query(participant_id)[0]

        rounds[participant] = [row[column_slices[i]].strip() for i in range(first_round_idx, last_round_idx + 1)]

    participants = select_participant_query(tournament_id=tournament_id)

    for player, results in rounds.items():
        for i in range(len(results)):
            match = results[i]
            round_skip = match in ('--', '+-')

            if not round_skip:
                re_match = RESULT_REGEX.match(match)
                opponent_place = int(re_match.group('opponent'))
                result = re_match.group('result') == '+'
                is_technical = bool(re_match.group('is_technical'))
                if re_match.group('color'):
                    color = re_match.group('color') in 'bw'
                else:
                    color = None
                handicap = re_match.group('color') or 0
                opponent = next(p for p in participants if p.place == opponent_place)
            else:
                is_technical = result = match == '+-'
                color, handicap = None, None
                opponent = Pairing.empty()

            insert_pairing_query(player.id, i + 1, opponent.id, color, handicap, result, round_skip, is_technical)
