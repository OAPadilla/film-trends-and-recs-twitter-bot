import os
import sqlite3
from sqlite3 import Error

DATABASE = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def connect_db():
    # Connecting to the database file
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(e)


def create_weekly_top_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def insert_weekly_top(conn, task):
    sql = '''INSERT INTO popular_films (id, rank, title, year, watches, likes, date)
             VALUES (?,?,?,?,?,?,CURRENT_DATE)'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()


def select_weekly_top(conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM popular_films WHERE date = CURRENT_DATE''')
    conn.commit()


def main():
    # Create a table for popular films
    sql_create_popular_table = '''CREATE TABLE popular_films (
                                    id integer PRIMARY KEY,
                                    rank integer NOT NULL,
                                    title text NOT NULL,
                                    year text NOT NULL,
                                    watches integer NOT NULL,
                                    likes integer NOT NULL,
                                    date date NOT NULL
                                  );'''

    conn.close()
