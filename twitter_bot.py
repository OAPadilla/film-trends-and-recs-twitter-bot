import tweepy
from secrets import *
from sqlite_db import *
from letterboxd_scraper import *


# Once a week, call scraper to scrape top 8 movies of the week
def scrape_weekly_pop_films():
    print("Scraping...")
    lb = LetterboxdScraper()
    lb.open_browser()
    films = lb.get_popular_films()
    lb.close_browser()
    return films


# Store scraped data
def store_pop_films(films):
    print("Storing scraped data...")
    conn = connect_db()
    for film in films:
        task = tuple((film['rank'], film['title'], film['year'], film['watches'], film['likes']))
        db_insert_weekly_top(conn, task)
    conn.close()


# Visualize/format that data
def format_pop_films():
    # get weekly top films and prev ranks
    conn = connect_db()
    films = db_select_weekly_top(conn)
    for f in range(len(films)):
        # append prev_rank to films tuples
        prev_rank = db_select_prev_rank(conn, (films[f][1], films[f][2]))
        films[f] = (films[f][0], films[f][1], films[f][2], films[f][3], films[f][4], films[f][5], prev_rank)
    print(films)


# Tweets Weekly Popular Films
def tweet_weekly_pop_films():
    # Scrape Letterboxd
    films_of_the_week = scrape_weekly_pop_films()
    # Store scraped data
    store_pop_films(films_of_the_week)
    # Visualize/format data
    format_pop_films()
    # Tweet out
    print("Tweeting...")


if __name__ == '__main__':

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    user = api.me()
    print(user.name)
    #api.update_status('test')

    #tweet_weekly_pop_films()

    format_pop_films()


