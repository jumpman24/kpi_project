import mysql.connector
import os

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

    # print(query)
    cursor.execute(query)

    results = []
    for row in cursor:
        results.append(row)

    connection.commit()

    cursor.close()
    connection.close()

    return results


def prep_value(value=None, default='NULL'):
    if value is None:
        return default

    if isinstance(value, str):
        value = value.replace("'", "\\'")
        return f"'{value}'"

    if isinstance(value, bool):
        return f"{int(value)}"

    if isinstance(value, int):
        return f"{value}"

    if isinstance(value, float):
        return f"{value:.3f}"


def prep_string(value, default='NULL'):
    if value is None:
        return default
    value = value.replace("'", "\\'")
    return f"'{value}'"


def prep_float(value, default='NULL'):
    if value is None or value == '':
        return default

    value = float(value)
    return f"{value:.3f}"


def prep_int(value, default='NULL'):
    if value is None or value == '':
        return default

    value = int(value)
    return f"{value}"


def prep_bool(value, default='NULL'):
    if value is None:
        return default

    value = int(bool(value))
    return f"{value}"
