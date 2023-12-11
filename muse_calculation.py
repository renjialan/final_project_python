import sqlite3
from collections import Counter
from datetime import datetime

conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

cursor.execute("SELECT publication_date FROM job_postings")
results = cursor.fetchall()

months = [datetime.strptime(date[0], '%B %d, %Y').strftime('%B') for date in results]
days = [datetime.strptime(date[0], '%B %d, %Y').strftime('%A') for date in results]

most_common_month = Counter(months).most_common(1)[0][0]
most_common_day = Counter(days).most_common(1)[0][0]

print(f"The most common month for a job listing to be posted on Muse is: {most_common_month}")
print(f"The most common day of the week for a job listing to be posted on Muse is: {most_common_day}")
conn.close()