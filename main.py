import sys
import ui
import queries


def handle_menu():
    options = ["A query that returns the 2 name columns of the given table",
               "A query that returns the nicknames of all mentors working at the given city",
               "A query that returns applicant data about given name in 2 columns: full_name, phone_number",
               "A query that returns applicant data with given e-mail address",
               "A query that returns applicant data after inserting it",
               "A query that returns applicant phone number after updating it",
               "A query that removes all applicants with given e-mail domain"]

    ui.print_menu("Main menu", options, "Exit program")


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
        queries.get_applicant_from_e_mail()
    elif option == "5":
        queries.get_inserted_applicant_data()
    elif option == "6":
        queries.get_updated_applicant_phone()
    elif option == "7":
        queries.get_remove_applicants_by_e_mail()
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
    main()
