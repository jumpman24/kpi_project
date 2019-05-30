from flask import Blueprint, render_template
from models import Player
from utils import render_table

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('/', methods=['GET'])
def players():
    player_list = Player.info()
    table_data = []
    for idx, row in enumerate(player_list, start=1):
        table_data.append([idx] + list(row))

    column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN']
    table = render_table(column_names, table_data)
    return render_template('players.html', player_list=table)
