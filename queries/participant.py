from database import execute_query, prep_int, prep_float
from models import Country, City, Rank, NationalRank, Player, Tournament, Participant


def select_participant_query(pid=None, tournament_id=None, player_id=None):
    query = f"""
SELECT
    tp.id, tp.place, tp.rating_start, tp.rating_end, 

    t.id, t.name, t.PIN, t.date_start, t.date_end, t.is_ranked,
    tc.id, tc.name,
    tc2.id, tc2.name, tc2.code,

    p.id, p.last_name, p.first_name, p.PIN, p.rating, p.is_active, 
    c.id, c.name, 
    c2.id, c2.name, c2.code,
    r.id, r.name, r.abbreviate, 
    nr.id, nr.name, nr.abbreviate,

    r2.id, r2.name, r2.abbreviate

FROM participant tp

INNER JOIN tournament t ON tp.tournament_id=t.id
LEFT JOIN city tc ON t.city_id=tc.id
LEFT JOIN country tc2 ON tc.country_id=tc2.id

INNER JOIN player p ON tp.player_id=p.id
LEFT JOIN city c ON p.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id 
LEFT JOIN rank r ON p.rank_id=r.id
LEFT JOIN national_rank nr ON p.national_rank_id=nr.id

LEFT JOIN rank r2 ON tp.rank_id=r2.id
"""
    if pid:
        query += f'WHERE tp.id = {pid}\n'
    elif tournament_id:
        query += f'WHERE tp.tournament_id = {tournament_id}\n'
    elif player_id:
        query += f"WHERE p1.id = {player_id}\n"

    query += 'ORDER BY place ASC'

    result = execute_query(query)

    participants = []
    for (
            tp1_id, tp_place, tp1_rating_start, tp1_rating_end,

            t_id, t_name, t_PIN, t_date_start, t_date_end, t_is_ranked,
            tc_id, tc_name,
            tc2_id, tc2_name, tc2_code,

            p1_id, p1_last_name, p1_first_name, p1_PIN, p1_rating, p1_is_active,
            c1_id, c1_name,
            c2_id, c2_name, c2_code,
            r1_id, r1_name, r1_abbreviate,
            nr1_id, nr1_name, nr1_abbreviate,

            r2_id, r2_name, r2_abbreviate
    ) in result:
        tournament_country = Country(tc2_id, tc2_name, tc2_code)
        tournament_city = City(tc_id, tc_name, tournament_country)

        tournament = Tournament(t_id, t_name, t_PIN, t_date_start, t_date_end, t_is_ranked, tournament_city)

        country1 = Country(c2_id, c2_name, c2_code)
        city1 = City(c1_id, c1_name, country1)
        rank1 = Rank(r1_id, r1_name, r1_abbreviate)
        national_rank1 = NationalRank(nr1_id, nr1_name, nr1_abbreviate)
        player1 = Player(p1_id, p1_last_name, p1_first_name, p1_PIN, p1_rating, p1_is_active, city1, rank1,
                         national_rank1)

        participant_rank = Rank(r2_id, r2_name, r2_abbreviate)
        participant = Participant(tp1_id, player1, tournament, tp_place, participant_rank, tp1_rating_start,
                                  tp1_rating_end)
        participants.append(participant)

    return participants


def insert_participant_query(player_id, tournament_id, place, rank_id, rating_start, rating_end):
    player_id = prep_int(player_id)
    tournament_id = prep_int(tournament_id)
    rank_id = prep_int(rank_id)
    place = prep_int(place)
    rating_start = prep_float(rating_start)
    rating_end = prep_float(rating_end)

    query = f"""INSERT INTO participant
    (player_id, tournament_id, place, rank_id, rating_start, rating_end)
VALUES
    ({player_id}, {tournament_id}, {place}, {rank_id}, {rating_start}, {rating_end})
"""

    return execute_query(query)


def delete_participant_query(tournament_id):
    query = f"DELETE FROM participant WHERE tournament_id = {tournament_id}"
    return execute_query(query)
