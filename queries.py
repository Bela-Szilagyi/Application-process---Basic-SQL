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
    tables = ['mentors', 'applicants']
    ui.print_menu('From which table do you want the 2 name columns?', tables, 'Return to main menu')
    answers = list(range(len(tables)+1))
    answer = ''
    while answer not in answers:
        answer = ui.get_predefined_type_input("Please enter a number: ", int)
    if answer != 0:
        table = tables[answer-1]
        query = 'SELECT first_name, last_name FROM "{}"'.format(table)
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        ui.print_result(column_names, rows, 'The 2 name columns of the {} table:'.format(table))
    cursor.close()
    conn.close()
    return


def get_nicknames():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT city FROM mentors;""")
    rows = cursor.fetchall()
    cities = [city[0] for city in rows]
    ui.print_menu('From which city do you want the nicknames of the mentors?', cities, 'Return to main menu')
    answers = list(range(len(cities)+1))
    answer = ''
    while answer not in answers:
        answer = ui.get_predefined_type_input("Please enter a number: ", int)
    if answer != 0:
        city = cities[answer-1]
        cursor.execute("SELECT nick_name FROM mentors WHERE city=%s", (city, ))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        ui.print_result(column_names, rows, 'The nick_name-s of all mentors working at {}'.format(city))
    cursor.close()
    conn.close()
    return


def get_full_name_and_phone_from_fist_name():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT first_name FROM applicants;""")
    rows = cursor.fetchall()
    names = [name[0] for name in rows]
    ui.print_menu('Which applicant\'s name and phone number do you want to know?', names, 'Return to main menu')
    answers = list(range(len(names)+1))
    answer = ''
    while answer not in answers:
        answer = ui.get_predefined_type_input("Please enter a number: ", int)
    if answer != 0:
        name = names[answer-1]
        cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name", phone_number
                       FROM applicants WHERE first_name=%s;""", (name, ))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        ui.print_result(column_names, rows, 'Applicant data about {} in 2 columns: full_name, phone_number'.format(name))
    cursor.close()
    conn.close()
    return


def get_applicant_from_e_mail():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT email FROM applicants;""")
    rows = cursor.fetchall()
    emails = [email[0] for email in rows]
    chopped_emails = []
    for email in emails:
        while email[0] != '@':
            email = email[1:]
        chopped_emails.append(email)
    ui.print_menu('Which e-mail address data do you want to know?', chopped_emails, 'Return to main menu')
    answers = list(range(len(chopped_emails)+1))
    answer = ''
    while answer not in answers:
        answer = ui.get_predefined_type_input("Please enter a number: ", int)
    if answer != 0:
        email = '%' + chopped_emails[answer-1]
        cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name", phone_number
                        FROM applicants WHERE email LIKE %s;""", (email, ))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        ui.print_result(column_names, rows, 'Applicant data for {} e-mail address'.format(email))
    cursor.close()
    conn.close()
    return


def get_inserted_applicant_data():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM applicants;""")
    column_names = [desc[0] for desc in cursor.description][1:-1]
    predefined_applicaton_data = ("Markus", "Schaffarzyk", "003620/725-2666", "djnovus@groovecoverage.com", )
    application_datas = []
    for i, column_name in enumerate(column_names):
        application_datas.append(ui.get_predefined_type_input(column_name + '(if {}, press enter)? '.format(predefined_applicaton_data[i]), str))
    for i in range(len(application_datas)):
        if application_datas[i] == '':
            application_datas[i] = predefined_applicaton_data[i]
    print(application_datas)
    cursor.execute("""SELECT application_code FROM applicants;""")
    rows = cursor.fetchall()
    predefined_application_code = 54823
    application_codes = [code[0] for code in rows]
    while predefined_application_code in application_codes:
        predefined_application_code += 1
    SQL = "INSERT INTO applicants (first_name, last_name, phone_number, email, application_code) VALUES (%s, %s, %s, %s, %s);"
    data = (application_datas[0], application_datas[1], application_datas[2], application_datas[3], predefined_application_code, )
    cursor.execute(SQL, data)
    cursor.execute("""SELECT * FROM applicants WHERE application_code=%s;""", (predefined_application_code, ))
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
