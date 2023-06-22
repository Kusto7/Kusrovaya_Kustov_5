import psycopg2


def create_database(database_name, params):

    """Создание базы данных и таблиц для сохранения данных о вакансиях и работодателях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f'DROP DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        pass

    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_table(params):

    """Создание таблиц для дальнейшей работы"""

    conn = psycopg2.connect(dbname='HH_api_vacancy', **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
            company_id int primary key,
            company_name varchar unique not null
            )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial primary key,
                vacancy_name text not null,
                salary int,
                company_name text not null,
                vacancy_url varchar not null
                )
                """)

    with conn.cursor() as cur:
        cur.execute("""alter table vacancies add constraint fk_company_name 
        foreign key(company_name) references companies(company_name)""")

    conn.commit()
    conn.close()
