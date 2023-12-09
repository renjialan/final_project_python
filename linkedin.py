import requests
from bs4 import BeautifulSoup
import sqlite3

# Create an SQLite database connection and cursor
conn = sqlite3.connect('linkedin-jobs.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company_id INTEGER,
        location TEXT,
        apply_link TEXT,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )
''')

def get_or_insert_company(name):
    cursor.execute("SELECT company_id FROM companies WHERE name = ?", (name,))
    company_id = cursor.fetchone()
    if company_id:
        return company_id[0]

    cursor.execute("INSERT INTO companies (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid

def linkedin_scraper(webpage, page_number, rows_to_fetch=25):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        title = job.find('h3', class_='base-search-card__title').text.strip()
        company_name = job.find('h4', class_='base-search-card__subtitle').text.strip()
        location = job.find('span', class_='job-search-card__location').text.strip()
        link = job.find('a', class_='base-card__full-link')['href']

        company_id = get_or_insert_company(company_name)

        # Check if a job with the same title, company_id, and location already exists
        cursor.execute("SELECT * FROM jobs WHERE title = ? AND company_id = ? AND location = ?", (title, company_id, location))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO jobs (title, company_id, location, apply_link)
                VALUES (?, ?, ?, ?)
            ''', (title, company_id, location, link))
            print('Data updated')

    if page_number < 25:
        page_number += rows_to_fetch  # Adjust as needed based on your pagination
        linkedin_scraper(webpage, page_number, rows_to_fetch)
    else:
        conn.commit()
        conn.close()
        print('Database connection closed')

# Start the scraping with an initial page_number of 0
linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Technology&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=', 0)
