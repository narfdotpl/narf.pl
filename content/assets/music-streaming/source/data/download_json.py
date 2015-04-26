#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from codecs import open
import json
from os.path import exists, join
from time import sleep

import requests

from settings import API_JSON_DIR, API_KEY, USERNAME

def get_chart_path(timestamp1, timestamp2):
    return join(API_JSON_DIR, '%s-%s.json' % (timestamp1, timestamp2))


def query_api(params):
    # provide default params
    default_params = {
        'api_key': API_KEY,
        'format': 'json',
    }
    default_params.update(params)
    params = default_params

    # get JSON
    url = 'http://ws.audioscrobbler.com/2.0/'
    json_string = requests.get(url, params=params).text

    return json.loads(json_string)


def _main():
    # get weekly track charts for each timestamp range
    dct = query_api({
        'method': 'user.getWeeklyChartList',
        'user': USERNAME,
    })
    charts = dct['weeklychartlist']['chart']

    for i, d in enumerate(reversed(charts), start=1):
        # get file path
        a, b = d['from'], d['to']
        path = get_chart_path(a, b)

        # skip if file exists
        if exists(path):
            i += 1
            continue

        # download
        print 'downloading data for week %i of %i' % (i, len(charts))
        weekly_dict = query_api({
            'method': 'user.getWeeklyTrackChart',
            'user': USERNAME,
            'from': a,
            'to': b,
        })

        # save
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(weekly_dict, sort_keys=True, indent=4))

        # don't spam
        sleep(0.25)


if __name__ == '__main__':
    _main()
