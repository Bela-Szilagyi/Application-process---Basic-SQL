import psycopg2
import ui


def get_name_columns():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""SELECT first_name, last_name FROM mentors;""")
        rows = cursor.fetchall()
        ui.print_result(rows, 'The 2 name columns of the mentors table:')
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    finally:
        return


def get_nicknames():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""SELECT nick_name FROM mentors WHERE city='Miskolc';""")
        rows = cursor.fetchall()
        ui.print_result(rows, 'The nick_name-s of all mentors working at Miskolc')
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    finally:
        return


def get_full_name_and_phone_from_fist_name():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name", phone_number
                       FROM applicants WHERE first_name='Carol';""")
        rows = cursor.fetchall()
        ui.print_result(rows, 'Applicant data about Carol in 2 columns: full_name, phone_number')
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    finally:
        return


def get_applicant_from_e_mail():
    pass


def get_inserted_applicant_data():
    pass


def get_updated_applicant_phone():
    pass


def get_remove_applicants_by_e_mail():
    pass


def main():
    pass

if __name__ == '__main__':
    main()
