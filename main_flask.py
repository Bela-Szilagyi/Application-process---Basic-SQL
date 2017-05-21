import sys
import ui
import queries
from flask import Flask, render_template

app = Flask(__name__)


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
    menu_items = [('mentors', 'mentors'),
                  ('applicants', 'applicants')]
    return render_template('menu.html', title=title, menu_items=menu_items)


'''
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
'''


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
