#!/usr/bin/env python
# encoding: utf-8
"""
Print three CSV columns: "IMDb rating", "Filmweb rating", and "Scale",
where "Scale" is determined by the number of the same rating pairs.
"""

from __future__ import absolute_import, division
from collections import Counter
from os.path import dirname, join, realpath


CURRENT_DIR = dirname(realpath(__file__))
CSV_PATH = join(CURRENT_DIR, 'ratings.csv')

MIN_SCALE = 0.4
MAX_SCALE = 1.5


def _main():
    pairs = []

    with open(CSV_PATH) as f:
        for line in f:
            _, __, filmweb_rating_string, imdb_rating_string = line.split('\t')
            pairs.append((float(imdb_rating_string),
                          round(float(filmweb_rating_string), 1)))

    pairs_counter = Counter(pairs)
    max_count = max(pairs_counter.itervalues())

    for (imdb_rating, filmweb_raiting), count in pairs_counter.iteritems():
        scale = MIN_SCALE + (MAX_SCALE - MIN_SCALE) * \
            (count - 1) / (max_count - 1)
        print ','.join(map(str, [imdb_rating, filmweb_raiting, scale]))

if __name__ == '__main__':
    _main()
