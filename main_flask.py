import sys
import ui
import queries
from flask import Flask, render_template, request, redirect
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
               ("A query that returns applicant data after inserting it","menu_insert_applicant_data"),
               ("A query that returns applicant data after updating it","menu_update_applicant_data"),
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


@app.route('/menu_full_name_and_phone_from_fist_name')
def menu_full_name_and_phone_from_fist_name():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT first_name FROM applicants;""")
    rows = cursor.fetchall()
    names = [name[0] for name in rows]
    cursor.close()
    conn.close()
    title = 'Which applicant\'s name and phone number do you want to know?'
    menu_items = []
    for name in names:
        menu_items.append((name, '/get_full_name_and_phone_from_fist_name/{}'.format(name)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/get_full_name_and_phone_from_fist_name/<name>')
def get_full_name_and_phone_from_fist_name(name):
    conn = init()
    cursor = conn.cursor()
    query = "SELECT CONCAT (first_name, ' ', last_name) AS full_name, phone_number FROM applicants WHERE first_name='{}'".format(name)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    title = 'Applicant data about {} in 2 columns: full_name, phone_number'.format(name)
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


@app.route('/menu_applicant_from_email')
def menu_applicant_from_email():
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
    cursor.close()
    conn.close()
    title = 'Which e-mail address data do you want to know?'
    menu_items = []
    for email in chopped_emails:
        menu_items.append((email, '/get_applicant_from_email/{}'.format(email)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/get_applicant_from_email/<email>')
def get_applicant_from_email(email):
    conn = init()
    cursor = conn.cursor()
    email = '%' + email
    query = "SELECT CONCAT (first_name, ' ', last_name) AS full_name, phone_number FROM applicants WHERE email LIKE '{}'".format(email)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()    
    title = 'Applicant data for {} e-mail address'.format(email)
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


@app.route("/menu_insert_applicant_data")
def menu_insert_applicant_data():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT application_code FROM applicants;""")
    rows = cursor.fetchall()
    application_codes = [code[0] for code in rows]
    application_code = max(application_codes) + 1
    cursor.execute("""SELECT * FROM applicants;""")
    title = "Application form"
    column_names = [desc[0] for desc in cursor.description][1:-1]
    # predefined_applicaton_data = ("Markus", "Schaffarzyk", "003620/725-2666", "djnovus@groovecoverage.com", )
    return render_template('empty_applicant_form.html', title=title, column_names=column_names, code=application_code)


@app.route("/get_inserted_applicant_data")
def get_inserted_applicant_data():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    email = request.args.get('email')
    application_code = request.args.get('code')
    SQL = "INSERT INTO applicants (first_name, last_name, phone_number, email, application_code) VALUES (%s, %s, %s, %s, %s);"
    data = (first_name, last_name, phone_number, email, application_code)
    conn = init()
    cursor = conn.cursor()
    cursor.execute(SQL, data)
    cursor.execute("""SELECT * FROM applicants WHERE application_code=%s;""", (application_code, ))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    title = 'Applicant data after inserting'
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


@app.route("/menu_update_applicant_data")
def menu_update_applicant_data():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT CONCAT (first_name, ' ', last_name) AS "full_name" FROM applicants ORDER BY id;""")
    rows = cursor.fetchall()
    names = [name[0] for name in rows]
    title = 'Which applicant\'s data do you want to update?'
    menu_items = []
    for name in names:
        menu_items.append((name, '/update_applicant_data/{}'.format(name)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/update_applicant_data/<name>')
def updated_applicant_data(name):
    conn = init()
    cursor = conn.cursor()
    query = "SELECT first_name, last_name, phone_number, email, application_code FROM applicants WHERE CONCAT (first_name, ' ', last_name) = '{}'".format(name)
    cursor.execute(query)
    rows = cursor.fetchall()
    datas = []
    datas.append(('first_name', rows[0][0]))
    datas.append(('last_name', rows[0][1]))
    datas.append(('phone_number', rows[0][2]))
    datas.append(('email', rows[0][3]))
    application_code = rows[0][4]
    cursor.close()
    conn.close()
    title = 'Appllication form'
    return render_template('filled_applicant_form.html', title=title, datas=datas, code=application_code)


@app.route("/get_updated_applicant_data")
def get_updated_applicant_data():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    email = request.args.get('email')
    application_code = request.args.get('code')
    SQL = "UPDATE applicants SET first_name=%s, last_name=%s, phone_number=%s, email=%s WHERE application_code=%s"
    data = (first_name, last_name, phone_number, email, application_code)
    conn = init()
    cursor = conn.cursor()
    cursor.execute(SQL, data)
    cursor.execute("""SELECT * FROM applicants WHERE application_code=%s;""", (application_code, ))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    title = 'Applicant data after update'
    return render_template('result.html', title=title, column_names=column_names, rows=rows)


@app.route('/menu_remove_applicants_by_email_domain')
def menu_remove_applicants_by_email_domain():
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""SELECT email FROM applicants;""")
    rows = cursor.fetchall()
    emails = [email[0] for email in rows]
    chopped_emails = []
    for email in emails:
        while email[0] != '@':
            email = email[1:]
        email = email[1:]
        chopped_emails.append(email)
    chopped_emails = set(chopped_emails)
    cursor.close()
    conn.close()
    title = 'Choose domain which you want to remove'
    menu_items = []
    for email in chopped_emails:
        menu_items.append((email, '/remove_applicants_by_email_domain/{}'.format(email)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.route('/remove_applicants_by_email_domain/<domain>')
def remove_applicants_by_email_domain(domain):
    email = '%' + domain
    conn = init()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM applicants WHERE email LIKE %s;""", (email, ))
    cursor.close()
    conn.close()
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
