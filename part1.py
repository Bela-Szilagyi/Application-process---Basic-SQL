from flask import Flask, render_template, request, redirect, Blueprint
import data_manager

part1 = Blueprint('part1', '__name__', template_folder='templates', static_folder='static')


@part1.route('/menu_name_columns')
def menu_name_columns():
    title = 'Name columns menu'
    menu_items = [('mentors', '/get_name_columns/mentors'),
                  ('applicants', '/get_name_columns/applicants')]
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/get_name_columns/<table>')
def get_name_columns(table):
    query = 'SELECT first_name, last_name FROM "{}"'.format(table)
    result = data_manager.handle_database(query)
    title = 'The 2 name columns of the {} table:'.format(table)
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route('/menu_nicknames')
def menu_nicknames():
    query = 'SELECT DISTINCT city FROM mentors'
    result = data_manager.handle_database(query)
    cities = [city[0] for city in result['rows']]
    title = 'From which city do you want the nicknames of the mentors?'
    menu_items = []
    for city in cities:
        menu_items.append((city, '/get_nicknames/{}'.format(city)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/get_nicknames/<city>')
def get_nicknames(city):
    query = "SELECT nick_name FROM mentors WHERE city='{}'".format(city)
    result = data_manager.handle_database(query)
    title = 'The nick_name-s of all mentors working at {}'.format(city)
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route('/menu_full_name_and_phone_from_fist_name')
def menu_full_name_and_phone_from_fist_name():
    query = ('SELECT first_name FROM applicants')
    result = data_manager.handle_database(query)
    names = [name[0] for name in result['rows']]
    title = 'Which applicant\'s name and phone number do you want to know?'
    menu_items = []
    for name in names:
        menu_items.append((name, '/get_full_name_and_phone_from_fist_name/{}'.format(name)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/get_full_name_and_phone_from_fist_name/<name>')
def get_full_name_and_phone_from_fist_name(name):
    query = "SELECT CONCAT (first_name, ' ', last_name) AS full_name, phone_number FROM applicants WHERE first_name='{}'".format(name)
    result = data_manager.handle_database(query)
    title = 'Applicant data about {} in 2 columns: full_name, phone_number'.format(name)
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route('/menu_applicant_from_email')
def menu_applicant_from_email():
    query = ('SELECT email FROM applicants')
    result = data_manager.handle_database(query)
    emails = [email[0] for email in result['rows']]
    chopped_emails = []
    for email in emails:
        while email[0] != '@':
            email = email[1:]
        chopped_emails.append(email)
    title = 'Which e-mail address data do you want to know?'
    menu_items = []
    for email in chopped_emails:
        menu_items.append((email, '/get_applicant_from_email/{}'.format(email)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/get_applicant_from_email/<email>')
def get_applicant_from_email(email):
    email = '%' + email
    query = "SELECT CONCAT (first_name, ' ', last_name) AS full_name, phone_number FROM applicants WHERE email LIKE '{}'".format(email)
    result = data_manager.handle_database(query)
    title = 'Applicant data for {} e-mail address'.format(email[1:])
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route("/menu_insert_applicant_data")
def menu_insert_applicant_data():
    query = ('SELECT application_code FROM applicants')
    result = data_manager.handle_database(query)
    application_codes = [code[0] for code in result['rows']]
    application_code = max(application_codes) + 1
    query = ('SELECT * FROM applicants')
    result = data_manager.handle_database(query)
    title = "Application form"
    predefined_applicaton_data = ("Markus", "Schaffarzyk", "003620/725-2666", "djnovus@groovecoverage.com")
    columns = []
    for i, column in enumerate(result['column_names'][1:-1]):
        columns.append((column, predefined_applicaton_data[i]))
    return render_template('empty_applicant_form.html', title=title, column_names=columns, code=application_code, placeholders = predefined_applicaton_data)


@part1.route("/get_inserted_applicant_data")
def get_inserted_applicant_data():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    email = request.args.get('email')
    application_code = request.args.get('code')
    query = ("INSERT INTO applicants (first_name, last_name, phone_number, email, application_code) VALUES ('{}', '{}', '{}', '{}', '{}')".format(first_name, last_name, phone_number, email, application_code))
    result = data_manager.handle_database(query)
    if result['error'] != 'No error':
        return render_template('error.html', error=result['error'])
    query = ('SELECT * FROM applicants WHERE application_code={}'.format(application_code))
    result = data_manager.handle_database(query)
    title = 'Applicant data after inserting'
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route("/menu_update_applicant_data")
def menu_update_applicant_data():
    query = ("SELECT CONCAT (first_name, ' ', last_name) AS full_name FROM applicants ORDER BY id")
    result = data_manager.handle_database(query)
    names = [name[0] for name in result['rows']]
    title = 'Which applicant\'s data do you want to update?'
    menu_items = []
    for name in names:
        menu_items.append((name, '/update_applicant_data/{}'.format(name)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/update_applicant_data/<name>')
def updated_applicant_data(name):
    query = "SELECT first_name, last_name, phone_number, email, application_code FROM applicants WHERE CONCAT (first_name, ' ', last_name) = '{}'".format(name)
    result = data_manager.handle_database(query)
    datas = []
    datas.append(('first_name', result['rows'][0][0]))
    datas.append(('last_name', result['rows'][0][1]))
    datas.append(('phone_number', result['rows'][0][2]))
    datas.append(('email', result['rows'][0][3]))
    application_code = result['rows'][0][4]
    title = 'Appllication form'
    return render_template('filled_applicant_form.html', title=title, datas=datas, code=application_code)


@part1.route("/get_updated_applicant_data")
def get_updated_applicant_data():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    email = request.args.get('email')
    application_code = request.args.get('code')
    query = ("UPDATE applicants \
             SET first_name='{}', last_name='{}', phone_number='{}', email='{}' \
             WHERE application_code='{}'".format(first_name, last_name, phone_number, email, application_code))
    data_manager.handle_database(query)
    query = "SELECT * FROM applicants WHERE application_code='{}'".format(application_code)
    result = data_manager.handle_database(query)
    title = 'Applicant data after update'
    return render_template('result.html',
                           title=title,
                           column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])


@part1.route('/menu_remove_applicants_by_email_domain')
def menu_remove_applicants_by_email_domain():
    query = 'SELECT email FROM applicants'
    result = data_manager.handle_database(query)
    emails = [email[0] for email in result['rows']]
    chopped_emails = []
    for email in emails:
        while email[0] != '@':
            email = email[1:]
        email = email[1:]
        chopped_emails.append(email)
    chopped_emails = set(chopped_emails)
    title = 'Choose domain which you want to remove'
    menu_items = []
    for email in chopped_emails:
        menu_items.append((email, '/remove_applicants_by_email_domain/{}'.format(email)))
    return render_template('menu.html', title=title, menu_items=menu_items)


@part1.route('/remove_applicants_by_email_domain/<domain>')
def remove_applicants_by_email_domain(domain):
    email = '%' + domain
    query = "DELETE FROM applicants WHERE email LIKE '{}'".format(email)
    data_manager.handle_database(query)
    return redirect('/')
