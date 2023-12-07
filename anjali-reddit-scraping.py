import requests
from datetime import datetime, timedelta
from pprint import pprint

full_data = []
page_count = 0

while len(full_data) < 100 and page_count < 25:
    page_count += 1
    res = requests.get(f'https://www.themuse.com/api/public/jobs?page={page_count}')
    data = res.json()

    lists = data['results']
    for item in lists:
        # Convert the publication date to a datetime object
        publication_date = datetime.strptime(item['publication_date'], '%Y-%m-%dT%H:%M:%SZ')

        # Check if the publication date is after '2023-05-19T23:38:55Z'
        if publication_date > datetime.strptime('2023-05-19T23:38:55Z', '%Y-%m-%dT%H:%M:%SZ'):
            name = item['name']
            full_data.append(name)

# Print the collected data
pprint(full_data)
pprint(len(full_data))

# for i in range(25):
#   cur.execute('INSERT ...', full_data[i])

# cur.execute('SELECT ....')
# selected_data = cur.fetcall()


# get data from api, store it in database, retrieve data with the select clauses and join, and visualize the data