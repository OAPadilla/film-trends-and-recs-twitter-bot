import tweepy
from secrets import *
from sqlite_db import *
from letterboxd_scraper import *


# Once a week, call scraper to scrape top 8 movies of the week
def scrape_weekly_pop_films():
    print("Scraping Letterboxd's Weekly Popular Films...")
    lb = LetterboxdScraper()
    lb.open_browser()
    pop = lb.get_popular_films()
    lb.close_browser()
    return pop


# Store scraped data
def store_pop_films(pop):
    print("Storing scraped data...")
    conn = connect_db()
    for film in pop:
        task = tuple((film['rank'], film['title'], film['year'], film['watches'], film['likes']))
        db_insert_weekly_top(conn, task)
    conn.close()


# Visualize/format that data
def format_pop_films():
    # get weekly top films
    db_select_weekly_top()
    # get prev ranks for each row

# Tweet it out


if __name__ == '__main__':

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    user = api.me()
    print(user.name)
    #api.update_status('test')

    films_of_the_week = scrape_weekly_pop_films()
    print(films_of_the_week)
    store_pop_films(films_of_the_week)

