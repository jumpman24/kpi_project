from models import BaseModel, Player, Tournament


class Participant(BaseModel):
    table_name = 'participant'
    columns = (
        'id',
        'player_id',
        'tournament_id',
        'rank_id',
        'place',
        'rating_start',
        'rating_end',
    )

    def __str__(self):
        player = Player.get_by_id(self.player_id)
        tournament = Tournament.get_by_id(self.tournament_id)
        return f"{player} @ {tournament}"
