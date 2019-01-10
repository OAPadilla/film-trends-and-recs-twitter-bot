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


# class LetterboxdScraper:
#
#     def __init__(self, url_list):
#         self.url_list = url_list
#
#     def open_browser(self):
#         print('Starting driver...')
#
#



def simple_get_html(url):
    """
    HTTP GET request
    """
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_response(res):
                return res.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(res):
    """
    Returns True if response is HTML
    """
    content_type = res.headers['Content-Type'].lower()
    return (res.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Prints error logs
    """
    print(e)


def get_names():
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    url = 'http://www.fabpedigree.com/james/mathmen.htm'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = set()
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    names.add(name.strip())
        return list(names)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))


def get_top_films_of_the_week():
    """
    Downloads Letterboxd weekly top movies.
    :return: List of strings
    """
    url = 'https://letterboxd.com/films/popular/this/week/'
    response = simple_get_html(url)

    if response is not None:
        soup = BeautifulSoup(response, 'html.parser')
        movies = set()

        return list(soup.children)

    raise Exception('Error retrieving contents at {}'.format(url))


def get_film_details():
    return


def get_diary_entry():
    return


def get_watchlist_titles(url):
    watchlist_titles = []
    innerHTML = driver.execute_script("return document.body.innerHTML")

    # parse with BeautifulSoup

    return watchlist_titles


def get_title_by_text(text):
    """Find title in the page with given text"""
    element = driver.find_element_by_class_name


def get_title_by_class_name(class_name):
    element_list = []
    try:
        all_elements = driver.find_elements_by_class_name(class_name)
        element_list = [x.text for x in all_elements if len(x.text) > 0]
    except (NoSuchElementException, WebDriverException) as e:
        print(e)
    return element_list


if __name__ == '__main__':
    print('Start...')

    url_watchlist = "https://letterboxd.com/narrowlightbulb/watchlist/"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    # create new instance of Chrome
    # FIXME: webdriver has personal pathname, maybe keep it in project folder
    driver = webdriver.Chrome(executable_path=r'C:\Users\Oscar\AppData\Local\Google\Chrome\chromedriver.exe',
                              chrome_options=options)
    driver.get(url_watchlist)

    watchlist = get_watchlist_titles(url_watchlist)

    driver.quit()



