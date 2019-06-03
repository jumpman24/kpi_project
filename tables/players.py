from flask_table import Table, Col, LinkCol

column_names = ['№ з/п', 'Прізвище та ім\'я', 'Місто', 'Рейтинг', 'Ранг', 'Розряд', 'PIN']


class PlayerTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    classes = ['ugd_table']
    table_id = 'player_list'

    counter = Col('№ з/п')
    full_name = LinkCol('Прізвище та ім\'я', '/player', url_kwargs=dict(player_id='player_id'))
    city = Col('Місто')
    rating = Col('Рейтинг')