#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os import walk, system
from os.path import dirname, exists, join, realpath

current_directory = dirname(realpath(__file__))
full_images_directory_name = 'full'
miniatures_directory_name = 'min'


def _main():
    full_dir = join(current_directory, full_images_directory_name)
    min_dir = join(current_directory, miniatures_directory_name)

    screen_shot_names = []

    for (_, __, file_names) in walk(full_dir):
        for file_name in file_names:
            if file_name.endswith('.png'):
                screen_shot_names.append(file_name)

    for name in sorted(screen_shot_names):
        full_path = join(full_dir, name)
        min_path = join(min_dir, name)

        if not exists(min_path):
            system("convert '%s' -resize 642x361 -shave 1x0 '%s'" % \
                (full_path, min_path))

            system("optipng '%s' 2> /dev/null" % full_path)
            system("optipng '%s' 2> /dev/null" % min_path)

        print '[![](%s/%s)](%s/%s)\n' % \
            (miniatures_directory_name, name,
             full_images_directory_name, name)

if __name__ == '__main__':
    _main()
