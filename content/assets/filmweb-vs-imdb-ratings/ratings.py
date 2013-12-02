#!/usr/bin/env python
# encoding: utf-8
"""
Get movie ratings from Filmweb Top 500 ranking, search for each movie on
IMDb, get its rating, and save results in a CSV file.
"""

from __future__ import absolute_import, division
import re

from bs4 import BeautifulSoup
import requests


class Movie(object):

    def __init__(self, title, year, filmweb_rating):
        self.title = title
        self.year = year
        self.filmweb_rating = filmweb_rating
        self.imdb_rating = None

    def __str__(self):
        return u'"%s" (%d)' % (self.title, self.year)

    @property
    def csv(self):
        xs = [self.title, self.year, self.filmweb_rating, self.imdb_rating]
        return u'\t'.join(map(unicode, xs))

    def get_imdb_rating(self):
        url = 'http://www.imdb.com/search/title'
        params = {
            'release_date': '%d,%d' % (self.year, self.year),
            'title': self.title,
        }
        html = requests.get(url, params=params).text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', {'class': 'results'})

        # quit if there are no results
        if not table:
            return

        for row in table.find_all('tr'):
            span = row.find('span', {'class': 'rating-rating'})
            if span:
                rating_string = get_text(span.find('span', {'class': 'value'}))

                try:
                    self.imdb_rating = float(rating_string)
                except ValueError:
                    return
                else:
                    return self.imdb_rating


whitespace_regex = re.compile(r'\s+')

def get_text(tag):
    return whitespace_regex.sub(' ', tag.text.strip())


def get_top_500_filmweb_movies():
    movies = []

    url = 'http://www.filmweb.pl/rankings/film/world'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'class': 'rankingTable'})

    for row in table.find_all('tr'):
        div = row.find('div', {'class': 'ohidden'})
        if not div:
            continue

        # get Polish title
        polish_title = get_text(div.find('a'))

        # get other info
        other_info = get_text(row.find('div', {'class': 'filmOtherInfo'}))
        components = other_info.split(' ')

        # get year
        year = int(components.pop())

        # get international title
        if components:
            title = ' '.join(components)
        else:
            title = polish_title

        # get rating
        rating_string = get_text(row.find('td', {'class': 'averageRate'}))
        rating = float(rating_string.replace(',', '.'))

        # add movie
        movies.append(Movie(title, year, rating))

    return movies


def _main():
    for movie in get_top_500_filmweb_movies()[140:]:
        movie.get_imdb_rating()
        if movie.imdb_rating:
            print movie.csv

if __name__ == '__main__':
    _main()
