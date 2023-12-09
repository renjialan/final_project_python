# This script migrates data from the Muse jobs database, the LinkedIn jobs database, and the News API database into a unified database.
# next steps: I have done calculations for news api in data_processing.py, but I have not done calculations for muse and linkedin.
# To run the code again i think i need to go to main.py to fetch data from news.api and run data_migration.py and data_processing.py
# 
# Run this script to get a unified databaseå
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

# Correct the CREATE TABLE statements to match your source table structures
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS muse_job_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_category TEXT,
        job_listing TEXT,
        publication_date TEXT,
        experience_level TEXT
    )
''')

create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS linkedin_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        apply_link TEXT
    )
''')
#news_api_table1
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
#news_api_table2
create_table_in_unified_db('unified_database.db', '''
    CREATE TABLE IF NOT EXISTS news_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        name TEXT
        
    )
''')

# Fetch and insert data from the first News API table
news_posts_data = fetch_data_from_db('database.db', 'SELECT source_id, content, timestamp, neutral_count, positive_count, negative_count FROM posts')
insert_data_into_unified_db('unified_database.db', news_posts_data, '''
    INSERT INTO news_posts (source_id, content, timestamp, neutral_count, positive_count, negative_count) VALUES (?, ?, ?, ?, ?, ?)
''')
# Fetch and insert data from the second News API table
news_sources_data = fetch_data_from_db('database.db', 'SELECT source_id, name FROM sources')
insert_data_into_unified_db('unified_database.db', news_sources_data, '''
    INSERT INTO news_sources (source_id, name) VALUES (?, ?)
''')



# Fetch and insert data from the Muse jobs database
muse_data = fetch_data_from_db('muse_jobs.db', 'SELECT job_category, job_listing, publication_date, experience_level FROM job_postings')
insert_data_into_unified_db('unified_database.db', muse_data, '''
    INSERT INTO muse_job_postings (job_category, job_listing, publication_date, experience_level) VALUES (?, ?, ?, ?)
''')

# Fetch and insert data from the LinkedIn jobs database
linkedin_data = fetch_data_from_db('linkedin-jobs.db', 'SELECT title, company, location, apply_link FROM jobs')
insert_data_into_unified_db('unified_database.db', linkedin_data, '''
    INSERT INTO linkedin_jobs (title, company, location, apply_link) VALUES (?, ?, ?, ?)
''')


