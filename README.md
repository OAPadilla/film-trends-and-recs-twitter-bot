# LetterBot.ME Films Twitter Bot
Tweets [Letterboxd](https://letterboxd.com/)'s (a social movie site) weekly top films and trends every Saturday at 5 PM and replies to @mentions with personalized movie recommendations based on a user's Letterboxd diary entries.

https://twitter.com/LetterBotFilm

## Preview


## File List

### twitter_bot.py
Automates the twitter bot's functionalities on a schedule and uses StreamListener to receive twitter messages in real time. The Tweepy library was used for accessing the Twitter API.

### letterboxd_scraper.py, sqlite_db.py
Web scraper using the Selenium and BeautifulSoup libraries to collect Letterboxd’s most popular films of the week and a user’s recent movie entries and wish list. The collected data is stored on a SQLite database.

### recommender.py, tmdb_api.py
A content-based movie recommender system based on the cosine similarities between vectorized film attributes from a generated user profile and a TMDb dataset using the Pandas and Scikit-learn libraries.

### visualize.py
Generates charts for weekly popular films and recommended lists to be tweeted out using the Matplotlib library.

### /datasets/tmdb/
Stores 'tmdb_5000_credits.csv' and 'tmdb_5000_movies.csv' files provided by [The Movie Database (TMDb)](https://www.themoviedb.org/) and is available on [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata/). These datasets include movie metadata used by the recommender system.

### /images/
Stores temporarily generated chart visuals in preperation to be tweeted.
