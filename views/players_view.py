from flask import Blueprint, render_template, request, redirect

from models import PlayerModel, City, Rank, NationalRank
from models.player import select_player
from utils import render_table, render_select, render_input, render_label, render_row, render_link

bp = Blueprint('players', __name__, url_prefix='/players')
PLAYER_ATTRS = ('full_name', 'city.name', 'rating', 'rank.name', 'national_rank.abbreviate', 'pin')


@bp.route('/', methods=['GET'])
def players():
    all_players = select_player()
    table_data = []
    for idx, player in enumerate(all_players, start=1):
        tr_data = [idx] + player.get_attrs(*PLAYER_ATTRS)
        tr_data[1] = render_link(f"/players/{player.id}", player.full_name)
        table_data.append(tr_data)

    column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN']
    table = render_table(column_names, table_data)
    return render_template('players.html', table=table)


@bp.route('/<string:player_id>', methods=['GET'])
def player_info(player_id):
    player_data = select_player(player_id)[0].get_attrs(*PLAYER_ATTRS)
    data = zip(['Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN'], player_data)
    column_names = ['Поле', 'Значення']
    table = render_table(column_names, data)
    return render_template('player.html', player_data=player_data, table=table, player_id=player_id)


@bp.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        return redirect('/players')

    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/add" method="post">',
        render_row(render_label('last_name', 'Прізвище', {'class': 'col-25'}),
                   render_input('text', {'name': 'last_name'}, {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('first_name', "Ім'я", {'class': 'col-25'}),
                   render_input('text', {'name': 'first_name'}, {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('city_id', "Місто", {'class': 'col-25'}),
                   render_select('city_id', City.info(), div_attrs={'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rating', "Рейтинг", {'class': 'col-25'}),
                   render_input('number',
                                {'name': 'rating', 'min': '100', 'max': '3000', 'step': '0.001'},
                                {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rank_id', "Ранг", {'class': 'col-25'}),
                   render_select('rank_id', Rank.info(), div_attrs={'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('national_rank_id', "Розряд", {'class': 'col-25'}),
                   render_select('national_rank_id', NationalRank.info(),
                                 div_attrs={'class': 'col-75'}),
                   {'class': 'row'}),
        render_row('', render_input('submit', {'value': 'Submit'}), {'class': 'row'}),
        '</form>',
        '</div>',
    ])

    return render_template('add_player.html', form=form)


@bp.route('/<string:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    if request.method == 'POST':
        request_form = request.form
        PlayerModel.update(player_id, **request_form)
        return redirect(f'/players/{player_id}')

    player_data = PlayerModel.info(player_id, False, True)[0]
    print(player_data)
    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/{player_id}/edit" method="post">',
        render_row(render_label('last_name', 'Прізвище', {'class': 'col-25'}),
                   render_input('text', {'name': 'last_name', 'value': player_data[1]},
                                {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('first_name', "Ім'я", {'class': 'col-25'}),
                   render_input('text', {'name': 'first_name', 'value': player_data[2]},
                                {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('city_id', "Місто", {'class': 'col-25'}),
                   render_select('city_id', City.info(), player_data[3], {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rating', "Рейтинг", {'class': 'col-25'}),
                   render_input('number', {'name': 'rating',
                                           'value': player_data[4],
                                           'min': '100',
                                           'max': '3000',
                                           'step': '0.001'},
                                {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('rank_id', "Ранг", {'class': 'col-25'}),
                   render_select('rank_id', Rank.info(), player_data[5], {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row(render_label('national_rank_id', "Розряд", {'class': 'col-25'}),
                   render_select('national_rank_id', NationalRank.info(), player_data[6],
                                 {'class': 'col-75'}),
                   {'class': 'row'}),
        render_row('', render_input('submit', {'value': 'Submit'}), {'class': 'row'}),
        '</form>',
        '</div>',
    ])

    return render_template('edit_player.html', player_data=player_data, form=form,
                           player_id=player_id)
