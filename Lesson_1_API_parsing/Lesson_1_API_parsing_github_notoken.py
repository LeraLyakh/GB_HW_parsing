import requests
from pprint import pprint
import json

token = ' '
username = 'LeraLyakh'
url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url, auth =(username, token))
j_data = response.json()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(j_data, f, ensure_ascii=False, indent=4)

#pprint(j_data)
for i in range(0,len(j_data)):
  print(f'Имя репозитория: {j_data[i]["name"]}')
  print(f'URL: {j_data[i]["html_url"]}\n')
