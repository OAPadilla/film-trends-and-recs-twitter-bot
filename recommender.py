
"""recommender.py: Content-based filtering movie recommender system."""

import os
import time
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ast import literal_eval
from nltk import *
from tmdb_api import *
from secrets import *

import warnings
warnings.simplefilter('ignore')

# Content-based items: genres, keywords, production_companies, title, vote_average, vote_count
DATASET_MOVIES = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_movies.csv')
# Content-based items: title, cast, crew
DATASET_CREDIT = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_credits.csv')


def create_metadata_dataframe():
    """
    Prepares a dataframe from the dataset's metadata
    :return: DataFrame
    """
    movies_metadata = pd.read_csv(DATASET_MOVIES)
    credits_metadata = pd.read_csv(DATASET_CREDIT)

    metadata = pd.merge(movies_metadata, credits_metadata, on='title')

    metadata_df = metadata[['title', 'genres', 'production_companies', 'cast', 'crew', 'vote_average', 'vote_count']]

    # Clean up genre metadata
    metadata_df['genres'] = metadata_df['genres'].fillna('[]').apply(literal_eval) \
        .apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    # Clean up production company metadata
    metadata_df['production_companies'] = metadata_df['production_companies'].fillna('[]').apply(literal_eval) \
        .apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    # Clean up cast metadata
    metadata_df['cast'] = metadata_df['cast'].fillna('[]').apply(literal_eval) \
        .apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    metadata_df['cast'] = metadata_df['cast'].apply(lambda x: x[:11] if len(x) >= 10 else x)
    # Clean up crew metadata for directors
    metadata_df['directors'] = metadata_df['crew'].fillna('[]').apply(literal_eval) \
        .apply(lambda x: [i['name'] for i in x if i['job'] == 'Director'] if isinstance(x, list) else [])
    # Clean up crew metadata for writers
    metadata_df['writers'] = metadata_df['crew'].fillna('[]').apply(literal_eval) \
        .apply(lambda x: [i['name'] for i in x if i['department'] == 'Writing'] if isinstance(x, list) else [])
    metadata_df['writers'] = metadata_df['writers'].apply(lambda x: x[:11] if len(x) >= 10 else x)
    metadata_df = metadata_df.drop(['crew'], axis=1)

    return metadata_df


def create_user_profile(diary):
    """
    Prepares a dataframe from the user's Letterboxd diary metadata
    diary = [{title, year, rating, details: [{genres, production_companies, tmdb_rating}],
              credits: [{cast, directors, writers}]}]
    :return: DataFrane
    """
    m = TheMovieDatabaseAPI(TMDB_API_KEY)
    for entry in diary:
        entry['details'] = m.get_movie_details(entry['title'], entry['year'], None)
        time.sleep(0.55)  # MAX LIMIT: 4 requests per second
        entry['credits'] = m.get_movie_credits(entry['title'], entry['year'], None)
        time.sleep(0.55)

    diary_df = pd.DataFrame(diary)
    return diary_df


def make_soup(df):
    """
    Creates word soup of all the metadata in the dataframe
    :return:
    """



def make_matrix(df1, df2):
    """
    Cosine similarity, a measure of similarity between two vectors, is used to create a
    similarity matrix between movies vectorized with the metadata word soup.
    :return:
    """
    # Frequency counter matrix
    # count = CountVectorizer()
    # matrix1 = count.fit_transform(df1['soup'])
    # matrix2 = count.fit_transform(df2['soup'])
    # Cosine similarity matrix
    # similarity_matrix = cosine_similarity(matrix1, matrix2)

    # return similarity_matrix


def get_recs(diary_df, metadata_df):
    recommended_films = []

    # Create word soup of dataset metadata
    # make_soup(metadata_df)
    # make_soup(diary_df)
    # Make cosine similarity matrix
    # similarity_matrix = make_matrix(metadata_df, soup)

    # do stuff

    return recommended_films



# Watchlist: Title, Year
# TMDb / MovieLens get genre, avg rating, actors, directors, producers of watchlist entries

if __name__ == '__main__':
    print(create_metadata_dataframe())

    # Create dataset df

    # Create diary df
    # Create word soup
    # Create count matrix and cosine sim
    # Get recommendations for films in diary df

