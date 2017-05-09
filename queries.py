import psycopg2
import ui
import sys


def init():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        return conn
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
        sys.exit()


def get_name_columns():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT first_name, last_name FROM mentors;""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'The 2 name columns of the mentors table:')
    cursor.close()
    conn.close()
    return


def get_nicknames():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT nick_name FROM mentors WHERE city='Miskolc';""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'The nick_name-s of all mentors working at Miskolc')
    cursor.close()
    conn.close()
    return


def get_full_name_and_phone_from_fist_name():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name", phone_number
                    FROM applicants WHERE first_name='Carol';""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'Applicant data about Carol in 2 columns: full_name, phone_number')
    cursor.close()
    conn.close()
    return


def get_applicant_from_e_mail():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name", phone_number
                    FROM applicants WHERE email LIKE '%@adipiscingenimmi.edu';""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'Applicant data with given e-mail address')
    cursor.close()
    conn.close()
    return


def get_inserted_applicant_data():
    conn = init()
    cursor = conn.cursor()
    SQL = "INSERT INTO applicants (first_name, last_name, phone_number, email, application_code) VALUES (%s, %s, %s, %s, %s);" # Note: no quotes
    data = ("Markus", "Schaffarzyk", "003620/725-2666", "djnovus@groovecoverage.com", "54823", )
    cursor.execute(SQL, data)
    cursor.execute("""SELECT * FROM applicants WHERE application_code='54823';""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'Applicant data after inserting it')
    cursor.close()
    conn.close()
    return


def get_updated_applicant_phone():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""UPDATE applicants SET phone_number = '003670/223-7459' WHERE first_name='Jemima' AND last_name='Foreman';""")
    cursor.execute("""SELECT phone_number FROM applicants WHERE first_name='Jemima' AND last_name='Foreman';""")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    ui.print_result(column_names, rows, 'Applicant data after inserting it')
    cursor.close()
    conn.close()
    return


def get_remove_applicants_by_e_mail():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM applicants WHERE email LIKE '%mauriseu.net';""")
    cursor.close()
    conn.close()
    return
