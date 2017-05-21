import sys
import ui
import queries
from flask import Flask, render_template
import psycopg2
import sys


app = Flask(__name__)


def init():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        return conn
    except Exception as e:
        error_message = "Uh oh, can't connect. Invalid dbname, user or password? \n" + str(e)
        ui.print_error_message(error_message)
        sys.exit()


@app.route('/')
def handle_menu():
    title = 'Main menu'
    menu_items = [("A query that returns the 2 name columns of the given table","menu_name_columns"),
               ("A query that returns the nicknames of all mentors working at the given city","menu_nicknames"),
               ("A query that returns applicant data about given name in 2 columns: full_name, phone_number","menu_full_name_and_phone_from_fist_name"),
               ("A query that returns applicant data with given e-mail address","menu_applicant_from_email"),
               ("A query that returns applicant data after inserting it","menu_inserted_applicant_data"),
               ("A query that returns applicant data after updating it","menu_updated_applicant_data"),
               ("A query that removes all applicants with given e-mail domain","menu_remove_applicants_by_email_domain")]
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/menu_name_columns')
def menu_name_columns():
    title = 'Name columns menu'
    menu_items = [('mentors', '/get_name_columns/mentors'),
                  ('applicants', '/get_name_columns/applicants')]
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/get_name_columns/<table>')
def get_name_columns(table):
    conn = init()
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name FROM "{}"'.format(table)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    title = 'The 2 name columns of the {} table:'.format(table)
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


@app.route('/menu_nicknames')
def menu_nicknames():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT city FROM mentors;""")
    rows = cursor.fetchall()
    cities = [city[0] for city in rows]
    cursor.close()
    conn.close()
    title = 'From which city do you want the nicknames of the mentors?'
    menu_items = []
    for city in cities:
        menu_items.append((city, '/get_nicknames/{}'.format(city)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/get_nicknames/<city>')
def get_nicknames(city):
    conn = init()
    cursor = conn.cursor()
    query = "SELECT nick_name FROM mentors WHERE city='{}'".format(city)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    title = 'The nick_name-s of all mentors working at {}'.format(city)
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


'''
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
        ui.print_result(
            column_names, rows, 'Applicant data about {} in 2 columns: full_name, phone_number'.format(name))
    cursor.close()
    conn.close()
    return
'''


'''
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
        ui.print_result(
            column_names, rows, 'Applicant data about {} in 2 columns: full_name, phone_number'.format(name))
    cursor.close()
    conn.close()
    return
'''


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
