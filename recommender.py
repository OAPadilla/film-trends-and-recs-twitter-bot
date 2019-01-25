
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

    metadata_df = metadata[['movie_id', 'title', 'genres', 'production_companies',
                            'cast', 'crew', 'vote_average', 'vote_count']]

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
    diary = [{title, year, rating, details: [{genres, production_companies, vote_average}],
              credits: [{cast, directors, writers}]}]
    :return: DataFrane
    """
    m = TheMovieDatabaseAPI(TMDB_API_KEY)
    for entry in diary:
        d = m.get_movie_details(entry['title'], entry['year'], None)
        entry['genres'] = d[0]['genres']
        entry['production_companies'] = d[0]['production_companies']
        entry['vote_average'] = d[0]['vote_average']
        time.sleep(0.55)  # MAX LIMIT: 4 requests per second

        c = m.get_movie_credits(entry['title'], entry['year'], None)
        entry['cast'] = c[0]['cast']
        entry['directors'] = c[0]['directors']
        entry['writers'] = c[0]['writers']
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
    diary = [{'title': 'Vice', 'year': '2018', 'rating': '6'}, {'title': 'Magnolia', 'year': '1999', 'rating': '10'},
             {'title': 'Roma', 'year': '2018', 'rating': '9'},
             {'title': 'Children of Men', 'year': '2006', 'rating': '9'},
             {'title': 'Black Mirror: Bandersnatch', 'year': '2018', 'rating': '5'},
             {'title': 'Take Shelter', 'year': '2011', 'rating': '7'},
             {'title': 'The Ballad of Buster Scruggs', 'year': '2018', 'rating': '7'},
             {'title': 'Incredibles 2', 'year': '2018', 'rating': '6'},
             {'title': 'Force Majeure', 'year': '2014', 'rating': '7'},
             {'title': 'Sorry to Bother You', 'year': '2018', 'rating': '8'},
             {'title': 'BlacKkKlansman', 'year': '2018', 'rating': '6'},
             {'title': 'Hereditary', 'year': '2018', 'rating': '8'},
             {'title': 'It Follows', 'year': '2014', 'rating': '7'},
             {'title': 'Black Swan', 'year': '2010', 'rating': '9'}, {'title': 'Mandy', 'year': '2018', 'rating': '7'},
             {'title': 'It', 'year': '2017', 'rating': '6'},
             {'title': 'What We Do in the Shadows', 'year': '2014', 'rating': '8'},
             {'title': 'Mamma Mia! Here We Go Again', 'year': '2018', 'rating': '4'},
             {'title': 'Isle of Dogs', 'year': '2018', 'rating': '7'},
             {'title': 'Thoroughbreds', 'year': '2017', 'rating': '7'},
             {'title': 'The Disaster Artist', 'year': '2017', 'rating': '6'},
             {'title': 'Solaris', 'year': '1972', 'rating': '0'},
             {'title': 'Fallen Angels', 'year': '1995', 'rating': '8'},
             {'title': 'The Master', 'year': '2012', 'rating': '7'},
             {'title': 'Suspiria', 'year': '1977', 'rating': '9'},
             {'title': 'Welcome to Leith', 'year': '2015', 'rating': '6'},
             {'title': 'Death Note', 'year': '2017', 'rating': '3'},
             {'title': 'There Will Be Blood', 'year': '2007', 'rating': '10'},
             {'title': 'Cube 2: Hypercube', 'year': '2002', 'rating': '2'},
             {'title': 'Cube', 'year': '1997', 'rating': '4'},
             {'title': "One Flew Over the Cuckoo's Nest", 'year': '1975', 'rating': '9'},
             {'title': 'Mulholland Drive', 'year': '2001', 'rating': '0'},
             {'title': 'Star Wars: The Last Jedi', 'year': '2017', 'rating': '5'},
             {'title': 'Coherence', 'year': '2013', 'rating': '6'},
             {'title': 'Avengers: Infinity War', 'year': '2018', 'rating': '7'},
             {'title': 'The One I Love', 'year': '2014', 'rating': '7'},
             {'title': 'Annihilation', 'year': '2018', 'rating': '7'},
             {'title': "The Devil's Backbone", 'year': '2001', 'rating': '9'},
             {'title': 'Coco', 'year': '2017', 'rating': '7'}, {'title': 'Office Space', 'year': '1999', 'rating': '8'},
             {'title': 'The Cloverfield Paradox', 'year': '2018', 'rating': '3'},
             {'title': 'Good Time', 'year': '2017', 'rating': '8'},
             {'title': 'The Shape of Water', 'year': '2017', 'rating': '8'},
             {'title': 'Three Billboards Outside Ebbing, Missouri', 'year': '2017', 'rating': '7'},
             {'title': 'The Killing of a Sacred Deer', 'year': '2017', 'rating': '7'},
             {'title': 'The Death of Stalin', 'year': '2017', 'rating': '7'},
             {'title': 'The Florida Project', 'year': '2017', 'rating': '9'},
             {'title': 'Once', 'year': '2007', 'rating': '7'},
             {'title': 'Blade Runner 2049', 'year': '2017', 'rating': '10'},
             {'title': 'Blade Runner', 'year': '1982', 'rating': '9'}]

    print(create_user_profile(diary))

    # Create dataset df

    # Create diary df
    # Create word soup
    # Create count matrix and cosine sim
    # Get recommendations for films in diary df

