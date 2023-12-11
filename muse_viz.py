import sqlite3
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

cursor.execute("SELECT publication_date FROM job_postings")
results = cursor.fetchall()

days = [datetime.strptime(date[0], '%B %d, %Y').strftime('%A') for date in results]

day_counts = Counter(days)

ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(figsize=(10, 6))
plt.bar(ordered_days, [day_counts[day] for day in ordered_days], color='skyblue', edgecolor='black', linewidth=1.2)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Number of Job Listings', fontsize=14)
plt.title('Muse Job Listings Posted by Day of the Week', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()

months = [datetime.strptime(date[0], '%B %d, %Y').strftime('%B') for date in results]

month_counts = Counter(months)

ordered_months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

plt.figure(figsize=(10, 6))
plt.bar(ordered_months, [month_counts[month] for month in ordered_months], color='salmon', edgecolor='black', linewidth=1.2)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Number of Job Listings', fontsize=14)
plt.title('Muse Job Listings Posted by Month', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
conn.close()
