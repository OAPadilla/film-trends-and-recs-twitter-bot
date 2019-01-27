
"""recommender.py: Content-based filtering movie recommender system."""

import os
import time
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ast import literal_eval
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
        if int(entry['rating']) >= 7:
            # GET API request to TMDb API for movie details of entry
            d = m.get_movie_details(entry['title'], entry['year'], None)
            entry['genres'] = d[0]['genres']
            entry['production_companies'] = d[0]['production_companies']
            entry['vote_average'] = d[0]['vote_average']
            time.sleep(0.55)  # MAX LIMIT: 4 requests per second

            # GET API request to TMDb API for movie credits of entry
            c = m.get_movie_credits(entry['title'], entry['year'], None)
            entry['cast'] = c[0]['cast']
            entry['directors'] = c[0]['directors']
            entry['writers'] = c[0]['writers']
            time.sleep(0.55)

    diary_df = pd.DataFrame(diary)

    return diary_df


def condense_terms(block):
    """
    Removes spaces and coverts characters in a array or string to lower case
    :return: String, or List of Strings
    """
    if isinstance(block, str):
        return str.lower(block.replace(" ", ""))
    elif isinstance(block, list):
        return [str.lower(term.replace(" ", "")) for term in block]
    return ''


def make_soup(df):
    """
    Creates word soup of all the relevant metadata of a dataframe
    :return: String
    """
    # Condenses metadata terms, lowercase and no spaces
    tmp_df = df.copy()
    tmp_df = tmp_df.apply(condense_terms)
    # Adjust weight of metadata for soup
    soup = tmp_df['genres']*2 + tmp_df['production_companies'] + tmp_df['cast'] + tmp_df['directors']*2 + tmp_df['writers']
    return ' '.join(soup)


def make_sim_matrix(df1_soup, df2_soup):
    """
    Cosine similarity, a measure of similarity between two vectors, is used to create a
    similarity matrix between films vectorized with the metadata word soup.
    :return: List of Lists of Decimal Floats
    """
    # Frequency counter matrices
    count = CountVectorizer()
    matrix1 = count.fit_transform(df1_soup)
    matrix2 = count.transform(df2_soup)
    # Cosine similarity matrix
    similarity_matrix = cosine_similarity(matrix2, matrix1)

    return similarity_matrix


def get_recs(metadata_df, user_profile_df, sim_matrix):
    """
    Finds list of films to recommend using cosine similarities of the metadata for each film
    :return: List of Dictionaries
    """
    recommended_films = []

    # md_indices = pd.Series(metadata_df.index, index=metadata_df['title'])
    up_indices = pd.Series(user_profile_df.index, index=user_profile_df['title'])

    for film in user_profile_df['title']:
        # Get index of film in user_profile row
        idx = up_indices[film]
        # Get cosine sims for row of current film from user_profile, sort them
        similarity_vals = pd.Series(sim_matrix[idx]).sort_values(ascending=False)
        # Store the indices of the top 10 highest cosine sims
        rec_indices = list(similarity_vals.iloc[1:4].index)
        # Append the recommended films based on current film to our list
        recommended_films.append(metadata_df['title'].iloc[rec_indices])

    # Filter long list of recs down to 15 HERE
    recommended_films = filter_recs(metadata_df, user_profile_df, recommended_films)
    # Return movie_id, title
    return recommended_films


def filter_recs(df, up_df, recommended_films):
    """
    Filters recommended films from hundreds to the top 10
    :return: List of Dictionaries
    """
    recs = []
    count = {}
    for row in recommended_films:
        for film in row:
            # Filter out films already seen recently from diary entries
            if (up_df['title'] == film).any():
                continue
            # Filter out if TMDb vote count too low
            if df.loc[df['title'] == film]['vote_count'].iloc[0] > 250 \
                    and df.loc[df['title'] == film]['vote_average'].iloc[0] > 6.0:
                # Add movie_id
                m_id = df.loc[df['title'] == film]['movie_id'].iloc[0]
                recs.append({'movie_id': m_id, 'title': film})
                if m_id in count:
                    count[m_id] += 1
                else:
                    count[m_id] = 1

    print("Amount of Films: " + str(len(recs)))
    # Add counts of frequency
    for m in recs:
        m['count'] = count[m['movie_id']]

    # Remove duplicates in recs
    result = []
    for i in range(len(recs)):
        if recs[i] not in recs[i+1:]:
            result.append(recs[i])

    # Sort by frequency count
    result = sorted(result, key=lambda k: k['count'], reverse=True)

    return result[:10]


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

    # Create dataset df from TMDb dataset metadata
    metadata_df = create_metadata_dataframe()
    # Create user profile df from diary
    user_profile_df = create_user_profile(diary)
    # Create word soup
    metadata_df['soup'] = metadata_df.apply(make_soup, axis=1)
    user_profile_df['soup'] = user_profile_df.apply(make_soup, axis=1)
    # Create Cosine Similarity Matrix between dataset metadata and user profile soups
    sim_matrix = make_sim_matrix(metadata_df['soup'], user_profile_df['soup'])
    # Get recommendations for films in diary df
    get_recs(metadata_df, user_profile_df, sim_matrix)

