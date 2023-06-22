import os

import psycopg2
import requests
from config import config

params_db = config()  # Параметры для подключения к BD
password = os.getenv('Pass_Postgres')  # Пароль как альтернатива для подключения, если параметры прописывать вручную.


class HH_api_db:

    """Класс для работы с API HH.ru и заполнение таблиц в BD"""

    # Список можно дополнить любыми компаниями.
    employers_dict = {'tinkoff': '78638', 'yandex': '5974128', 'Sberbank': '3529'}

    def get_request(self, employer_id) -> dict:
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list

    def employers_to_db(self):
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                for employer in self.employers_dict:
                    cur.execute(f"INSERT INTO companies values ('{int(self.employers_dict[employer])}', '{employer}')")
        conn.commit()
        conn.close()

    def vacancies_to_db(self):
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                for vacancy in self.get_vacancies():
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['employer']}', '{vacancy['url']}')")
        conn.commit()
        conn.close()


class DBManager:

    """Класс для работы с информацией из Базы Данных"""

    @staticmethod
    def get_companies_and_vacancies_count():
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('select company_name, count(vacancy_name) from vacancies group by company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_all_vacancies():
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('select * from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_avg_salary():
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('select avg(salary) from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_higher_salary():
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('select vacancy_name from vacancies where salary > (select avg(salary) from vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        with psycopg2.connect(dbname='HH_api_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"select vacancy_name from vacancies where vacancy_name like '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer
