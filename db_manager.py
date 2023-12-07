import sqlite3
from datetime import datetime

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_sources_table(conn):
    sql = ''' CREATE TABLE IF NOT EXISTS sources (
                source_id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
              ); '''
    create_table(conn, sql)

def create_posts_table(conn):
    sql = ''' CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                content TEXT,
                timestamp TEXT,
                neutral_count INTEGER,
                negative_count INTEGER,
                positive_count INTEGER,
                FOREIGN KEY (source_id) REFERENCES sources (source_id)
              ); '''
    create_table(conn, sql)

def get_or_insert_source(conn, source_name):
    cur = conn.cursor()
    cur.execute("SELECT source_id FROM sources WHERE name = ?", (source_name,))
    source_id = cur.fetchone()
    if source_id:
        return source_id[0]

    cur.execute("INSERT INTO sources(name) VALUES(?)", (source_name,))
    conn.commit()
    return cur.lastrowid

def insert_post(conn, source_id, content, timestamp, neutral_count, negative_count, positive_count):
    formatted_timestamp = datetime.fromisoformat(timestamp.rstrip("Z")).strftime('%Y-%m-%d')
    sql = '''INSERT INTO posts(source_id, content, timestamp, neutral_count, negative_count, positive_count) VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (source_id, content, formatted_timestamp, neutral_count, negative_count, positive_count))
    conn.commit()
    return cur.lastrowid
