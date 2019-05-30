from flask import Blueprint, render_template, request, redirect
from models import Player, City
from utils import render_table, render_select

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


@bp.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        return redirect('/players')

    city_data = City.get_columns('id', 'name')
    cities = render_select('city', city_data)
    return render_template('add_player.html', cities=cities)
