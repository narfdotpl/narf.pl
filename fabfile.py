#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os.path import dirname, realpath

from fabric.api import lcd, local, task


CURRENT_DIR = dirname(realpath(__file__))
REPO_DIR = CURRENT_DIR


@task
def dev():
    'Run development sever.'

    local('open http://localhost:5000/')

    with lcd(REPO_DIR):
        local('python engine/main.py')


@task
def visit():
    'Visit http://narf.pl/.'

    local('open http://narf.pl/')
