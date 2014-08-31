#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os.path import dirname, join, realpath

from fabric.api import cd, env, lcd, local, run, task


CURRENT_DIR = dirname(realpath(__file__))
REPO_DIR = CURRENT_DIR
CONTENT_DIR = join(REPO_DIR, 'content')
ENGINE_DIR = join(REPO_DIR, 'engine')

REMOTE_APP_DIR = '~/narf.pl/main'


env.hosts = ['narf@narf.megiteam.pl']


@task
def checkout(branch=None):
    'Checkout branch in production. Use current branch by default.'

    if branch is None:
        branches = local('git branch', capture=True).split('\n')
        predicate = lambda s: s.startswith('*')
        branch = filter(predicate, branches)[0].lstrip('*').strip()

    with cd(REMOTE_APP_DIR):
        run('git checkout %s' % branch)


@task
def deploy():
    'Update production with latest changes.'
    # aka push, pull, checkout, pull, install, restart, visit

    local('git push private')

    with cd(REMOTE_APP_DIR):
        run('git pull')

    checkout()

    with cd(REMOTE_APP_DIR):
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
def js():
    'Compile CoffeeScript.'

    with lcd(join(CONTENT_DIR, 'assets', 'index')):
        local('coffee --print script.coffee | '
              'uglifyjs --no-copyright > script.js')

@task
def publish():
    'Publish to GitHub and deploy to production.'

    deploy()
    local('git push public')


@task
def restart():
    'Restart production.'

    run('restart-app main')


@task
def visit():
    'Visit http://narf.pl/.'

    local('open http://narf.pl/')
