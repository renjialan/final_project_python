import sqlite3

def create_table_in_unified_db(db_path, create_table_sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def fetch_data_from_db(db_path, query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_data_into_unified_db(db_path, data, insert_query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany(insert_query, data)
    conn.commit()
    conn.close()

# LinkedIn data
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS linkedin_titles (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
''')
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS linkedin_companies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
''')
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS linkedin_locations (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
''')
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS linkedin_jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_id INTEGER,
        company_id INTEGER,
        location_id INTEGER,
        apply_link TEXT,
        FOREIGN KEY (title_id) REFERENCES linkedin_titles (id),
        FOREIGN KEY (company_id) REFERENCES linkedin_companies (id),
        FOREIGN KEY (location_id) REFERENCES linkedin_locations (id)
    )
''')

#for Muse data
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS muse_job_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_category TEXT,
        job_listing TEXT,
        publication_date TEXT,
        experience_level TEXT
    )
''')

# tables for News API data
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS news_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        content TEXT,
        timestamp TEXT,
        neutral_count INTEGER,
        positive_count INTEGER,
        negative_count INTEGER
    )
''')
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS news_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        name TEXT
    )
''')

# Insert data LinkedIn tables
titles_data = fetch_data_from_db('linkedin-jobs.db', 'SELECT id, name FROM titles')
companies_data = fetch_data_from_db('linkedin-jobs.db', 'SELECT id, name FROM companies')
locations_data = fetch_data_from_db('linkedin-jobs.db', 'SELECT id, name FROM locations')
jobs_data = fetch_data_from_db('linkedin-jobs.db', 'SELECT title_id, company_id, location_id, apply_link FROM jobs')

insert_data_into_unified_db('unified_database.db', titles_data, 'INSERT INTO linkedin_titles (id, name) VALUES (?, ?)')
insert_data_into_unified_db('unified_database.db', companies_data, 'INSERT INTO linkedin_companies (id, name) VALUES (?, ?)')
insert_data_into_unified_db('unified_database.db', locations_data, 'INSERT INTO linkedin_locations (id, name) VALUES (?, ?)')
insert_data_into_unified_db('unified_database.db', jobs_data, 'INSERT INTO linkedin_jobs (title_id, company_id, location_id, apply_link) VALUES (?, ?, ?, ?)')

# InserMuse table
muse_data = fetch_data_from_db('muse_jobs.db', 'SELECT job_category, job_listing, publication_date, experience_level FROM job_postings')
insert_data_into_unified_db('unified_database.db', muse_data, '''
    INSERT INTO muse_job_postings (job_category, job_listing, publication_date, experience_level) VALUES (?, ?, ?, ?)
''')

# News AP
news_posts_data = fetch_data_from_db('news_database.db', 'SELECT source_id, content, timestamp, neutral_count, positive_count, negative_count FROM posts')
news_sources_data = fetch_data_from_db('news_database.db', 'SELECT source_id, name FROM sources')

insert_data_into_unified_db('unified_database.db', news_posts_data, '''
    INSERT INTO news_posts (source_id, content, timestamp, neutral_count, positive_count, negative_count) VALUES (?, ?, ?, ?, ?, ?)
''')
insert_data_into_unified_db('unified_database.db', news_sources_data, '''
    INSERT INTO news_sources (source_id, name) VALUES (?, ?)
''')
