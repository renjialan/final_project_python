import sqlite3
import requests
from datetime import datetime, timedelta
from pprint import pprint

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

# Commit changes to the database
conn.commit()

full_data = []
unique_job_listings = set()
page_count = 0

while len(full_data) < 100 and page_count < 25:
    page_count += 1
    res = requests.get(f'https://www.themuse.com/api/public/jobs?page={page_count}')
    data = res.json()

    lists = data['results']
    for item in lists:
        # Convert the publication date to a datetime object
        publication_date = datetime.strptime(item['publication_date'], '%Y-%m-%dT%H:%M:%SZ')

        # Check if the publication date is after '2023-05-19T23:38:55Z'
        if publication_date > datetime.strptime('2023-05-19T23:38:55Z', '%Y-%m-%dT%H:%M:%SZ'):
            job_listing = item.get('name', 'N/A')

            # Check if the job listing is not already in the set
            if job_listing not in unique_job_listings:
                job_category = item.get('category', 'N/A')
                experience_level = item.get('level', 'N/A')

                # Store data in SQLite database
                cursor.execute('''
                    INSERT INTO job_postings (job_category, job_listing, publication_date, experience_level)
                    VALUES (?, ?, ?, ?)
                ''', (job_category, job_listing, publication_date.strftime('%Y-%m-%dT%H:%M:%SZ'), experience_level))
                conn.commit()

                # Append data to the full_data list (optional)
                full_data.append({
                    'job_category': job_category,
                    'job_listing': job_listing,
                    'publication_date': publication_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'experience_level': experience_level
                })

                # Add job listing to the set to track uniqueness
                unique_job_listings.add(job_listing)

# Print the collected data
pprint(full_data)
