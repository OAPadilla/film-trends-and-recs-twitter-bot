#!/usr/bin/env python3

"""tmdb_api.py: Makes HTTP GET requests for movie information to The Movie Database API"""

import requests
import time
from secrets import *

__author__ = "Oscar Antonio Padilla"
__email__ = "PadillaOscarA@gmail.com"
__status__ = "Development"


class TheMovieDatabaseAPI:

    URL_SEARCH = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'
    URL_CREDITS = 'https://api.themoviedb.org/3/movie/{}/credits?api_key='
    URL_DETAILS = 'https://api.themoviedb.org/3/movie/{}?api_key='

    def __init__(self, key):
        self.api_key = key

    def get_movie_id(self, title, year):
        """
        Gets TMDb movie_id of film from search TMDb API call
        :return: Integer
        """
        parsed_title = '+'.join(title.split(' '))
        url = self.URL_SEARCH.format(self.api_key, parsed_title)

        r = requests.get(url)
        res = r.json()

        if r.status_code == 200:
            # Default movie_id is first result
            m_id = res['results'][0]['id']

            for movie in res['results']:
                release_date = movie['release_date']
                if release_date[:4] == year:
                    m_id = movie['id']
                    break
            return m_id
        return None

    def get_movie_credits(self, title, year, movie_id):
        """
        Gets cast (first 15), directors, and writers of film from credits TMDb API call
        :return: List of Dictionaries
        """
        credits = []

        if movie_id is None:
            movie_id = self.get_movie_id(title, year)

        url = self.URL_CREDITS.format(movie_id) + self.api_key
        res = requests.get(url).json()

        cast = [res['cast'][x]['name'] for x in range(min(len(res['cast']), 10))]
        directors = [d['name'] for d in res['crew'] if d['department'] == 'Directing']
        writers = [w['name'] for w in res['crew'] if w['department'] == 'Writing']

        credits.append({'cast': cast, 'directors': directors, 'writers': writers})
        return credits

    def get_movie_details(self, title, year, movie_id):
        """
        Gets genre, production companies, and avg rating of film from details TMDb API call
        :return: List of Dictionaries
        """
        details = []

        if movie_id is None:
            movie_id = self.get_movie_id(title, year)

        url = self.URL_DETAILS.format(movie_id) + self.api_key
        res = requests.get(url).json()

        genres = [g['name'] for g in res['genres']]
        production_co = [p['name'] for p in res['production_companies']]
        average_rating = res['vote_average']

        details.append({'genres': genres, 'production_companies': production_co, 'tmdb_rating': average_rating})
        return details

    def get_film_image(self, film):
        pass


if __name__ == '__main__':

    diary = [{'title': 'Vice', 'year': '2018', 'rating': '6'}, {'title': 'Magnolia', 'year': '1999', 'rating': '10'}, {'title': 'Roma', 'year': '2018', 'rating': '9'}, {'title': 'Children of Men', 'year': '2006', 'rating': '9'}, {'title': 'Black Mirror: Bandersnatch', 'year': '2018', 'rating': '5'}, {'title': 'Take Shelter', 'year': '2011', 'rating': '7'}, {'title': 'The Ballad of Buster Scruggs', 'year': '2018', 'rating': '7'}, {'title': 'Incredibles 2', 'year': '2018', 'rating': '6'}, {'title': 'Force Majeure', 'year': '2014', 'rating': '7'}, {'title': 'Sorry to Bother You', 'year': '2018', 'rating': '8'}, {'title': 'BlacKkKlansman', 'year': '2018', 'rating': '6'}, {'title': 'Hereditary', 'year': '2018', 'rating': '8'}, {'title': 'It Follows', 'year': '2014', 'rating': '7'}, {'title': 'Black Swan', 'year': '2010', 'rating': '9'}, {'title': 'Mandy', 'year': '2018', 'rating': '7'}, {'title': 'It', 'year': '2017', 'rating': '6'}, {'title': 'What We Do in the Shadows', 'year': '2014', 'rating': '8'}, {'title': 'Mamma Mia! Here We Go Again', 'year': '2018', 'rating': '4'}, {'title': 'Isle of Dogs', 'year': '2018', 'rating': '7'}, {'title': 'Thoroughbreds', 'year': '2017', 'rating': '7'}, {'title': 'The Disaster Artist', 'year': '2017', 'rating': '6'}, {'title': 'Solaris', 'year': '1972', 'rating': '0'}, {'title': 'Fallen Angels', 'year': '1995', 'rating': '8'}, {'title': 'The Master', 'year': '2012', 'rating': '7'}, {'title': 'Suspiria', 'year': '1977', 'rating': '9'}, {'title': 'Welcome to Leith', 'year': '2015', 'rating': '6'}, {'title': 'Death Note', 'year': '2017', 'rating': '3'}, {'title': 'There Will Be Blood', 'year': '2007', 'rating': '10'}, {'title': 'Cube 2: Hypercube', 'year': '2002', 'rating': '2'}, {'title': 'Cube', 'year': '1997', 'rating': '4'}, {'title': "One Flew Over the Cuckoo's Nest", 'year': '1975', 'rating': '9'}, {'title': 'Mulholland Drive', 'year': '2001', 'rating': '0'}, {'title': 'Star Wars: The Last Jedi', 'year': '2017', 'rating': '5'}, {'title': 'Coherence', 'year': '2013', 'rating': '6'}, {'title': 'Avengers: Infinity War', 'year': '2018', 'rating': '7'}, {'title': 'The One I Love', 'year': '2014', 'rating': '7'}, {'title': 'Annihilation', 'year': '2018', 'rating': '7'}, {'title': "The Devil's Backbone", 'year': '2001', 'rating': '9'}, {'title': 'Coco', 'year': '2017', 'rating': '7'}, {'title': 'Office Space', 'year': '1999', 'rating': '8'}, {'title': 'The Cloverfield Paradox', 'year': '2018', 'rating': '3'}, {'title': 'Good Time', 'year': '2017', 'rating': '8'}, {'title': 'The Shape of Water', 'year': '2017', 'rating': '8'}, {'title': 'Three Billboards Outside Ebbing, Missouri', 'year': '2017', 'rating': '7'}, {'title': 'The Killing of a Sacred Deer', 'year': '2017', 'rating': '7'}, {'title': 'The Death of Stalin', 'year': '2017', 'rating': '7'}, {'title': 'The Florida Project', 'year': '2017', 'rating': '9'}, {'title': 'Once', 'year': '2007', 'rating': '7'}, {'title': 'Blade Runner 2049', 'year': '2017', 'rating': '10'}, {'title': 'Blade Runner', 'year': '1982', 'rating': '9'}]

    m = TheMovieDatabaseAPI(TMDB_API_KEY)
    for entry in diary:
        # entry['details'] = m.get_movie_details(entry['title'], entry['year'], None)
        # time.sleep(0.55)    # MAX LIMIT: 4 requests per second
        # entry['credits'] = m.get_movie_credits(entry['title'], entry['year'], None)
        print(entry['title'])
        # time.sleep(0.55)

    print(diary)
