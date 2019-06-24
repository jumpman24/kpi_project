from database import execute_query

from . import BaseModel, Country, City, Rank, NationalRank, Player, Tournament


class Participant(BaseModel):
    table_name = 'participant'
    columns = [
        ('id', int),
        ('player_id', int),
        ('tournament_id', int),
        ('place', int),
        ('rank_id', int),
        ('rating_start', float),
        ('rating_end', float),
    ]

    def __init__(self, participant_id, place, rating_start, rating_end,
                 player: Player, tournament: Tournament, rank: Rank):
        self.id = participant_id
        self.place = place
        self.rating_start = rating_start
        self.rating_end = rating_end
        self.player = player
        self.tournament = tournament
        self.rank = rank

    def __str__(self):
        if self:
            return f"{self.place} {self.player}"
        return "-- no player --"

    @classmethod
    def aliased_columns(cls):
        return cls.make_aliased_columns('tp') \
               + Tournament.make_aliased_columns('t') \
               + City.make_aliased_columns('tc') \
               + Country.make_aliased_columns('tc2') \
               + Player.make_aliased_columns('p') \
               + City.make_aliased_columns('c') \
               + Country.make_aliased_columns('c2') \
               + Rank.make_aliased_columns('r') \
               + NationalRank.make_aliased_columns('nr') \
               + Rank.make_aliased_columns('r2')

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, Player.empty(), Tournament.empty(), Rank.empty())

    def __bool__(self):
        return bool(self.player)

    @classmethod
    def execute_select(cls, filters=None, order_by=None):
        query = f"""SELECT
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
LEFT JOIN `rank` r ON p.rank_id=r.id
LEFT JOIN national_rank nr ON p.national_rank_id=nr.id

LEFT JOIN `rank` r2 ON tp.rank_id=r2.id
    """
        query += cls.prepare_where(filters, 'tp')
        query += cls.prepare_order(order_by)
        result = execute_query(query)

        participants = []
        for row in result:
            participant_values = row[:4]

            tournament_values = row[4:10]
            tournament_city_values = row[10:12]
            tournament_country_values = row[12:15]

            player_values = row[15:21]
            player_city_values = row[21:23]
            player_country_values = row[23:26]
            player_rank_values = row[26:29]
            player_national_rank_values = row[29:32]

            participant_rank_values = row[32:]

            tournament_country = Country(*tournament_country_values)
            tournament_city = City(*tournament_city_values, country=tournament_country)
            tournament = Tournament(*tournament_values, city=tournament_city)

            player_country = Country(*player_country_values)
            player_city = City(*player_city_values, country=player_country)
            player_rank = Rank(*player_rank_values)
            player_national_rank = NationalRank(*player_national_rank_values)
            player = Player(*player_values, city=player_city, rank=player_rank,
                            national_rank=player_national_rank)

            participant_rank = Rank(*participant_rank_values)
            participant = Participant(*participant_values, player=player, tournament=tournament,
                                      rank=participant_rank)
            participants.append(participant)

        return participants
