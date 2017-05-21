import sys
import ui
import queries
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def handle_menu():
    title = 'Main menu'
    menu_items = [("A query that returns the 2 name columns of the given table","get_name_columns"),
               ("A query that returns the nicknames of all mentors working at the given city","get_nicknames"),
               ("A query that returns applicant data about given name in 2 columns: full_name, phone_number","get_full_name_and_phone_from_fist_name"),
               ("A query that returns applicant data with given e-mail address","get_applicant_from_email"),
               ("A query that returns applicant data after inserting it","get_inserted_applicant_data"),
               ("A query that returns applicant data after updating it","get_updated_applicant_data"),
               ("A query that removes all applicants with given e-mail domain","remove_applicants_by_email_domain")]
    return render_template('menu.html', title=title, menu_items=menu_items)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def choose():
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    if option == "1":
        queries.get_name_columns()
    elif option == "2":
        queries.get_nicknames()
    elif option == "3":
        queries.get_full_name_and_phone_from_fist_name()
    elif option == "4":
        queries.get_applicant_from_email()
    elif option == "5":
        queries.get_inserted_applicant_data()
    elif option == "6":
        queries.get_updated_applicant_data()
    elif option == "7":
        queries.remove_applicants_by_email_domain()
    elif option == "0":
        sys.exit(0)
    else:
        raise KeyError("There is no such option.")


def main():
    while True:
        handle_menu()
        try:
            choose()
        except KeyError as err:
            ui.print_error_message(err)


if __name__ == '__main__':
    app.run(debug=True)
