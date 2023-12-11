import matplotlib.pyplot as plt
import seaborn as sns

def read_from_txt(filename='top_job_titles.txt'):
    with open(filename, 'r') as file:
        data = [line.strip().split(': ') for line in file]

    return data

def plot_top_job_titles(data):
    titles, counts = zip(*data)
    plt.bar(titles, counts)
    plt.xlabel('Job Titles')
    plt.ylabel('Number of Jobs')
    plt.title('Top 5 Job Titles by Count')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(bottom=0)
    plt.tight_layout()
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

    plt.gca().invert_yaxis()
    
    for i, count in enumerate(counts):
        plt.text(i, float(count) + 0.1, str(int(float(count))), ha='center', va='bottom', fontsize=10)

    plt.show()

def main():
    job_titles_data = read_from_txt(filename='top_job_titles.txt')
    plot_top_job_titles(job_titles_data)

    # Visualize top locations
    locations_data = read_from_txt(filename='top_locations.txt')
    plot_top_locations(locations_data)


    main()
