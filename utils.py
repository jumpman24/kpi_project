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
    body = [f"<td{attrs}>{value if value is not None else ''}</td>" for value in values]
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


def render_input(type_, attrs: dict = None, div_attrs: dict = None, checked: bool = None, required=False):
    div_attrs = div_attrs or {'class': 'col-75'}
    checked = ' checked' if type_ == 'checkbox' and checked else ''
    required = ' reqiured' if required else ''
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<input type="{type_}"{make_attrs(attrs)}{checked}{required}>',
                      f"</div>"])


def render_label(for_, value, div_attrs: dict = None):
    div_attrs = div_attrs or {'class': 'col-25'}
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<label for="{for_}">{value}</label>',
                      f"</div>"])


def render_select(name, values, selected=None, div_attrs: dict = None):
    data = []
    div_attrs = div_attrs or {'class': 'col-75'}
    for item_id, value in values:
        if item_id == selected:
            data.append(f'<option selected value="{item_id}">{value}</option>')
        else:
            data.append(f'<option value="{item_id}">{value}</option>')

    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      f'<select name="{name}">',
                      f"<option{' selected' if selected else ''} value> -- Не обрано -- </option>\n",
                      '\n'.join(data),
                      '</select>',
                      f"</div>"])


def render_row(label, input, div_attrs: dict = None):
    div_attrs = div_attrs or {'class': 'row'}
    return '\n'.join([f"<div{make_attrs(div_attrs)}>",
                      label,
                      input,
                      f"</div>"])


def render_link(url, name):
    return f'<b><a href="{url}">{name}</a></b>'


def render_text_input_row(item_id: str, display_name: str, value: str = None, required=False):
    label = render_label(item_id, display_name)
    input_attrs = {'name': item_id}

    if value is not None:
        input_attrs['value'] = value

    input_field = render_input('text', input_attrs, required=required)

    return render_row(label, input_field)


def render_number_input_row(item_id: str, display_name: str, min_value: str = None, max_value: str = None,
                            step: str = None, value: str = None, required=False):
    label = render_label(item_id, display_name)
    input_attrs = {'name': item_id, 'min': min_value, 'max': max_value, 'step': step}

    if value is not None:
        input_attrs['value'] = value

    input_field = render_input('number', input_attrs)

    return render_row(label, input_field)


def render_checkbox_row(item_id: str, display_name: str, value: str = None):
    label = render_label(item_id, display_name)
    input_attrs = {'name': item_id, 'value': item_id}
    checkbox = render_input('checkbox', input_attrs, checked=value)

    return render_row(label, checkbox)


def render_select_row(item_id: str, display_name: str, values: list, selected: str = None):
    label = render_label(item_id, display_name)
    select = render_select(item_id, values, selected)

    return render_row(label, select)


def render_date_row(item_id: str, display_name: str, value: str = None):
    label = render_label(item_id, display_name)
    input_attrs = {'name': item_id, 'value': value}
    input_date = render_input('date', input_attrs)

    return render_row(label, input_date)


def render_file_row(item_id: str, display_name: str, required=False):
    label = render_label(item_id, display_name)
    input_file = render_input('file', {'name': item_id}, required=required)

    return render_row(label, input_file)


def render_submit():
    return render_row('', render_input('submit', {'value': 'Submit'}))
