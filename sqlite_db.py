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


def db_create_weekly_top_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def db_insert_weekly_top(conn, task):
    sql = '''INSERT INTO popular_films (rank, title, year, watches, likes, date)
             VALUES (?,?,?,?,?,CURRENT_DATE)'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()
    return c.lastrowid


def db_select_weekly_top(conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM popular_films WHERE date = CURRENT_DATE''')
    rows = c.fetchall()
    return rows


def db_select_prev_rank(conn, task):
    sql = '''SELECT rank FROM popular_films WHERE title = ? AND year = ? AND date != CURRENT_DATE
             ORDER BY date DESC'''
    c = conn.cursor()
    c.execute(sql, task)
    if c.fetchone() is None:
        return 0
    prev_rank = c.fetchone()[0]
    return prev_rank


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





