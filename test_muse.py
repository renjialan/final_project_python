# CODE FOR CALCULATIONS FROM MUSE DB ALONE, NOT FULL DB YET
# import sqlite3
# from collections import Counter
# from datetime import datetime

# # Connect to SQLite database
# conn = sqlite3.connect('muse_jobs.db')
# cursor = conn.cursor()

# # Fetch all job postings from the database
# cursor.execute("SELECT publication_date FROM job_postings")
# results = cursor.fetchall()

# # Extract months and days from publication dates
# months = [datetime.strptime(date[0], '%B %d, %Y').strftime('%B') for date in results]
# days = [datetime.strptime(date[0], '%B %d, %Y').strftime('%A') for date in results]

# # Calculate the most common month and day
# most_common_month = Counter(months).most_common(1)[0][0]
# most_common_day = Counter(days).most_common(1)[0][0]

# # Print the results
# print(f"The most common month for job postings is: {most_common_month}")
# print(f"The most common day of the week for job postings is: {most_common_day}")

# # Close the database connection
# conn.close()

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
plt.title('Job Listings Posted by Day of the Week', fontsize=16)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()

# Display the bar chart
plt.show()

# Close the database connection
conn.close()
