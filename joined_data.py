import sqlite3
import matplotlib.pyplot as plt

def calculate_percentage(conn, table, title_column):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {title_column} LIKE '%intern%'")
    intern_count = cursor.fetchone()[0]

    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    total_count = cursor.fetchone()[0]

    if total_count > 0:
        return (intern_count / total_count) * 100
    else:
        return 0

def main():
    
    conn = sqlite3.connect('unified_database.db')

    
    linkedin_percentage = calculate_percentage(conn, 'linkedin_titles', 'name')
    muse_percentage = calculate_percentage(conn, 'muse_job_postings', 'job_listing')

    conn.close()

   
    labels = 'LinkedIn Internships', 'Muse Internships'
    sizes = [linkedin_percentage, muse_percentage]
    colors = ['#1E90FF', '#87CEFA'] 

    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  
    plt.title('Percentage of Internship Job Titles in LinkedIn and Muse')
    plt.show()


main()
