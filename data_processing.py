# Run this file to calculate 
import sqlite3
from datetime import datetime

def connect_to_db(db_path):
    return sqlite3.connect(db_path)

def calculate_averages(conn):
    cursor = conn.cursor()
    query = '''
        SELECT timestamp, AVG(neutral_count), AVG(positive_count), AVG(negative_count)
        FROM news_posts
        GROUP BY timestamp
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def main():
    db_path = 'unified_database.db'  # Adjust this path to your unified database file
    conn = connect_to_db(db_path)

    averages = calculate_averages(conn)
    conn.close()

    # Write results to a file
    with open('averages_per_day.txt', 'w') as file:
        for date, avg_neutral, avg_positive, avg_negative in averages:
            file.write(f"{date}: Neutral - {avg_neutral}, Positive - {avg_positive}, Negative - {avg_negative}\n")

    print("Averages per day have been written to averages_per_day.txt")

if __name__ == '__main__':
    main()
