import datetime

import mysql.connector
from flask import Blueprint, render_template, url_for, request, redirect, flash

from models import City, TournamentTable
from queries import (
    select_tournament_query,
    insert_tournament_query,
    update_tournament_query,
    select_pairing_query,
)
from utils import (
    render_table,
    render_link,
    render_text_input_row,
    render_select_row,
    render_checkbox_row,
    render_date_row,
    render_file_row,
    render_submit
)

from parser import parse_tournament_table

bp = Blueprint('tournaments', __name__, url_prefix='/tournaments')
ALLOWED_EXTENSIONS = {'txt', 'csv'}
TOURNAMENT_LIST_ATTRS = ['name', 'city.name', 'date_start', 'date_end', 'pin', 'is_ranked']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['GET'])
def tournaments():
    tournament_list = select_tournament_query()
    table_data = []
    for idx, tournament in enumerate(tournament_list, start=1):
        tr_data = [render_link(url_for('.tournament_info', tournament_id=tournament.id), idx),
                   render_link(url_for('.tournament_info', tournament_id=tournament.id), tournament.name)]
        tr_data.extend(tournament.get_attrs('city.name', 'date_start', 'date_end', 'pin', 'is_ranked'))
        table_data.append(tr_data)

    column_names = ['№ з/п', 'Назва', 'Місто', 'Дата початку', 'Дата завершення', 'PIN', 'Рейтинговий']
    table = render_table(column_names, table_data)
    return render_template('tournament_list.html', table=table)


@bp.route('/<string:tournament_id>', methods=['GET'])
def tournament_info(tournament_id):
    tournament = select_tournament_query(tournament_id)[0]
    pairings = select_pairing_query(tournament_id)
    tournament_table, length = TournamentTable(tournament, pairings).get_table()
    return render_template('tournament_info.html', tournament=tournament, table=tournament_table, length=length)


@bp.route('/<string:tournament_id>/edit', methods=['GET', 'POST'])
def edit_tournament(tournament_id):
    edit_url = url_for('.edit_tournament', tournament_id=tournament_id)

    if request.method == 'POST':
        update_data = dict(request.form)
        update_data['is_ranked'] = 'is_ranked' in update_data.keys()
        update_data['date_start'] = request.form.getlist('date_start')[0]
        update_data['date_end'] = request.form.getlist('date_end')[0]
        try:
            update_tournament_query(tournament_id, **update_data)
            flash('Дані турніру оновлені', 'isa_success')
            return redirect(url_for('.tournament_info', tournament_id=tournament_id))
        except mysql.connector.Error as err:
            flash(err.msg, 'isa_error')

        return redirect(edit_url)

    tournament = select_tournament_query(tournament_id)[0]
    cities = City.select_attrs(['id', 'name'])

    form = '\n'.join([
        '<div class="container">',
        f'<form action="{edit_url}" method="post">',
        render_text_input_row("name", "Назва", tournament.name),
        render_select_row('city_id', "Місто", cities, tournament.city.id),
        render_date_row('date_start', 'Дата початку', tournament.date_start),
        render_date_row('date_end', 'Дата закінчення', tournament.date_end),
        render_text_input_row("pin", "EGF PIN", tournament.pin),
        render_checkbox_row('is_ranked', "Рейтинговий", tournament.is_ranked),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('edit_tournament.html', tournament=tournament, form=form)


@bp.route('/add', methods=['GET', 'POST'])
def add_tournament():
    add_url = url_for('.add_tournament')

    if request.method == 'POST':
        file = request.files['file']

        filename = file.filename
        if not filename:
            flash('Додайте файл з турнірними даними', 'isa_warning')
            return redirect(url_for('.add_tournament'))

        if not allowed_file(filename):
            flash('Файл має бути текстовим', 'isa_error')
            return redirect(url_for('.add_tournament'))

        update_data = dict(request.form)
        update_data['is_ranked'] = 'is_ranked' in update_data.keys()
        update_data['date_start'] = request.form.getlist('date_start')[0]
        update_data['date_end'] = request.form.getlist('date_end')[0]
        tournament_id = insert_tournament_query(**update_data)
        parse_tournament_table(file.read(), tournament_id, 0, 1, 2, 3, 4, 5, 7, 11)
        return redirect(url_for('.tournament_info', tournament_id=tournament_id))

    cities = City.select_attrs(['id', 'name'])

    form = '\n'.join([
        '<div class="container">',
        f'<form action="{add_url}" enctype="multipart/form-data" method="post">',
        render_text_input_row("name", "Назва"),
        render_select_row('city_id', "Місто", cities),
        render_date_row('date_start', 'Дата початку', str(datetime.date.today())),
        render_date_row('date_end', 'Дата закінчення', str(datetime.date.today())),
        render_text_input_row("pin", "EGF PIN"),
        render_checkbox_row('is_ranked', "Рейтинговий"),
        render_file_row('file', 'Файл'),
        render_submit(),
        '</form>',
        '</div>',
    ])

    return render_template('add_tournament.html', form=form)
