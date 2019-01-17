#!/usr/bin/env python3

"""letterboxd_scraper.py: Scrapes information from Letterboxd, a social network site for film."""

import re
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__author__ = "Oscar Antonio Padilla"
__email__ = "PadillaOscarA@gmail.com"
__status__ = "Development"


class LetterboxdScraper:

    DRIVER_PATH = r'C:\Users\Oscar\AppData\Local\Google\Chrome\chromedriver.exe'
    URL_WATCHLIST = "https://letterboxd.com/{}/watchlist/"
    URL_DIARY = 'https://letterboxd.com/{}/films/diary/'
    URL_POP_FILMS = 'https://letterboxd.com/films/'

    def __init__(self):
        self.driver_path = LetterboxdScraper.DRIVER_PATH
        self.driver = None

    def open_browser(self):
        """
        Starts the web browser/driver in icognito mode.
        """
        print('Starting driver...')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)

    def close_browser(self):
        """
        Closes the web browser/driver.
        """
        self.driver.quit()
        print("Driver closed.")

    def get_html(self, url):
        """
        Navigates driver to link, interacts with page, and extracts the HTML with JS included.
        :return: String
        """
        self.driver.get(url)
        sleep(0.5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        inner_html = self.driver.execute_script("return document.body.innerHTML")
        return inner_html

    def get_watchlist_films(self, username):
        """
        Downloads watchlist page with url, and parses film titles.
        :return: Array of Dictionaries
        """
        url = LetterboxdScraper.URL_WATCHLIST.format(username)
        inner_html = self.get_html(url)
        watchlist = []

        try:
            soup = BeautifulSoup(inner_html, 'html.parser')
            films = soup.find_all('li', {'class': 'poster-container'})

            for film in films:
                film_title = film.div['data-film-name']
                film_year = film.div['data-film-release-year']

                watchlist.append({"title": film_title, "year": film_year})
        except NoSuchElementException as e:
            print(e)

        return watchlist

    def get_recent_diary_entries(self, username):
        """
        Downloads diary entry page with url, and parses film titles, years, and ratings.
        :return: Array of Dictionaries
        """
        url = LetterboxdScraper.URL_DIARY.format(username)
        inner_html = self.get_html(url)
        diary = []

        try:
            soup = BeautifulSoup(inner_html, 'html.parser')
            entries = soup.find_all('tr', {'class': 'diary-entry-row'})

            for entry in entries:
                film_detail = entry.find('td', {'class': 'td-film-details'})
                entry_title = film_detail.div['data-film-name']
                entry_year = film_detail.div['data-film-release-year']
                entry_rating = entry.find('td', {'class': 'td-rating rating-green'}).div.span.meta['content']

                diary.append({"title": entry_title, "year": entry_year, "rating": entry_rating})
        except NoSuchElementException as e:
            print(e)

        return diary

    def get_popular_films(self):
        """
        Downloads popular films of the week with url, parses film ranks, titles, years, number of watches,
        and number of likes.
        :return: Array of Dictionaries
        """
        inner_html = self.get_html(LetterboxdScraper.URL_POP_FILMS)
        popular = []

        try:
            soup = BeautifulSoup(inner_html, 'html.parser')
            films = soup.find_all('li', {'class': 'listitem'})
            num_ranks = 8
            count = 0

            for film in films:
                # Keep count/rank as 'films' is iterated through.
                # If we want to go beyond the first 8, we must use Selenium to scroll right.
                if count == num_ranks:
                    break
                count += 1

                film_rank = count
                film_title = film.div['data-film-name']
                film_year = film.div['data-film-release-year']

                watches = film.find('li', {'class': 'stat filmstat-watches'}).a['data-original-title']
                watches = "".join(re.findall("[0-9]", watches))

                likes = film.find('li', {'class': 'stat filmstat-likes'}).a['data-original-title']
                likes = "".join(re.findall("[0-9]", likes))

                popular.append({"rank": film_rank, "title": film_title, "year": film_year,
                                "watches": int(watches), "likes": int(likes)})
        except NoSuchElementException as e:
            print(e)

        return popular


if __name__ == '__main__':

    user = "narrowlightbulb"

    lb = LetterboxdScraper()
    lb.open_browser()
    #print(lb.get_watchlist_films(user))
    #print(lb.get_recent_diary_entries(user))
    #print(lb.get_popular_films())
    lb.close_browser()
