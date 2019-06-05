from flask import Blueprint, render_template, request, redirect
from models import Tournament, City
from utils import render_table, render_link, render_select, render_input, render_label, render_row

bp = Blueprint('tournaments', __name__, url_prefix='/tournaments')


@bp.route('/', methods=['GET'])
def tournaments():
    tournament_list = Tournament.info()
    tournament_ids = []
    table_data = []
    for idx, row in enumerate(tournament_list, start=1):
        tournament_ids.append(row[0])
        table_data.append([idx, render_link(f"/tournaments/{row[0]}", row[1])] + list(row)[2:])

    column_names = ['№ з/п', 'Назва', 'Місто', 'Дата початку', 'Дата завершення', 'PIN']
    table = render_table(column_names, table_data)
    return render_template('tournaments.html', table=table)
