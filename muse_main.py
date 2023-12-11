import sqlite3
import requests
from datetime import datetime

conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

cursor.execute('''
   CREATE TABLE IF NOT EXISTS job_postings (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       job_category TEXT,
       job_listing TEXT,
       publication_date TEXT,
       experience_level TEXT
   )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS last_processed_page (
        id INTEGER PRIMARY KEY,
        page_number INTEGER
    )
''')

def get_last_processed_page(cursor):
    cursor.execute("SELECT page_number FROM last_processed_page WHERE id = 1")
    result = cursor.fetchone()
    return result[0] if result else 0

def update_last_processed_page(cursor, page_number):
    cursor.execute("INSERT OR REPLACE INTO last_processed_page (id, page_number) VALUES (1, ?)", (page_number,))

unique_job_listings = set()

last_processed_page = get_last_processed_page(cursor)
max_pages = 10
rows_to_fetch = 25
page_count = last_processed_page + 1

while page_count <= max_pages and len(unique_job_listings) < rows_to_fetch:
    res = requests.get(f'https://www.themuse.com/api/public/jobs?page={page_count}')
    data = res.json()

    lists = data['results']
    for item in lists:
        publication_date = datetime.strptime(item['publication_date'], '%Y-%m-%dT%H:%M:%SZ')
        formatted_date = publication_date.strftime('%B %d, %Y')
        job_listing = item.get('name', 'N/A')

        if job_listing not in unique_job_listings:
            job_category = item.get('category', 'N/A')
            experience_level = item.get('level', 'N/A')

            cursor.execute('''
                INSERT INTO job_postings (job_category, job_listing, publication_date, experience_level)
                VALUES (?, ?, ?, ?)
            ''', (job_category, job_listing, formatted_date, experience_level))
            unique_job_listings.add(job_listing)

            if len(unique_job_listings) >= rows_to_fetch:
                break

    if len(unique_job_listings) >= rows_to_fetch:
        break

    page_count += 1

update_last_processed_page(cursor, page_count)
conn.commit()
conn.close()
