from flask import Blueprint, render_template
from models import Player

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('/', methods=['GET'])
def players():
    player_list = Player.info()
    return render_template('players.html', player_list=player_list)
