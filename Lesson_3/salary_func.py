from pymongo import MongoClient
from pprint import pprint


def get_salary():
    desired_salary = int(input("Введите желаемую зарплату: "))
    for vacancy in db.vacancies_hh.find(
            {'$or': [{'s_max': {'$gt': desired_salary}}, {'s_min': {'$gt': desired_salary}}]}):
        pprint(vacancy)

client = MongoClient('localhost', 27017)
db = client['hh_ru']

sal_vac = get_salary()

