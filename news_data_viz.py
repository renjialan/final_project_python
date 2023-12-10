import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def fetch_total_sentiment_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = '''
        SELECT timestamp, SUM(neutral_count), SUM(positive_count), SUM(negative_count)
        FROM news_posts
        GROUP BY timestamp
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def plot_total_sentiment_data(data):
    dates = [row[0] for row in data]
    neutral_counts = [row[1] for row in data]
    positive_counts = [row[2] for row in data]
    negative_counts = [row[3] for row in data]

    bar_width = 0.2
    index = np.arange(len(dates))

    plt.figure(figsize=(10, 6))

    # Creating a side-by-side bar chart
    plt.bar(index - bar_width, neutral_counts, bar_width, color='#00008B', label='Neutral')
    plt.bar(index, positive_counts, bar_width, color='#ADD8E6', label='Positive')
    plt.bar(index + bar_width, negative_counts, bar_width, color='#B0E0E6', label='Negative')

    plt.xlabel('Date')
    plt.ylabel('Total Count')
    plt.title('Sentiment Analysis of Todays News')
    #plt.xticks(index, dates, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    db_path = 'unified_database.db'  # Adjust this path to your unified database file
    total_data = fetch_total_sentiment_data(db_path)

    # Plotting total sentiment data
    plot_total_sentiment_data(total_data)

if __name__ == '__main__':
    main()
