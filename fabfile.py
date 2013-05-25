#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os.path import dirname, join, realpath

from fabric.api import cd, env, lcd, local, run, task


CURRENT_DIR = dirname(realpath(__file__))
REPO_DIR = CURRENT_DIR
ENGINE_DIR = join(REPO_DIR, 'engine')


env.hosts = ['narf@narf.megiteam.pl']


@task
def deploy():
    'Update production with latest changes.'
    # aka push, pull, install, restart, visit

    local('git push')

    with cd('~/narf.pl/main'):
        run('git pull')
        run('source engine/.environment && pip install -r requirements.txt')

    restart()
    visit()


@task
def dev():
    'Run development sever.'

    # symlink static directory
    with lcd(ENGINE_DIR):
        local('rm -rf static; true')
        local('ln -s {_,}static')

        # open browser
        local('open http://localhost:5000/')

        # run server
        local('python main.py')


@task
def restart():
    'Restart production.'

    run('restart-app main')


@task
def visit():
    'Visit http://narf.pl/.'

    local('open http://narf.pl/')
