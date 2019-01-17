import tweepy
import sqlite3
from secrets import *
from sqlite_db import *
from letterboxd_scraper import *


auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.me()
print(user.name)
api.update_status('test')


# Once a week, call scraper to scrape top 8 movies of the week
def weekly_top():
    lb = LetterboxdScraper()
    lb.open_browser()
    top8 = lb.get_popular_films()
    lb.close_browser()
    return top8


# Save that onto a database sqlite


# Visualize/format that data
# Tweet it out


