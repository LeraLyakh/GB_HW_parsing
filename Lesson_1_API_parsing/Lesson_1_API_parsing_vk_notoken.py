import requests
from pprint import pprint
import json

access_token = ' '
u_id = '312396764'
version = '5.131'

url = f'https://api.vk.com/method/groups.get'
params = {'access_token':access_token,
          'extended': 1,
          'user_id':u_id,
          'v': version}

response = requests.get(url, params=params)
j_data = response.json()

with open('data_vk.json', 'w', encoding='utf-8') as f:
    json.dump(j_data, f, ensure_ascii=False, indent=4)
j_data = j_data['response']['items']
#pprint(j_data)
for i in range(0,len(j_data)):
  print(f'№{i+1}')
  print(f'Название: {j_data[i]["name"]}')
  print(f'URL: https://vk.com/{j_data[i]["screen_name"]}\n')
