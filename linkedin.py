import matplotlib.pyplot as plt
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup

import csv
import requests
from bs4 import BeautifulSoup
 
file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Apply'])
 
def linkedin_scraper(webpage, page_number):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content,'html.parser')
 
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link')['href']
 
    writer.writerow([
    job_title.encode('utf-8'),
    job_company.encode('utf-8'),
    job_location.encode('utf-8'),
    job_link.encode('utf-8')
    ])
 
    print('Data updated')
 
    if page_number < 25:
        page_number = page_number + 25
        linkedin_scraper(webpage, page_number)
    else:
        file.close()
        print('File closed')


linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Technology&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=', 0)

# Database-related code starts here

import sqlite3
import csv

# Open a connection to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('linkedin_jobs.db')
cursor = conn.cursor()

# Create a table in the database to store the job data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        title TEXT,
        company TEXT,
        location TEXT,
        apply_link TEXT
    )
''')

# Open the CSV file for reading
with open('linkedin-jobs.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row

    # Iterate through each row in the CSV file and insert into the SQLite database
    for row in csvreader:
        title, company, location, apply_link = row
        cursor.execute('''
            INSERT INTO jobs (title, company, location, apply_link)
            VALUES (?, ?, ?, ?)
        ''', (title, company, location, apply_link))
# Commit the changes and close the database connection
conn.commit()
conn.close()

