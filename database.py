import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "your_database_file.db"

    # SQL statement for creating a posts table
    sql_create_posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                        id integer PRIMARY KEY,
                                        source text NOT NULL,
                                        content text,
                                        timestamp text
                                    ); """

    # SQL statement for creating a word frequency table
    sql_create_word_freq_table = """CREATE TABLE IF NOT EXISTS word_frequency (
                                    id integer PRIMARY KEY,
                                    word text NOT NULL,
                                    frequency integer,
                                    post_id integer NOT NULL,
                                    FOREIGN KEY (post_id) REFERENCES posts (id)
                                );"""

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        # Create posts table
        create_table(conn, sql_create_posts_table)

        # Create word frequency table
        create_table(conn, sql_create_word_freq_table)

        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
 