import psycopg2


def get_name_columns():
    try:
        connect_str = "dbname='en' user='en' host='localhost'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mentors;""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    finally:
        return


def get_nicknames():
    pass


def get_full_name_and_phone_from_fist_name():
    pass


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
