import requests
from bs4 import BeautifulSoup
import sqlite3

# Create an SQLite database connection and cursor
conn = sqlite3.connect('linkedin-jobs.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        title TEXT,
        company TEXT,
        location TEXT,
        apply_link TEXT
    )
''')

def linkedin_scraper(webpage, page_number, rows_to_fetch=25):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        title = job.find('h3', class_='base-search-card__title').text.strip()
        company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        location = job.find('span', class_='job-search-card__location').text.strip()
        link = job.find('a', class_='base-card__full-link')['href']

        # Insert data into the SQLite database
        cursor.execute('''
            INSERT INTO jobs (title, company, location, apply_link)
            VALUES (?, ?, ?, ?)
        ''', (title, company, location, link))

        print('Data updated')

    if page_number < 25:
        page_number += rows_to_fetch  # Adjust as needed based on your pagination
        linkedin_scraper(webpage, page_number, rows_to_fetch)
    else:
        # Commit changes and close the database connection
        conn.commit()
        conn.close()
        print('Database connection closed')

# Start the scraping with an initial page_number of 0
linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Technology&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=', 0)