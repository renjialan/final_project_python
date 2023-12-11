# CODE FOR VISUALIZATIONS FROM MUSE DB ALONE, NOT FULL DB YET
import sqlite3
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('muse_jobs.db')
cursor = conn.cursor()

# Fetch all job postings from the database
cursor.execute("SELECT publication_date FROM job_postings")
results = cursor.fetchall()

# Extract days from publication dates
days = [datetime.strptime(date[0], '%B %d, %Y').strftime('%A') for date in results]

# Count occurrences of each day
day_counts = Counter(days)

# Order days of the week
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create a bar chart with enhanced formatting
plt.figure(figsize=(10, 6))
plt.bar(ordered_days, [day_counts[day] for day in ordered_days], color='skyblue', edgecolor='black', linewidth=1.2)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Number of Job Listings', fontsize=14)
plt.title('Muse Job Listings Posted by Day of the Week', fontsize=16)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Display the bar chart
plt.show()

# Extract months from publication dates
months = [datetime.strptime(date[0], '%B %d, %Y').strftime('%B') for date in results]

# Count occurrences of each month
month_counts = Counter(months)

# Order months
ordered_months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Create a bar graph
plt.figure(figsize=(10, 6))
plt.bar(ordered_months, [month_counts[month] for month in ordered_months], color='salmon', edgecolor='black', linewidth=1.2)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Number of Job Listings', fontsize=14)
plt.title('Muse Job Listings Posted by Month', fontsize=16)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Display the bar graph
plt.show()

# Close the database connection
conn.close()
