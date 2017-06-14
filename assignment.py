#! /usr/bin/env python3

# Import modules
import psycopg2
import datetime
# from datetime import strftime


def connect():
    """
    Connect to news database

    return (psycopg2 connection object) : required for executing queries
    """
    conn_string = "host='localhost' dbname='news' user='vagrant' password=''"
    try:
        conn = psycopg2.connect(conn_string)
    except Exception as e:
        conn.close()
        raise ConnectionError('Cannot connect to DB, {}'.format(e))
    return conn


def extract(conn, query):
    """
    Execute SQL query

    conn(object) : psycopg connection object
    query (str) : SQL query
    returns (list): SQL query results as python list
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        conn.close()
        raise Exception('Cannot execute SQL query {}'.format(e))
    return cursor.fetchall()


def close(conn):
    """
    Close connection to DB
    """
    conn.close()


def main():

    # Connect to news DB
    conn = connect()

    # Please see README.md for most_popular view detall.
    question1 = "select article.title, popular.cnt " \
                "from most_popular as popular, " \
                "articles as article " \
                "where article.slug = popular.slug " \
                "limit 3;"

    result1 = extract(conn, question1)
    print('Q1: What are the most popular three articles of all time?')
    print('=========================================================')
    for row in result1:
        article, views = row
        print('"{}" -- {} views'.format(article, views))
    print()

    # # Please see README.md for most_popular view detall.
    print('Q2: Who are the most popular article authors of all time?')
    print('=========================================================')
    question2 = "select authors.name, sum(popular.cnt) as cnt " \
                "from authors, " \
                "     most_popular as popular, " \
                "     articles " \
                "where articles.slug = popular.slug and " \
                "     articles.author = authors.id " \
                "group by authors.name " \
                "order by cnt desc;"

    result2 = extract(conn, question2)
    for row in result2:
        author, views = row
        print('"{}" -- {} views'.format(author, views))
    print()

    # Please see README.md for http_codes view detall.
    print('Q3: On which days did more than 1% of requests lead to errors?')
    print('==============================================================')
    question3 = 'select date,ratio ' \
                'from http_codes ' \
                'where status = 404 and ratio>1;'

    result3 = extract(conn, question3)
    for row in result3:
        err_rate = float(row[1])
        day = row[0].strftime('%B %d, %Y')
        print('{} -- {}% errors'.format(day, err_rate))

    # Close connectivity to DB
    close(conn)

if __name__ == "__main__":
    main()
