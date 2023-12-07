import requests
import sqlite3
from datetime import datetime

from pprint import pprint
full_data = []
for i in range(10):
      res = requests.get('https://www.themuse.com/api/public/jobs?page=' + i)
      data = res.json()

      lists = data['results']
      if data['publication_date'] > '2023-05-19T23:38:55Z':
          for item in lists:
              name = item['name']
              full_data.append(name)

# pprint(data)

# for i in range(25):
#   cur.execute('INSERT ...', full_data[i])

# cur.execute('SELECT ....')
# selected_data = cur.fetcall()


# get data from api, store it in database, retrieve data with the select clauses and join, and visualize the data