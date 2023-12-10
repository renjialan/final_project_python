import sqlite3

def connect_to_db(db_path):
    return sqlite3.connect(db_path)

def calculate_averages_and_totals(conn):
    cursor = conn.cursor()
    # Query for averages
    query_avg = '''
        SELECT timestamp, AVG(neutral_count), AVG(positive_count), AVG(negative_count)
        FROM news_posts
        GROUP BY timestamp
    '''
    cursor.execute(query_avg)
    averages = cursor.fetchall()

    # Query for totals
    query_total = '''
        SELECT timestamp, SUM(neutral_count) AS total_neutral, SUM(positive_count) AS total_positive, SUM(negative_count) AS total_negative
        FROM news_posts
        GROUP BY timestamp
    '''
    cursor.execute(query_total)
    totals = cursor.fetchall()

    return averages, totals

def main():
    db_path = 'unified_database.db'  # Adjust this path to your unified database file
    conn = connect_to_db(db_path)

    averages, totals = calculate_averages_and_totals(conn)
    conn.close()

    # Write averages to a file
    with open('averages_per_day.txt', 'w') as file:
        for date, avg_neutral, avg_positive, avg_negative in averages:
            file.write(f"{date}: Neutral - {avg_neutral}, Positive - {avg_positive}, Negative - {avg_negative}\n")

    # Write totals to a file
    with open('totals_per_day.txt', 'w') as file:
        for date, total_neutral, total_positive, total_negative in totals:
            file.write(f"{date}: Total Neutral - {total_neutral}, Total Positive - {total_positive}, Total Negative - {total_negative}\n")

    print("Averages and total counts per day have been written to their respective files.")

if __name__ == '__main__':
    main()
