import mysql.connector
from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for, flash

from models import City, Rank, NationalRank, Player
from queries import (
    select_participant_query,
)

from utils import (
    render_table,
    render_link,
    render_text_input_row,
    render_number_input_row,
    render_checkbox_row,
    render_select_row,
    render_submit
)

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('/', methods=['GET'])
def players():
    all_players = Player.select()
    table_data = []
    for idx, player in enumerate(all_players, start=1):
        player_data = player.get_attrs('full_name', 'city.name', 'rating', 'rank.name',
                                       'national_rank.abbreviate', 'pin', 'is_active')
        tr_data = [render_link(f"/players/{player.id}", idx)] + player_data
        tr_data[1] = render_link(f"/players/{player.id}", player.full_name)
        tr_data[-1] = 'Так' if tr_data[-1] else ''
        table_data.append(tr_data)

    column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN', 'Активний']
    table = render_table(column_names, table_data)
    return render_template('player_list.html', table=table)


@bp.route('/<int:player_id>', methods=['GET'])
def player_info(player_id):
    player = Player.select({'id': player_id})[0]
    participant = select_participant_query(player_id=player.id)
    return render_template('player_info.html', player=player, participant=participant)


@bp.route('/add', methods=['GET', 'POST'])
def add_player():
    error = None
    if request.method == 'POST':
        insert_data = dict(request.form)
        insert_data['is_active'] = 'is_active' in insert_data.keys()
        try:
            player_id = Player.execute_insert([insert_data])[0]
            flash('Гравець створений', 'isa_success')
            return redirect(url_for('.player_info', player_id=player_id))
        except mysql.connector.Error as err:
            flash(err.msg)

    cities = City.select_attrs(['id', 'name'])
    ranks = Rank.select_attrs(['id', 'name'])
    national_ranks = NationalRank.select_attrs(['id', 'name'])

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
        render_checkbox_row('is_active', "Активний"),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('add_player.html', form=form, error=error)


@bp.route('/<string:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    if request.method == 'POST':
        update_data = dict(request.form)
        update_data['is_active'] = 'is_active' in update_data.keys()
        try:
            Player.execute_update(player_id, **update_data)
            flash('Дані гравця оновлені', 'isa_success')
            return redirect(url_for('.players'))
        except mysql.connector.Error as err:
            flash(err.msg, 'isa_error')

        return redirect(url_for('.player_info', player_id=player_id))

    player = Player.select({'id': player_id})[0]

    cities = City.select_attrs(['id', 'name'])
    ranks = Rank.select_attrs(['id', 'name'])
    national_ranks = NationalRank.select_attrs(['id', 'name'])

    form = '\n'.join([
        '<div class="container">',
        f'<form action="/players/{player_id}/edit" method="post">',
        render_text_input_row("last_name", "Прізвище", player.last_name),
        render_text_input_row("first_name", "Ім'я", player.first_name),
        render_select_row('city_id', "Місто", cities, player.city.id),
        render_number_input_row('rating', "Рейтинг", '100', '3000', '0.001', player.rating),
        render_select_row('rank_id', "Ранг", ranks, player.rank.id),
        render_select_row('national_rank_id', "Розряд", national_ranks, player.national_rank.id),
        render_text_input_row("pin", "EGF PIN", player.pin),
        render_checkbox_row('is_active', "Активний", player.is_active),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('edit_player.html', player=player, form=form)


@bp.route('/<string:player_id>/delete', methods=['GET', 'POST'])
def delete_player(player_id):
    try:
        Player.execute_delete([player_id])
        flash('Гравець видалений', 'isa_success')
        return redirect(url_for('.players'))
    except mysql.connector.Error as err:
        flash(err.msg, 'isa_error')
        return redirect(url_for('.player_info', player_id=player_id))
