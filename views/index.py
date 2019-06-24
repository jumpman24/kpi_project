from flask import Blueprint, render_template
from models import Player, Tournament

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    players = Player.execute_select()[:10]
    tournaments = Tournament.execute_select()[:10]
    return render_template('index.html', players=players, tournaments=tournaments)
