from flask import Blueprint, render_template, request, redirect

from models import (
    select_city,
    select_rank,
    select_national_rank,
    select_player,
    insert_player,
    update_player,
)
from utils import (
    render_table,
    render_link,
    render_text_input_row,
    render_number_input_row,
    render_select_row,
    render_submit
)

bp = Blueprint('players', __name__, url_prefix='/players')
PLAYER_INFO_ATTRS = ('full_name', 'city.name', 'rating', 'rank.name', 'national_rank.abbreviate', 'pin', 'is_active')
PLAYER_EDIT_ATTRS = ('last_name', 'first_name', 'rating', 'pin', 'is_active')
PLAYER_FOREIGN_KEYS = ('city.id', 'rank.id', 'national_rank.id')


@bp.route('/', methods=['GET'])
def players():
    all_players = select_player()
    table_data = []
    for idx, player in enumerate(all_players, start=1):
        tr_data = [idx] + player.get_attrs(*PLAYER_INFO_ATTRS)
        tr_data[1] = render_link(f"/players/{player.id}", player.full_name)
        table_data.append(tr_data)

    column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN']
    table = render_table(column_names, table_data)
    return render_template('players.html', table=table)


@bp.route('/<string:player_id>', methods=['GET'])
def player_info(player_id):
    player_data = select_player(player_id)[0].get_attrs(*PLAYER_INFO_ATTRS)
    data = zip(['Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN'], player_data)
    column_names = ['Поле', 'Значення']
    table = render_table(column_names, data)
    return render_template('player.html', player_data=player_data, table=table, player_id=player_id)


@bp.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        insert_player(**request.form)
        return redirect('/players')

    cities = [c.get_attrs('id', 'name') for c in select_city()]
    ranks = [r.get_attrs('id', 'name') for r in select_rank()]
    national_ranks = [nr.get_attrs('id', 'name') for nr in select_national_rank()]
    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/add" method="post">',
        render_text_input_row("last_name", "Прізвище"),
        render_text_input_row("first_name", "Ім'я"),
        render_select_row('city_id', "Місто", cities),
        render_number_input_row('rating', "Рейтинг", '100', '3000', '0.001'),
        render_select_row('rank_id', "Ранг", ranks),
        render_select_row('national_rank_id', "Розряд", national_ranks),
        render_text_input_row("pin", "EGF PIN"),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('add_player.html', form=form)


@bp.route('/<string:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    if request.method == 'POST':
        update_data = dict(request.form)
        update_data['player_id'] = player_id
        print(update_data)
        update_player(**update_data)
        return redirect(f'/players/{player_id}')

    player = select_player(player_id)[0]
    player_data = player.get_attrs(*PLAYER_EDIT_ATTRS)
    foreign_keys = player.get_attrs(*PLAYER_FOREIGN_KEYS)

    cities = [c.get_attrs('id', 'name') for c in select_city()]
    ranks = [r.get_attrs('id', 'name') for r in select_rank()]
    national_ranks = [nr.get_attrs('id', 'name') for nr in select_national_rank()]

    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/{player_id}/edit" method="post">',
        render_text_input_row("last_name", "Прізвище", player_data[0]),
        render_text_input_row("first_name", "Ім'я", player_data[1]),
        render_select_row('city_id', "Місто", cities, foreign_keys[0]),
        render_number_input_row('rating', "Рейтинг", '100', '3000', '0.001', player_data[2]),
        render_select_row('rank_id', "Ранг", ranks, foreign_keys[1]),
        render_select_row('national_rank_id', "Розряд", national_ranks, foreign_keys[2]),
        render_text_input_row("pin", "EGF PIN", player_data[3]),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('edit_player.html', player_data=player_data, form=form, player_id=player_id)
