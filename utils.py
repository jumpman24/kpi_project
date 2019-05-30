def make_attrs(**attrs):
    data = []
    for key, value in attrs.items():
        data.append(f'{key}="{value}"')

    if data:
        return ' ' + ' '.join(data)

    return ''


def make_table_header(values, header_attrs):
    attrs = make_attrs(**header_attrs)
    body = [f"<th{attrs}>{value}</th>" for value in values]
    body_string = '\n'.join(body)
    return '\n'.join(['<tr>', body_string, '</tr>'])


def make_table_row(values, row_attrs):
    attrs = make_attrs(**row_attrs)
    body = [f"<td{attrs}>{value}</td>" for value in values]
    body_string = '\n'.join(body)
    return '\n'.join(['<tr>', body_string, '</tr>'])


def render_table(column_names, rows, table_attrs=None, header_attrs=None, row_attrs=None):
    table_attrs = table_attrs or {'class': 'ugd_table'}
    header_attrs = header_attrs or {}
    row_attrs = row_attrs or {}
    attrs = make_attrs(**table_attrs)
    table_data = [make_table_header(column_names, header_attrs)]
    for row in rows:
        table_data.append(make_table_row(row, row_attrs))

    return '\n'.join([f'<table{attrs}>', '\n'.join(table_data), '</table>'])


def render_select(name, values):
    data = []
    for idx, value in values:
        data.append(f'<option value="{idx}">{value}</option>')

    return '\n'.join([f'<select name={name}>', '\n'.join(data), '</select>'])
