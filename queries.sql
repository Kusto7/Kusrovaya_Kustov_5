CREATE TABLE companies (
            company_id int primary key,
            company_name varchar unique not null
            )

CREATE TABLE vacancies (
                vacancy_id serial primary key,
                vacancy_name text not null,
                salary int,
                company_name text not null,
                vacancy_url varchar not null
                )

alter table vacancies add constraint fk_company_name foreign key(company_name) references companies(company_name)

-- 1
select vacancy_name from vacancies where salary > (select avg(salary) from vacancies)

-- 2
select * from vacancies

-- 3
select avg(salary) from vacancies

--4
select vacancy_name from vacancies where salary > (select avg(salary) from vacancies)

--5
select vacancy_name from vacancies where vacancy_name like '%{keyword}%'