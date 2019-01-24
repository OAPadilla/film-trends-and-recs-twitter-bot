
"""recommender.py: Content-based filtering movie recommender system."""

import os
import time
import requests
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from secrets import *
from tmdb_api import *


# Content-based items: genres, keywords, production_companies, title, vote_average, vote_count
DATASET_MOVIES = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_movies.csv')
# Content-based items: title, cast, crew
DATASET_CREDIT = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_credits.csv')


def create_metadata_dataframe():
    """
    Prepares a dataframe from the dataset's metadata
    :return:
    """
    movies_metadata = pd.read_csv(DATASET_MOVIES)
    credit_metadata = pd.read_csv(DATASET_CREDIT)
    metadata = pd.merge(movies_metadata, credit_metadata, on='title')

    films_df = metadata[['title', 'genres', 'production_companies', 'cast', 'crew', 'vote_average', 'vote_count']]

    return films_df


# User profile, Diary: Title, Year, Rating
def create_user_profile(diary):
    """
    Prepares a dataframe from the user's Letterboxd diary metadata
    :return: Array of Dictionaries : [{'title', 'year', 'rating',
                                       'details': [{'genres', 'production_companies', 'tmdb_rating'}],
                                       'credits': [{'cast', 'directors', 'writers'}]
    """
    m = TheMovieDatabaseAPI(TMDB_API_KEY)
    for entry in diary:
        entry['details'] = m.get_movie_details(entry['title'], entry['year'], None)
        time.sleep(0.55)  # MAX LIMIT: 4 requests per second
        entry['credits'] = m.get_movie_credits(entry['title'], entry['year'], None)
        time.sleep(0.55)

    return pd.DataFrame(diary)


def create_soup:
    """
    Creates word soup of all the metadata
    :return:
    """
    pass


def get_recommendations():
    pass

# Watchlist: Title, Year
# TMDb / MovieLens get genre, avg rating, actors, directors, producers of watchlist entries

if __name__ == '__main__':
    print(create_metadata_dataframe())


# Prepare dataframes
# Find correlation coefficient
