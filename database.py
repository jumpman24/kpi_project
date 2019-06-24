import mysql.connector
import os
import datetime

MYSQL_CONFIG = {
    'user': 'is8204',
    'password': os.environ.get('MYSQL_PASSWORD'),
    'host': 'zanner.org.ua',
    'port': '33321',
    'database': 'is8204',
}


def execute_query(query):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    print(query)
    cursor.execute(query)

    results = []
    for row in cursor:
        results.append(row)

    connection.commit()

    if query.strip().startswith('INSERT'):
        results = cursor.lastrowid

    cursor.close()
    connection.close()

    return results


def execute_procedure(procedure_name):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    print(f"CALL {procedure_name}();")
    cursor.callproc(procedure_name)

    connection.commit()

    cursor.close()
    connection.close()


def prep_string(value):
    if not value:
        return 'NULL'

    value = value.replace("'", "\\'")
    return f"'{value}'"


def prep_float(value):
    if value is None or value == '':
        return 'NULL'

    value = float(value)
    return f"{value:.3f}"


def prep_int(value):
    if value is None or value == '':
        return 'NULL'

    return f"{int(value)}"


def prep_bool(value):
    return '1' if value else '0'


def prep_date(value):
    if not value:
        return 'NULL'

    value = datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
    return f"'{value}'"
