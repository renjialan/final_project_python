# CODE FOR CALCULATIONS FROM MUSE DB ALONE, NOT FULL DB YET

import sqlite3
from collections import Counter
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

# Fetch all job postings from the database
cursor.execute("SELECT publication_date FROM job_postings")
results = cursor.fetchall()

# Extract months and days from publication dates
months = [datetime.strptime(date[0], '%B %d, %Y').strftime('%B') for date in results]
days = [datetime.strptime(date[0], '%B %d, %Y').strftime('%A') for date in results]

# Calculate the most common month and day
most_common_month = Counter(months).most_common(1)[0][0]
most_common_day = Counter(days).most_common(1)[0][0]

# Print the results
print(f"The most common month for job postings is: {most_common_month}")
print(f"The most common day of the week for job postings is: {most_common_day}")

# Close the database connection
conn.close()