# please adjust this code so the publication_date information is in string format instead of tuple

import sqlite3
import requests
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

# Create a table for job postings if it doesn't exist
cursor.execute('''
   CREATE TABLE IF NOT EXISTS job_postings (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       job_category TEXT,
       job_listing TEXT,
       publication_date TEXT,
       experience_level TEXT
   )
''')

# Create a table to track the last processed page
cursor.execute('''
    CREATE TABLE IF NOT EXISTS last_processed_page (
        id INTEGER PRIMARY KEY,
        page_number INTEGER
    )
''')

# Function to get the last processed page
def get_last_processed_page(cursor):
    cursor.execute("SELECT page_number FROM last_processed_page WHERE id = 1")
    result = cursor.fetchone()
    return result[0] if result else 0

# Function to update the last processed page
def update_last_processed_page(cursor, page_number):
    cursor.execute("INSERT OR REPLACE INTO last_processed_page (id, page_number) VALUES (1, ?)", (page_number,))

# Initialize a set to track unique job listings
unique_job_listings = set()

# Fetch the last processed page
last_processed_page = get_last_processed_page(cursor)
max_pages = 10  # Max pages to scrape
rows_to_fetch = 25  # Number of rows to insert per run
page_count = last_processed_page + 1  # Start from the next page


# # Fetch and insert data
# while page_count <= max_pages and len(unique_job_listings) < rows_to_fetch:
#     res = requests.get(f'https://www.themuse.com/api/public/jobs?page={page_count}')
#     data = res.json()

#     lists = data['results']
#     for item in lists:
#         publication_date = datetime.strptime(item['publication_date'], '%Y-%m-%dT%H:%M:%SZ')
#         formatted_date = publication_date.strftime('%B %d, %Y')  # Change the format here
#         job_listing = item.get('name', 'N/A')

#         if job_listing not in unique_job_listings:
#             job_category = item.get('category', 'N/A')
#             experience_level = item.get('level', 'N/A')

#             cursor.execute('''
#                 INSERT INTO job_postings (job_category, job_listing, publication_date, experience_level)
#                 VALUES (?, ?, ?, ?)
#             ''', (job_category, job_listing, formatted_date, experience_level))
#             unique_job_listings.add(job_listing)

#             if len(unique_job_listings) >= rows_to_fetch:
#                 break

#     if len(unique_job_listings) >= rows_to_fetch:
#         break

#     page_count += 1

# Fetch and insert data
while page_count <= max_pages and len(unique_job_listings) < rows_to_fetch:
    res = requests.get(f'https://www.themuse.com/api/public/jobs?page={page_count}')
    data = res.json()

    lists = data['results']
    for item in lists:
        publication_date = datetime.strptime(item['publication_date'], '%Y-%m-%dT%H:%M:%SZ')
        formatted_date = publication_date.strftime('%B %d, %Y')  # Change the format here
        job_listing = item.get('name', 'N/A')

        if job_listing not in unique_job_listings:
            job_category = item.get('category', 'N/A')
            experience_level = item.get('level', 'N/A')

            # Insert formatted_date as a string instead of a tuple
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


# Update the last processed page
update_last_processed_page(cursor, page_count)
conn.commit()
conn.close()
