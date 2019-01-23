
"""recommender.py: Content-based movie recommender system."""

import os
import requests
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from secrets import *

# Content-based items: genres

# genres, keywords, production_companies, title, vote_average, vote_count
# DATASET_MOVIES = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_movies.csv')
# title, cast, crew
# DATASET_CREDIT = os.path.join(os.path.dirname(__file__), 'datasets', 'tmdb', 'tmdb_5000_credits.csv')



# Watchlist: Title, Year
# TMDb / MovieLens get genre, avg rating, actors, directors, producers of watchlist entries

# movies_metadata = pd.read_csv(DATASET_MOVIES)
# credit_metadata = pd.read_csv(DATASET_CREDIT)
# films_df = pd.merge(movies_metadata, credit_metadata, on='title')





# -User profile-
# Diary: Title, Year, Rating
# TMDb get genre, avg rating, actors, directors, producers of diary entries
#
# 1. Search for the movie by title, get movie_id
# 2. Use movie_id to get film details
# 3. Add to json result
class TheMovieDatabaseAPI:

    details_url = 'https://api.themoviedb.org/3/movie/{}?api_key='
    search_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'
    credits_url = 'https://api.themoviedb.org/3/movie/{}/credits?api_key='

    def __init__(self, key):
        self.api_key = key
        self.result = []

    # FIXME CHECK YEAR TOO
    def get_movie_id(self, title, year):
        """
        Gets TMDb movie_id of film from search API call
        :return: integer
        """
        parsed_title = '+'.join(title.split(' '))
        url = self.search_url.format(self.api_key, parsed_title)

        res = requests.get(url).json()
        m_id = res['results'][0]['id']
        return m_id

    def get_movie_credits(self, title, year, movie_id):
        """
        Gets cast (first 15), directors, and writers of film from credits API call
        :return: List of Dictionary
        """
        credits = []

        if movie_id is None:
            movie_id = self.get_movie_id(title, year)

        url = self.credits_url.format(movie_id) + self.api_key
        res = requests.get(url).json()

        cast = [res['cast'][x]['name'] for x in range(15)]
        directors = [res['crew'][x]['name'] for x in range(len(res['crew']))
                     if res['crew'][x]['department'] == 'Directing']
        writers = [res['crew'][x]['name'] for x in range(len(res['crew']))
                     if res['crew'][x]['department'] == 'Writing']

        credits.append({'cast': cast, 'directors': directors, 'writers': writers})
        return credits


    def get_movie_details(self, title, year, movie_id):
        """
        Gets genre and avg rating of film from details API call
        :return: List of Dictionary
        """
        details = {}

        if movie_id is None:
            movie_id = self.get_movie_id(title, year)


        url = self.details_url.format(movie_id) + self.api_key
        res = requests.get(url).json()

        #details.append({'tmdb_movie_id': movie_id, 'genres': res['genres'], 'tmdb_rating': res['vote_average'], 'actors': , 'directors': , 'producers'})
        return details

    def get_film_image(self, film):
        pass




if __name__ == '__main__':

    diary = [{'title': 'Vice', 'year': '2018', 'rating': '6'}, {'title': 'Magnolia', 'year': '1999', 'rating': '10'}, {'title': 'Roma', 'year': '2018', 'rating': '9'}, {'title': 'Children of Men', 'year': '2006', 'rating': '9'}, {'title': 'Black Mirror: Bandersnatch', 'year': '2018', 'rating': '5'}, {'title': 'Take Shelter', 'year': '2011', 'rating': '7'}, {'title': 'The Ballad of Buster Scruggs', 'year': '2018', 'rating': '7'}, {'title': 'Incredibles 2', 'year': '2018', 'rating': '6'}, {'title': 'Force Majeure', 'year': '2014', 'rating': '7'}, {'title': 'Sorry to Bother You', 'year': '2018', 'rating': '8'}, {'title': 'BlacKkKlansman', 'year': '2018', 'rating': '6'}, {'title': 'Hereditary', 'year': '2018', 'rating': '8'}, {'title': 'It Follows', 'year': '2014', 'rating': '7'}, {'title': 'Black Swan', 'year': '2010', 'rating': '9'}, {'title': 'Mandy', 'year': '2018', 'rating': '7'}, {'title': 'It', 'year': '2017', 'rating': '6'}, {'title': 'What We Do in the Shadows', 'year': '2014', 'rating': '8'}, {'title': 'Mamma Mia! Here We Go Again', 'year': '2018', 'rating': '4'}, {'title': 'Isle of Dogs', 'year': '2018', 'rating': '7'}, {'title': 'Thoroughbreds', 'year': '2017', 'rating': '7'}, {'title': 'The Disaster Artist', 'year': '2017', 'rating': '6'}, {'title': 'Solaris', 'year': '1972', 'rating': '0'}, {'title': 'Fallen Angels', 'year': '1995', 'rating': '8'}, {'title': 'The Master', 'year': '2012', 'rating': '7'}, {'title': 'Suspiria', 'year': '1977', 'rating': '9'}, {'title': 'Welcome to Leith', 'year': '2015', 'rating': '6'}, {'title': 'Death Note', 'year': '2017', 'rating': '3'}, {'title': 'There Will Be Blood', 'year': '2007', 'rating': '10'}, {'title': 'Cube 2: Hypercube', 'year': '2002', 'rating': '2'}, {'title': 'Cube', 'year': '1997', 'rating': '4'}, {'title': "One Flew Over the Cuckoo's Nest", 'year': '1975', 'rating': '9'}, {'title': 'Mulholland Drive', 'year': '2001', 'rating': '0'}, {'title': 'Star Wars: The Last Jedi', 'year': '2017', 'rating': '5'}, {'title': 'Coherence', 'year': '2013', 'rating': '6'}, {'title': 'Avengers: Infinity War', 'year': '2018', 'rating': '7'}, {'title': 'The One I Love', 'year': '2014', 'rating': '7'}, {'title': 'Annihilation', 'year': '2018', 'rating': '7'}, {'title': "The Devil's Backbone", 'year': '2001', 'rating': '9'}, {'title': 'Coco', 'year': '2017', 'rating': '7'}, {'title': 'Office Space', 'year': '1999', 'rating': '8'}, {'title': 'The Cloverfield Paradox', 'year': '2018', 'rating': '3'}, {'title': 'Good Time', 'year': '2017', 'rating': '8'}, {'title': 'The Shape of Water', 'year': '2017', 'rating': '8'}, {'title': 'Three Billboards Outside Ebbing, Missouri', 'year': '2017', 'rating': '7'}, {'title': 'The Killing of a Sacred Deer', 'year': '2017', 'rating': '7'}, {'title': 'The Death of Stalin', 'year': '2017', 'rating': '7'}, {'title': 'The Florida Project', 'year': '2017', 'rating': '9'}, {'title': 'Once', 'year': '2007', 'rating': '7'}, {'title': 'Blade Runner 2049', 'year': '2017', 'rating': '10'}, {'title': 'Blade Runner', 'year': '1982', 'rating': '9'}]

    m = TheMovieDatabaseAPI(TMDB_API_KEY)
    #m.get_movie_details(diary[3]['title'])
    print(m.get_movie_credits(diary[3]['title'], diary[3]['year'], 9693))


    # result diary with all new info