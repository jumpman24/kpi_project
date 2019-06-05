def make_attrs(attrs: dict):
    if not attrs:
        return ''
    data = []
    for key, value in attrs.items():
        data.append(f'{key}="{value}"')

    return ' ' + ' '.join(data)


def make_table_header(values, header_attrs):
    attrs = make_attrs(header_attrs)
    body = [f"<th{attrs}>{value}</th>" for value in values]
    body_string = '\n'.join(body)
    return '\n'.join(['<tr>', body_string, '</tr>'])


def make_table_row(values, row_attrs):
    attrs = make_attrs(row_attrs)
    body = [f"<td{attrs}>{value}</td>" for value in values]
    body_string = '\n'.join(body)
    return '\n'.join(['<tr>', body_string, '</tr>'])


def render_table(column_names, rows, table_attrs=None, header_attrs=None, row_attrs=None):
    table_attrs = table_attrs or {'class': 'ugd_table'}
    header_attrs = header_attrs or {}
    row_attrs = row_attrs or {}
    table_data = [make_table_header(column_names, header_attrs)]
    for row in rows:
        table_data.append(make_table_row(row, row_attrs))

    return '\n'.join([f'<table{make_attrs(table_attrs)}>', '\n'.join(table_data), '</table>'])


def render_input(type_, attrs: dict = None, div_attrs: dict = None):
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<input type="{type_}" {make_attrs(attrs)}>',
                      f"</div>"])


def render_label(for_, value, div_attrs: dict = None):
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<label for="{for_}">{value}</label>',
                      f"</div>"])


def render_select(name, values, selected=None, div_attrs: dict = None):
    data = []
    for idx, value in values:
        if value == selected:
            data.append(f'<option selected value="{idx}">{value}</option>')
        else:
            data.append(f'<option value="{idx}">{value}</option>')

    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<select name="{name}">',
                      '\n'.join(data),
                      '</select>',
                      f"</div>"])


def render_row(label, input, div_attrs):
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      label,
                      input,
                      f"</div>"])


def render_link(url, name):
    return f'<b><a href="{url}">{name}</a></b>'
