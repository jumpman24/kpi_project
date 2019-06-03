from flask import Blueprint, render_template, request, redirect
from models import Player, City, Rank, NationalRank
from utils import render_table, render_select, render_input, render_label, render_row

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
        player_info = request.form
        print(dict(player_info))
        Player.update(player_id, **player_info)
        return redirect(f'/players/{player_id}')

    player_data = Player.info(player_id, False, True)[0]

    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/{player_id}/edit" method="post">',
        render_row(render_label('last_name', 'Прізвище', {'class': 'col-25'}),
                   render_input('text', {'name': 'last_name', 'value': player_data[1]}, {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('first_name', "Ім'я", {'class': 'col-25'}),
                   render_input('text', {'name': 'first_name', 'value': player_data[2]}, {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('city_id', "Місто", {'class': 'col-25'}),
                   render_select('city_id', City.info(), player_data[3], {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rating', "Рейтинг", {'class': 'col-25'}),
                   render_input('number', {'name': 'rating', 'value': player_data[4], 'min': '100', 'max': '3000'},
                                {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rank_id', "Ранг", {'class': 'col-25'}),
                   render_select('rank_id', Rank.info(), player_data[5], {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('national_rank_id', "Розряд", {'class': 'col-25'}),
                   render_select('national_rank_id', NationalRank.info(), player_data[6], {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row('', render_input('submit', {'value': 'Submit'}), {'class': 'row'}),
        '</form>',
        '</div>',
    ])

    return render_template('edit_player.html',
                           player_id=player_id,
                           form=form)
