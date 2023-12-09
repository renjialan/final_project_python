# This code is for vizualization but i havent tried it yet
import matplotlib.pyplot as plt
def plot_job_category_distribution(muse_data_file):
    categories = {}
    with open(muse_data_file, 'r') as file:
        next(file)  # Skip header line
        for line in file:
            _, category, _, _, _ = line.strip().split('\t')
            categories[category] = categories.get(category, 0) + 1

    labels = list(categories.keys())
    sizes = list(categories.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
    plt.title('Job Category Distribution in Muse Data')
    plt.savefig('job_category_distribution.png')
    plt.show()

def plot_word_count_histogram(news_data_file):
    word_counts = []
    with open(news_data_file, 'r') as file:
        next(file)  # Skip header line
        for line in file:
            content = line.strip().split('\t')[2]
            word_counts.append(len(content.split()))

    plt.figure(figsize=(10, 6))
    plt.hist(word_counts, bins=20, color='purple')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.title('Distribution of Word Counts in News Posts')
    plt.savefig('word_count_histogram.png')
    plt.show()

def plot_stacked_sentiment_counts(news_data_file):
    dates = []
    neutral_counts = []
    positive_counts = []
    negative_counts = []
    with open(news_data_file, 'r') as file:
        next(file)  # Skip header line
        for line in file:
            date, _, _, neutral, positive, negative = line.strip().split('\t')
            if date not in dates:
                dates.append(date)
                neutral_counts.append(int(neutral))
                positive_counts.append(int(positive))
                negative_counts.append(int(negative))
            else:
                idx = dates.index(date)
                neutral_counts[idx] += int(neutral)
                positive_counts[idx] += int(positive)
                negative_counts[idx] += int(negative)

    plt.figure(figsize=(12, 6))
    plt.bar(dates, neutral_counts, color='blue', label='Neutral')
    plt.bar(dates, positive_counts, bottom=neutral_counts, color='green', label='Positive')
    plt.bar(dates, negative_counts, bottom=[i+j for i,j in zip(neutral_counts, positive_counts)], color='red', label='Negative')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Count')
    plt.title('Stacked Sentiment Counts per Day')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('stacked_sentiment_counts.png')
    plt.show()

# Replace the file names with the correct paths to your data files
plot_job_category_distribution('muse_jobs_data.txt')  # Muse job data file
plot_word_count_histogram('news_data.txt')  # News data file
plot_stacked_sentiment_counts('news_data.txt')  # News data file
