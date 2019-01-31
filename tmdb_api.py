
"""tmdb_api.py: Makes HTTP GET requests for movie information to The Movie Database API"""

import requests
import wget

from secrets import *

__author__ = "Oscar Antonio Padilla"
__email__ = "PadillaOscarA@gmail.com"
__status__ = "Development"


class TheMovieDatabaseAPI:

    URL_SEARCH = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'
    URL_CREDITS = 'https://api.themoviedb.org/3/movie/{}/credits?api_key='
    URL_DETAILS = 'https://api.themoviedb.org/3/movie/{}?api_key='
    URL_IMAGE = 'https://image.tmdb.org/t/p/w200'

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
            if res['total_results'] == 0:
                return None
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

        if movie_id is None:
            return None

        url = self.URL_DETAILS.format(movie_id) + self.api_key
        res = requests.get(url).json()

        # For metadata analysis
        genres = [g['name'] for g in res['genres']]
        production_co = [p['name'] for p in res['production_companies']]
        average_rating = res['vote_average']

        details.append({'genres': genres, 'production_companies': production_co, 'vote_average': average_rating})
        return details

    def download_movie_poster(self, m_id, directory):
        """
        Gets poster url path of film from details TMDb API call and downloads the image into a directory
        """
        # Get poster path from movie details request
        url = self.URL_DETAILS.format(m_id) + self.api_key
        res = requests.get(url).json()
        path = res['poster_path']

        full_url = self.URL_IMAGE + path

        # Download url image to /images directory
        wget.download(full_url, out=directory)
