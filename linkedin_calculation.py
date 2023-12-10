import sqlite3

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
        GROUP BY locations.name
        ORDER BY job_count DESC
        LIMIT ?
    ''', (limit,))
    top_locations = cursor.fetchall()

    return top_locations

def write_to_txt_titles(data, filename='top_job_titles.txt'):
    with open(filename, 'w') as file:
        for title, count in data:
            file.write(f"{title}: {count}\n")

def write_to_txt_locations(data, filename='top_locations.txt'):
    with open(filename, 'w') as file:
        for location, count in data:
            file.write(f"{location}: {count}\n")

def main():
    conn = sqlite3.connect('linkedin-jobs.db')
    cursor = conn.cursor()

     # Calculate top job titles
    top_job_titles = calculate_top_job_titles(cursor)
    write_to_txt_titles(top_job_titles, filename='top_job_titles.txt')

    # Calculate top locations
    top_locations = calculate_top_locations(cursor)
    write_to_txt_locations(top_locations, filename='top_locations.txt')

    conn.close()


    main()
