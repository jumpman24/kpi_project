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

    print(query)
    cursor.execute(query)

    results = []
    for row in cursor:
        results.append(row)

    connection.commit()

    cursor.close()
    connection.close()

    return results
