#!/usr/bin/env python3

"""twitter_bot.py: Tweets Letterboxd's weekly popular films and recommends based on a user's profile"""

import time
import tweepy
import schedule

from secrets import *
from sqlite_db import *
from letterboxd_scraper import *
from visualize import *
from recommender import *

__author__ = "Oscar Antonio Padilla"
__email__ = "PadillaOscarA@gmail.com"
__status__ = "Development"


auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    """
    Tweepy Twitter Streaming API: Receives twitter messages in real time.
    For replying with recommended films based on tweets providing Letterboxd username
    """
    def on_status(self, status, count=1):
        print("Twitter mention detected...")
        sn = status.user.screen_name
        words = status.text.split(' ')
        if len(words) > 1:
            lb_username = words[1]
            tweet_recommended_films(sn, status.id, lb_username)
        else:
            api.update_status("@" + sn + " Please provide your Letterboxd username!", in_reply_to_status_id=status.id)

    def on_error(self, status_code):
        print(status_code)
        return True

myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
myStream.filter(track=['@LetterBotFilm'], async=True)


def scrape_weekly_pop_films():
    """
    Scrapes Letterboxd site for the top 8 popular films of the week
    :return: List of Strings
    """
    print("Scraping...")
    lb = LetterboxdScraper()
    lb.open_browser()
    films = lb.get_popular_films()
    lb.close_browser()
    return films


def scrape_letterboxd_diary(username):
    """
    Scrapes Letterboxd site for the recent diary entries of the user
    :return: List of Strings
    """
    print("Scraping...")
    lb = LetterboxdScraper()
    lb.open_browser()
    films = lb.get_recent_diary_entries(username)
    lb.close_browser()
    return films


def store_pop_films(films):
    """
    Store scraped data with SQLite
    """
    print("Storing scraped data...")
    conn = connect_db()
    for film in films:
        task = tuple((film['rank'], film['title'], film['year'], film['watches'], film['likes']))
        db_insert_weekly_top(conn, task)
    conn.close()


def visualize_pop_films():
    """
    Visualize the popular films of the week rank data
    """
    print("Visualizing weekly popular films...")
    conn = connect_db()
    # Get weekly top films with previous ranks and prepare the data for visualization
    films = db_select_weekly_top(conn)
    for f in range(len(films)):
        prev_rank = db_select_prev_rank(conn, (films[f][1], films[f][2]))
        films[f] = (films[f][0], films[f][1], films[f][2], films[f][3], films[f][4], films[f][5], prev_rank)
    generate_pop_film_chart(films)


def visualize_recomendations(films):
    """
    Visualize the recommended films
    """
    print("Visualizing recommended films...")
    print(films)
    for f in range(len(films)):
        films[f] = (films[f]['movie_id'], films[f]['title'], films[f]['release_date'], films[f]['count'])
    generate_rec_chart(films)


def tweet_weekly_pop_films():
    """
    Tweets weekly popular films image
    :return: Integer of status id
    """
    # Scrape Letterboxd
    films_of_the_week = scrape_weekly_pop_films()
    # Store scraped data
    store_pop_films(films_of_the_week)
    # Visualize/format data
    visualize_pop_films()
    # Tweet out
    print("Tweeting weekly popular films...")
    status = api.update_with_media(filename=POP_IMAGE_DIR)
    print(status.id)


def tweet_recommended_films(screen_name, status_id, letterboxd_name):
    """
    Tweet replies with recommended films based on tweets provided Letterboxd username
    :return: Integer of status id
    """
    # Read username of comment: Stream Listener does this

    # Scrape letterboxd diary
    diary = scrape_letterboxd_diary(letterboxd_name)
    # Create user profile and TMDb dataset metadata dataframes
    print("Creating user profile and TMDb dataset dataframes...")
    md = create_metadata_dataframe()
    up = create_user_profile(diary)
    # Make user word soups
    md['soup'] = md.apply(make_soup, axis=1)
    up['soup'] = up.apply(make_soup, axis=1)
    # Find similarity matrix
    sim_matrix = make_sim_matrix(md['soup'], up['soup'])
    # Get recs
    rec_films = get_recs(md, up, sim_matrix)
    print(rec_films)
    # Visualize recs, saves image locally
    visualize_recomendations(rec_films)
    # Tweet reply message with image
    print("Tweeting recommendations to... @{} (Letterboxd: {})".format(screen_name, letterboxd_name))
    status = api.update_with_media(filename=RECS_IMAGE_DIR, status="@" + screen_name, in_reply_to_status_id=status_id)
    print(status.id)


if __name__ == '__main__':
    user = api.me()
    print(user.name + " is online.")

    # Tweet Weekly Popular Films on Letterboxd every Saturday, 5 PM
    schedule.every().saturday.at("17:00").do(tweet_weekly_pop_films)

    while True:
        schedule.run_pending()
        time.sleep(1)
