from models import BaseModel


class Pairing(BaseModel):
    table_name = 'pairing'
    columns = (
        'id',
        'player_id',
        'opponent_id',
        'round',
        'color',
        'handicap',
        'result',
        'round_skip',
        'is_technical',
    )

    def __str__(self):
        return f"{self.player_id} vs. {self.opponent_id}: {self.result}"
