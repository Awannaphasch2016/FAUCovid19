import sqlite3
x = """
            CREATE TABLE IF NOT EXISTS {table} (
                PRIMARY KEY {table}
            );
    """

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                    {table} integer PRIMARY KEY
                                      , sentiment double
                                    , text STRING
                                    , date DATE
                                ); """
sql_add_data = """INSERT INTO projects (sentiment, text, date)
VALUES( 	0.100 , 'billionair', '2020-089-19');
"""

# sql_create_projects_table = """ CREATE TABLE projects (
#                                     {table} integer PRIMARY KEY
#                                       , sentiment double
#                                     , text STRING
#                                 ); """
# sql_add_data = """INSERT INTO projects (sentiment, text)
# VALUES( 	0.100 , 'billionair');"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except ValueError as e:
        raise ValueError(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except ValueError as e:
        raise ValueError(e)

def add_data(conn, add_data_sql):
    try:
        c = conn.cursor()
        c.execute(add_data_sql)
    except ValueError as e:

        raise ValueError(e)

if __name__== '__main__':
    conn = create_connection('test_db')
    # create_table(conn, x.format(table = 'Anak'))
    
    create_table(conn, sql_create_projects_table.format(table='Anak'))
    add_data(conn, sql_add_data )
    conn.commit()
    conn.close()

