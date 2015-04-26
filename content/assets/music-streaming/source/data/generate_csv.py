#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os.path import join

import models
from settings import CHART_CSV_DIR

# load data
manager = models.Manager()
groups = manager.group_weeks()


def csv(function):
    """
    Because DSLs and non-descriptive names.
    """

    # open CSV file
    name = function.__name__
    path = join(CHART_CSV_DIR, '%s.csv' % name.replace('_', '-'))
    with open(path, 'w') as f:
        # DRY
        write = lambda xs: f.write('%s\n' % ','.join(map(str, xs)))

        for i, group in enumerate(groups):
            # get values
            xs = function(group)
            if not isinstance(xs, tuple):
                xs = (xs,)

            # add column names
            if i == 0:
                column_names = ['date']
                for j in range(len(xs)):
                    column_names.append('v%d' % (j + 1))

                write(column_names)

            # add row
            write([group.isodate1] + list(xs))


global_old_tracks = global_old_artists = None


def _main():
    @csv
    def play_count(group):
        # get total play count
        total = group.total_play_count

        # get play count of top X most played artists
        x = 20
        top = sum(play_count for artist, play_count in
                    group.most_played_artists_with_play_count[:x])

        return top, total - top

    global global_old_tracks
    global_old_tracks = set()

    @csv
    def play_count_new_old_tracks(group):
        global global_old_tracks
        new = 0
        old = 0

        for track in group.tracks:
            n = track.get_play_count_for_group(group)
            if track in global_old_tracks:
                old += n
            else:
                new += n

            global_old_tracks.add(track)

        return new, old

    global global_old_artists
    global_old_artists = set()

    @csv
    def play_count_new_old_artists(group):
        global global_old_artists
        new = 0
        old = 0

        for artist in group.artists:
            n = artist.get_play_count_for_group(group)
            if artist in global_old_artists:
                old += n
            else:
                new += n

            global_old_artists.add(artist)

        return new, old

    global_old_tracks = set()

    @csv
    def tracks(group):
        global global_old_tracks
        n = len(group.tracks - global_old_tracks)
        global_old_tracks |= group.tracks

        return n, len(group.tracks) - n

    global_old_artists = set()

    @csv
    def artists(group):
        global global_old_artists
        n = len(group.artists - global_old_artists)
        global_old_artists |= group.artists

        return n, len(group.artists) - n


if __name__ == '__main__':
    _main()
