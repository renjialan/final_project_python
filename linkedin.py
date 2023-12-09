import sqlite3
import requests
from bs4 import BeautifulSoup

def get_or_insert(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    row_id = cursor.fetchone()
    if row_id:
        return row_id[0]

    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
    return cursor.lastrowid

def linkedin_scraper(webpage, page_number, conn, cursor, max_pages, rows_to_fetch=25):
    if page_number > max_pages:
        return

    next_page = webpage + str(page_number * rows_to_fetch)
    print(f"Scraping: {next_page}")

    try:
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        for job in jobs:
            title = job.find('h3', class_='base-search-card__title').text.strip()
            company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job.find('span', class_='job-search-card__location').text.strip()
            link = job.find('a', class_='base-card__full-link')['href']

            title_id = get_or_insert(cursor, 'titles', 'name', title)
            company_id = get_or_insert(cursor, 'companies', 'name', company)
            location_id = get_or_insert(cursor, 'locations', 'name', location)

            cursor.execute('''
                INSERT INTO jobs (title_id, company_id, location_id, apply_link)
                VALUES (?, ?, ?, ?)
            ''', (title_id, company_id, location_id, link))

        conn.commit()  # Commit after processing each page
        linkedin_scraper(webpage, page_number + 1, conn, cursor, max_pages, rows_to_fetch)
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    conn = sqlite3.connect('linkedin-jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS titles (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_id INTEGER,
        company_id INTEGER,
        location_id INTEGER,
        apply_link TEXT,
        FOREIGN KEY (title_id) REFERENCES titles (id),
        FOREIGN KEY (company_id) REFERENCES companies (id),
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
''')

    conn.commit()

    max_pages = 5
    linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Technology&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=', 0, conn, cursor, max_pages)

    conn.close()

if __name__ == '__main__':
    main()
