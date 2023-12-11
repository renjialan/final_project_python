import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_top_job_titles(cursor, limit=5):
    cursor.execute('''
        SELECT titles.name, COUNT(jobs.job_id) as job_count
        FROM titles
        LEFT JOIN jobs ON titles.id = jobs.title_id
        GROUP BY titles.name
        ORDER BY job_count DESC
        LIMIT ?
    ''', (limit,))
    top_job_titles = cursor.fetchall()

    return top_job_titles

def calculate_top_locations(cursor, limit=5):
    cursor.execute('''
        SELECT locations.name, COUNT(jobs.job_id) as job_count
        FROM locations
        LEFT JOIN jobs ON locations.id = jobs.location_id
        WHERE locations.name LIKE '%, %'  -- Filter for "city, state" format
        GROUP BY locations.name
        ORDER BY job_count DESC
        LIMIT ?
    ''', (limit,))
    top_locations = cursor.fetchall()

    return top_locations

def plot_top_job_titles(data):
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))

    titles, counts = zip(*data)
    plt.bar(titles, counts, color=sns.color_palette("viridis", len(titles)))
    plt.xlabel('Job Titles', fontsize=12)
    plt.ylabel('Number of Jobs', fontsize=12)
    plt.title('Top 5 Job Titles by Count', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.ylim(bottom=0)
    plt.tight_layout()

    for i, count in enumerate(counts):
        plt.text(i, float(count) + 0.1, str(int(float(count))), ha='center', va='bottom', fontsize=10)

    plt.show()


def plot_top_locations(data):
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))

    locations, counts = zip(*data)
    plt.bar(locations, counts, color=sns.color_palette("viridis", len(locations)))
    plt.xlabel('Locations', fontsize=12)
    plt.ylabel('Number of Jobs', fontsize=12)
    plt.title('Top 5 Job Locations by Count', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.ylim(bottom=0)
    plt.tight_layout()

    for i, count in enumerate(counts):
        plt.text(i, float(count) + 0.1, str(int(float(count))), ha='center', va='bottom', fontsize=10)
    
    plt.show()

def main():
    conn = sqlite3.connect('linkedin-jobs.db')
    cursor = conn.cursor()

    # Calculate top job titles
    top_job_titles = calculate_top_job_titles(cursor)

    # Calculate top locations
    top_locations = calculate_top_locations(cursor)

    # Visualize top job titles
    plot_top_job_titles(top_job_titles)

    # Visualize top locations
    plot_top_locations(top_locations)

    conn.close()


if __name__ == "__main__":
    main()