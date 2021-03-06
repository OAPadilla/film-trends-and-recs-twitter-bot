# LetterBot.ME Films Twitter Bot
Tweets [Letterboxd](https://letterboxd.com/)'s (a social movie site) weekly top films and trends every Saturday at 5 PM and replies to mentions with personalized movie recommendations based on a user's Letterboxd diary entries.

https://twitter.com/LetterBotFilm

Usage: Tweet to the bot account '@LetterBotFilm *[Letterboxd_username]*'

Hosted on a Raspberry Pi 3.

## Preview
![weekly popular films](https://i.imgur.com/imGuTLq.png)
![Recommendations](https://i.imgur.com/Z6FEglz.png)

## File List

### twitter_bot.py
Automates the twitter bot's functionalities on a schedule and uses StreamListener to receive twitter messages in real time. The Tweepy library was used for accessing the Twitter API.

### letterboxd_scraper.py, sqlite_db.py
A web scraper to collect Letterboxd’s most popular films of the week and a user’s recent movie entries and wish list using the Selenium and BeautifulSoup libraries. The collected data is stored on a SQLite database.

### recommender.py
A content-based movie recommender system based on the cosine similarities between vectorized film attributes from a generated user profile and TMDb datasets using the Pandas and Scikit-learn libraries.

### tmdb_api.py
Contains GET requests to TMDB API for movie metadata and poster.

### visualize.py
Generates charts for weekly popular films and recommended lists to be tweeted out using the Matplotlib library.

### /datasets/tmdb/
Contains 'tmdb_5000_credits.csv' and 'tmdb_5000_movies.csv' files provided by [The Movie Database (TMDb)](https://www.themoviedb.org/) and available on [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata/). These datasets include movie metadata used by the recommender system.

### /images/
Temporarily holds generated chart visuals in preperation to be tweeted.
