
"""recommender.py: Content-based movie recommender system."""

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
# 3. Add to json result
