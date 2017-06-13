# Udacity Logs Analysis Project
In this project we are asked to analyze `news` database and using `psycopg2` we are tring to answer the follwoing questions:

1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Project Details
This project makes use of two views, help to summarize few operations. These views are:

- `most_popular` : It cleans and transforms `log` table path. Q1 and Q2 use this view.
- `http_codes` : It aggregates `log` table http codes vs dates. Q3 uses this view 

### Views

##### most_popular

```sql
create view most_popular as 
select
  case when slug like 'candidate%' then 'candidate-is-jerk'
       when slug like 'bears%' then 'bears-love-berries' 
       when slug like 'bad-things%' then 'bad-things-gone' 
       when slug like 'goats%' then 'goats-eat-googles' 
       when slug like 'trouble%' then 'trouble-for-troubled' 
       when slug like 'balloon%' then 'balloon-goons-doomed' 
       when slug like 'so-many%' then 'so-many-bears' 
       when slug like 'media%' then 'media-obsessed-with-bears' 
  end as slug, count(*) as cnt
  from
  (select replace(path,'/article/','') as slug 
    from log 
  where path like '%article%') as a
  group by 1
  order by cnt desc;
```

##### http_codes
```sql
create view http_codes as
select  status, date, cnt, round(100*cnt/sum(cnt) over (partition by date),2) as ratio 
from (
  select status::char(3)::int, date(time), count(*) as cnt 
  from log 
  group by status, date) as a;
```

### How to run code?
This code is written in **python3.6**. Though it is highly likely compatible with earlier versions of **python3.x**. I haven't tested them in all environments. There is no guarantee this code would work in **python2**.

After cloning from git, ideally you should create a virtual environment using `venv` by:
```sh
$ python -m venv venv 
$ source venv/bin/activate 
```
and install `psycopg2` module
```sh
(venv)$ pip3 install psycopg2
```

make `assignment.py` file executable 
```sh
(venv)$ chmod +x assignment.py
```

and then you can run `assignment.py` by:
```sh
(venv)$ python3 assignment.py
```


