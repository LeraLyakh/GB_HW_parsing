import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import json

#https://hh.ru/search/vacancy?text=аналитик
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
url = 'https://hh.ru'
params = {'text': 'аналитик',
          'page': 0}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

num = 0
page = 0
vacancies_list = []
while page <= 2:
    params = {'text': 'аналитик',
              'page': page}
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
    page += 1

    for vacancy in vacancies:
        vacancy_data = {}
        num += 1
       # print(num)
        name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        name = name.getText()
        #print(name)
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        #print(salary)

        if salary is None:
            s_min = None
            s_max = None
            currency = None
            #print(f'минимум: {s_min}\nмаксимум: {s_max}\nвалюта: {currency}')
        else:
            salary = salary.getText().replace("–", " - ").split()
           # print(salary)
            if salary[0] == 'от':
                s_min = float(salary[1]+'000')
                s_max = None
                currency = salary[len(salary)-1]
               # print(f'минимум: {s_min}\nмаксимум: {s_max}\nвалюта: {currency}')
            elif salary[0] == 'до':
                s_min = None
                s_max = float(salary[1]+'000')
                currency = salary[len(salary)-1]
               # print(f'минимум: {s_min}\nмаксимум: {s_max}\nвалюта: {currency}')
            else:
                s_min = float(salary[0] + '000')
                s_max = float(salary[3] + '000')
                currency = salary[len(salary) - 1]
                #print(f'минимум: {s_min}\nмаксимум: {s_max}\nвалюта: {currency}')
        link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href'].split('/')
        link = url + '/vacancy/'+link[4].split('?')[0]



        vacancy_data['name'] = name
        vacancy_data['s_min'] = s_min
        vacancy_data['s_max'] = s_max
        vacancy_data['currency'] = currency
        vacancy_data['link'] = link
        vacancies_list.append(vacancy_data)

        # company = vacancy.find('a',{'class':'bloko-link bloko-link_secondary'}).getText()
        # print(company)
    # salary_min = vacancy.find('span',{'class': 'bloko-header-section-3 bloko-header-section-3_lite'})
    # print(salary_min)
        #print()
with open('vacancies.json', 'w+') as f:
    json.dump(vacancies_list, f)

v_df = pd.DataFrame(vacancies_list)
#pd.set_option('display.max_columns', 500)
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 10000)
print(v_df)


