from flask import Blueprint, render_template
from queries import select_player_query, select_tournament_query


bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    players = select_player_query()[:10]
    tournaments = select_tournament_query()[:10]
    return render_template('index.html', players=players, tournaments=tournaments)
