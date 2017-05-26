from flask import Flask, render_template, request, redirect, Blueprint
import data_manager

part2_routes = Blueprint('part2_routes', '__name__', template_folder='templates', static_folder='static')


@part2_routes.route('/')
def handle_menu():
    title = 'Main menu'
    menu_items = [("A query that returns the first name and the code of the applicants plus the name of the assigned mentor", "applicants-and-mentors"),
               ("A query that returns the first name and the code of the applicants plus the creation_date of the application", "applicants"),
               ("A query that returns the name of the school plus the name of contact person at the school", "contacts"),
               ("A query that returns the number of the mentors per country", "mentors-by-country"),
               ("A query that returns the name of the mentors plus the name and country of all the schools", "all-school"),
               ("A query that returns the name of the mentors plus the name and country of the school", "mentors"),
               ("A query that returns the 2 name columns of the given table","menu_name_columns"),
               ("A query that returns the nicknames of all mentors working at the given city","menu_nicknames"),
               ("A query that returns applicant data about given name in 2 columns: full_name, phone_number","menu_full_name_and_phone_from_fist_name"),
               ("A query that returns applicant data with given e-mail address","menu_applicant_from_email"),
               ("A query that returns applicant data after inserting it","menu_insert_applicant_data"),
               ("A query that returns applicant data after updating it","menu_update_applicant_data"),
               ("A query that removes all applicants with given e-mail domain","menu_remove_applicants_by_email_domain")]
    return render_template('menu.html', title=title, menu_items=menu_items)


@part2_routes.route("/mentors")
def mentors():
    '''
    Mentors and schools page [/mentors]
    On this page you should show the result of a query
    that returns the name of the mentors plus the name and country of the school
    (joining with the schools table) ordered by the mentors id column
    (columns: mentors.first_name, mentors.last_name, schools.name, schools.country).
    '''
    query = "SELECT mentors.first_name, mentors.last_name, schools.name, schools.country \
             FROM mentors LEFT JOIN schools \
             ON mentors.city=schools.city \
             ORDER BY mentors.id;"
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The name of the mentors plus the name and country of the school'
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])


@part2_routes.route("/all-school")
def all_school():
    '''
    All school page [/all-school]
    On this page you should show the result of a query 
    that returns the name of the mentors plus the name and country of the school
    (joining with the schools table) ordered by the mentors id column.
    BUT include all the schools, even if there's no mentor yet!
    columns: mentors.first_name, mentors.last_name, schools.name, schools.country
    '''
    query = 'SELECT mentors.first_name, mentors.last_name, schools.name, schools.country \
             FROM mentors FULL JOIN schools ON mentors.city=schools.city \
             ORDER BY mentors.id;'
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The name of the mentors plus the name and country of all the schools'
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])


@part2_routes.route("/mentors-by-country")
def mentors_by_country():
    '''
    Contacts page [/mentors-by-country]
    On this page you should show the result of a query
    that returns the number of the mentors per country ordered by the name of the countries
    columns: country, count
    '''
    query = 'SELECT country, COUNT(mentors.id) AS count \
             FROM schools RIGHT JOIN mentors ON schools.city=mentors.city \
             GROUP BY schools.country \
             ORDER BY schools.country;'
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The number of the mentors per country'
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])


@part2_routes.route("/contacts")
def contacts():
    '''
    Contacts page [/contacts]
    On this page you should show the result of a query
    that returns the name of the school plus the name of contact person at the school (from the mentors table)
    ordered by the name of the school
    columns: schools.name, mentors.first_name, mentors.last_name
    '''
    query = 'SELECT schools.name, mentors.first_name, mentors.last_name \
             FROM schools LEFT JOIN mentors ON schools.city = mentors.city \
             ORDER BY schools.name;'
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The name of the school plus the name of contact person at the school'
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])


@part2_routes.route("/applicants")
def applicants():
    '''
    Applicants page [/applicants]
    On this page you should show the result of a query
    that returns the first name and the code of the applicants plus the creation_date of the application
    (joining with the applicants_mentors table)
    ordered by the creation_date in descending order
    BUT only for applications later than 2016-01-01
    columns: applicants.first_name, applicants.application_code, applicants_mentors.creation_date
    '''
    query = "SELECT applicants.first_name, applicants.application_code, applicants_mentors.creation_date \
             FROM applicants LEFT JOIN applicants_mentors ON applicants.id=applicants_mentors.applicant_id \
             WHERE applicants_mentors.creation_date > '2016-01-01' \
             ORDER BY applicants_mentors.creation_date DESC;"
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The first name and the code of the applicants plus the creation_date of the application'
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])


@part2_routes.route("/applicants-and-mentors")
def applicants_and_mentors():
    '''
    Applicants and mentors page [/applicants-and-mentors]
    On this page you should show the result of a query
    that returns the first name and the code of the applicants plus the name of the assigned mentor
    (joining through the applicants_mentors table)
    ordered by the applicants id column
    Show all the applicants, even if they have no assigned mentor in the database!
    In this case use the string 'None' instead of the mentor name
    columns: applicants.first_name, applicants.application_code, mentor_first_name, mentor_last_name
    '''
    query = "SELECT applicants.first_name, applicants.application_code, \
             COALESCE (mentors.first_name, 'None') AS mentor_first_name, \
             COALESCE (mentors.last_name, 'None') AS mentor_last_name \
             FROM applicants LEFT JOIN applicants_mentors ON applicants.id=applicants_mentors.applicant_id \
             LEFT JOIN mentors ON applicants_mentors.mentor_id=mentors.id \
             ORDER BY applicants.id;"
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        title = 'The first name and the code of the applicants plus the name of the assigned mentor'
        return render_template('result.html',
                               title=title,
                               column_names=result['column_names'],
                               rows=result['rows'],
                               row_count=result['row_count'])
    else:
        return render_template('error.html', error=result['result'])
