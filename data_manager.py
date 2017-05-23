import psycopg2
import sys


def handle_database(command):
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(command)
        if "SELECT" in command:
            result = {}
            result['rows'] = cursor.fetchall()
            result['column_names'] = [desc[0] for desc in cursor.description]
            result['row_count'] = cursor.rowcount
            return result
        cursor.close()
        conn.close()
    except Exception as e:
        error_message = "Uh oh, can't connect. Invalid dbname, user or password? \n" + str(e)
        print(error_message)
        sys.exit()
