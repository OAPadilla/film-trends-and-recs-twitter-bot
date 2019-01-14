#!/bin/python

from requests import get
from requests.exceptions import RequestException 
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver                                      #launch/initialize a browser
from selenium.webdriver.common.by import By                         #to search for things using specific params
from selenium.webdriver.support.ui import WebDriverWait             #for waiting for a page load
from selenium.webdriver.support import expected_conditions as EC    #specify what you're looking for on specific page in order to determine that the webpage has loaded
from selenium.common.exceptions import TimeoutException, \
    NoSuchElementException, WebDriverException                      #handling a timeout situation
from time import sleep


class LetterboxdScraper:

    def __init__(self, dp):
        self.driver_path = dp

    # Start the web browser/driver
    def open_browser(self):
        print('Starting driver...')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)

    # Close the web browser/driver
    def close_browser(self):
        self.driver.quit()
        print("Driver closed.")

    # Gets inner HTML of browser page
    def get_html(self, url):
        """
        Navigates driver to link, scrolls to bottom of page, and extracts the HTML with JS incl
        :return: string
        """
        self.driver.get(url)
        sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        inner_html = self.driver.execute_script("return document.body.innerHTML")
        return inner_html

    def get_watchlist_films(self, url):
        """
        Downloads watchlist page with url, parses film titles
        :return: string array
        """
        inner_html = self.get_html(url)

        if inner_html is not None:
            soup = BeautifulSoup(inner_html, 'html.parser').find_all("span", {"class": "frame-title"})
            films = [x.get_text() for x in soup]
            return films
        raise Exception('Error retrieving contents at {}'.format(url))

    def get_recent_diary_entries(self, url):
        """
        Downloads diary entry page with url, parses film titles, years, and ratings
        :return: string array
        """
        inner_html = self.get_html(url)

        if inner_html is not None:
            diary = []

            soup = BeautifulSoup(inner_html, 'html.parser')
            entries = soup.find_all('tr', {'class': 'diary-entry-row'})

            for entry in entries:
                film_detail = entry.find('td', {'class': 'td-film-details'})
                entry_title = film_detail.div['data-film-name']
                entry_year = film_detail.div['data-film-release-year']
                entry_rating = entry.find('td', {'class': 'td-rating rating-green'}).div.span.meta['content']

                diary.append({"title": entry_title, "year": entry_year, "rating": entry_rating})

            return diary
        raise Exception('Error retrieving contents at {}'.format(url))

    # Gets Letterboxd's most popular films of the week
    def get_popular_films(self, url):
        pop_films = []
        inner_html = self.get_html(url)

        # parse with BeautifulSoup

        return pop_films


if __name__ == '__main__':
    url_watchlist = "https://letterboxd.com/narrowlightbulb/watchlist/"
    url_diary = 'https://letterboxd.com/narrowlightbulb/films/diary/'
    url_pop_films = 'https://letterboxd.com/films/'

    driver_path = r'C:\Users\Oscar\AppData\Local\Google\Chrome\chromedriver.exe'

    lb = LetterboxdScraper(driver_path)
    lb.open_browser()
    #lb.get_watchlist_films(url_watchlist)
    lb.get_recent_diary_entries(url_diary)
    lb.close_browser()




# def simple_get_html(url):
#     """
#     HTTP GET request
#     """
#     try:
#         with closing(get(url, stream=True)) as res:
#             if is_good_response(res):
#                 return res.content
#             else:
#                 return None
#
#     except RequestException as e:
#         log_error('Error during requests to {0} : {1}'.format(url, str(e)))
#         return None
#
#
# def is_good_response(res):
#     """
#     Returns True if response is HTML
#     """
#     content_type = res.headers['Content-Type'].lower()
#     return (res.status_code == 200
#             and content_type is not None
#             and content_type.find('html') > -1)
#
#
# def log_error(e):
#     """
#     Prints error logs
#     """
#     print(e)
#
#
# def get_names():
#     """
#     Downloads the page where the list of mathematicians is found
#     and returns a list of strings, one per mathematician
#     """
#     url = 'http://www.fabpedigree.com/james/mathmen.htm'
#     response = simple_get(url)
#
#     if response is not None:
#         html = BeautifulSoup(response, 'html.parser')
#         names = set()
#         for li in html.select('li'):
#             for name in li.text.split('\n'):
#                 if len(name) > 0:
#                     names.add(name.strip())
#         return list(names)
#
#     # Raise an exception if we failed to get any data from the url
#     raise Exception('Error retrieving contents at {}'.format(url))
#
#
# def get_top_films_of_the_week():
#     """
#     Downloads Letterboxd weekly top movies.
#     :return: List of strings
#     """
#     url = 'https://letterboxd.com/films/popular/this/week/'
#     response = simple_get_html(url)
#
#     if response is not None:
#         soup = BeautifulSoup(response, 'html.parser')
#         movies = set()
#
#         return list(soup.children)
#
#     raise Exception('Error retrieving contents at {}'.format(url))
#
#
# def get_title_by_class_name(class_name):
#     element_list = []
#     try:
#         all_elements = driver.find_elements_by_class_name(class_name)
#         element_list = [x.text for x in all_elements if len(x.text) > 0]
#     except (NoSuchElementException, WebDriverException) as e:
#         print(e)
#     return element_list



