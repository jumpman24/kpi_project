from flask import Blueprint, render_template, request, redirect
from models import Player, City, Rank, NationalRank
from utils import render_table, render_select

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('/', methods=['GET'])
def players():
    player_list = Player.info()
    player_ids = []
    table_data = []
    for idx, row in enumerate(player_list, start=1):
        player_ids.append(row[0])
        table_data.append([idx] + list(row)[1:])

    column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN']
    table = render_table(column_names, table_data)
    return render_template('players.html', player_list=table)


@bp.route('/<string:player_id>', methods=['GET'])
def player_info(player_id):
    player_data = Player.info(player_id)[0][1:]
    data = zip(['Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN'], player_data)
    column_names = ['Поле', 'Значення']
    table = render_table(column_names, data)
    return render_template('player.html', player=table, player_id=player_id)


@bp.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        return redirect('/players')

    city_data = City.get_columns('id', 'name')
    cities = render_select('city', city_data)
    return render_template('add_player.html', cities=cities)


@bp.route('/<string:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    if request.method == 'POST':
        return redirect(f'/players/{player_id}')
    player_data = Player.info(player_id)[0]
    cities = render_select('city', City.info())
    ranks = render_select('rank', Rank.info())
    national_ranks = render_select('national_rank', NationalRank.info())

    return render_template('edit_player.html', player_id=player_id, player_data=player_data, cities=cities, ranks=ranks,
                           national_ranks=national_ranks)
