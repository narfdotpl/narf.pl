#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from codecs import open
from collections import defaultdict
import datetime
import json
from os import listdir
from os.path import join


from settings import API_JSON_DIR


class ArtistAndTrackBase(object):

    def __init__(self, name):
        self.name = name
        self.play_count_by_week = defaultdict(int)

    @property
    def first_week(self):
        return min(self.play_count_by_week.iterkeys())

    @property
    def total_play_count(self):
        return sum(self.play_count_by_week.itervalues())

    def get_play_count_for_week(self, week):
        return self.play_count_by_week[week]

    def get_play_count_for_group(self, group):
        return sum(self.get_play_count_for_week(week) for week in group.weeks)


class Artist(ArtistAndTrackBase):

    def __repr__(self):
        return self.name


class Track(ArtistAndTrackBase):

    def __init__(self, artist, title):
        super(Track, self).__init__(title)
        self.artist = artist

    def __repr__(self):
        return '%s - %s' % (self.artist, self.name)


class Week(object):

    def __init__(self, timestamp1, timestamp2):
        self.timestamp1 = int(timestamp1)
        self.timestamp2 = int(timestamp2)

        to_iso = lambda timestamp: \
            datetime.datetime.fromtimestamp(timestamp).date().isoformat()

        self.isodate1 = to_iso(self.timestamp1)
        self.isodate2 = to_iso(self.timestamp2)

        self.artists = set()
        self.tracks = set()

    def __repr__(self):
        return '%s - %s' % (self.isodate1, self.isodate2)

    @property
    def total_play_count(self):
        return sum(track.get_play_count_for_week(self) \
                   for track in self.tracks)


class Group(object):

    def __init__(self, weeks):
        self.weeks = weeks

    def __len__(self):
        return len(self.weeks)

    def __repr__(self):
        return '%s - %s' % (self.isodate1, self.isodate2)

    @property
    def artists(self):
        artists = set()
        for week in self.weeks:
            artists = artists | week.artists

        return artists

    @property
    def isodate1(self):
        return self.weeks[0].isodate1

    @property
    def isodate2(self):
        return self.weeks[-1].isodate2

    @property
    def most_played_artists_with_play_count(self):
        return self._most_played_x_with_play_count('artists')

    @property
    def most_played_tracks_with_play_count(self):
        return self._most_played_x_with_play_count('tracks')

    def _most_played_x_with_play_count(self, name):
        play_count_by_x = defaultdict(int)

        for week in self.weeks:
            for x in getattr(week, name):
                play_count = x.get_play_count_for_week(week)
                play_count_by_x[x] += play_count

        return sorted(play_count_by_x.iteritems(), key=lambda tpl: -tpl[1])

    @property
    def tracks(self):
        tracks = set()
        for week in self.weeks:
            tracks = tracks | week.tracks

        return tracks

    @property
    def total_play_count(self):
        return sum(week.total_play_count for week in self.weeks)


class Manager(object):

    def __init__(self, directory=API_JSON_DIR):
        # make place for data
        self.weeks = []
        self.artists_by_name = {}
        self.tracks_by_name = {}

        # read data
        self.read_data(directory)

    @property
    def artists(self):
        return self.artists_by_name.values()

    @property
    def tracks(self):
        return self.tracks_by_name.values()

    def group_weeks(self, n=4):
        # happy hacking: offset groups so that spotify period will start
        # near the beginning of a group
        offset = 2 if n == 4 else 0

        # group weeks into n-element lists
        xs = self.weeks
        lists = [xs[i:i + n] for i in range(offset, len(xs), n)]

        # remove lists shorter than n
        lists = filter(lambda xs: len(xs) == n, lists)

        return map(Group, lists)

    def read_data(self, directory):
        for name in listdir(directory):
            # skip non-JSON files
            if not name.endswith('.json') or name.startswith('.'):
                continue

            # read JSON
            path = join(directory, name)
            with open(path, 'r', encoding='utf-8') as f:
                dct = json.load(f)['weeklytrackchart']

            # create week object
            if '@attr' in dct:
                attributes = dct['@attr']
            else:
                attributes = dct
            week = Week(attributes['from'], attributes['to'])
            self.weeks.append(week)

            # skip weeks with no track data
            if 'track' not in dct:
                continue

            # get tracks and artists
            for d in dct['track']:
                # get artist
                name = d['artist']['#text']
                artist = self.artists_by_name.get(name, None)
                if not artist:
                    artist = Artist(name)
                    self.artists_by_name[name] = artist

                # add artist to week
                week.artists.add(artist)

                # get track
                title = d['name']
                name = '%s - %s' % (artist, title)
                track = self.tracks_by_name.get(name, None)
                if not track:
                    track = Track(artist, title)
                    self.tracks_by_name[name] = track

                # add track to week
                week.tracks.add(track)

                # save play count
                play_count = int(d['playcount'])
                artist.play_count_by_week[week] += play_count
                track.play_count_by_week[week] = play_count

        # remove first weeks with no tracks played (find split index)
        for i, week in enumerate(self.weeks):
            if week.total_play_count > 0:
                break
        self.weeks = self.weeks[i:]
