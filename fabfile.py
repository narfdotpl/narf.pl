#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os import walk
from os.path import dirname, join, realpath
from sys import stdout

from fabric.api import cd, hosts, lcd, local, quiet, run, task


CURRENT_DIR = dirname(realpath(__file__))
REPO_DIR = CURRENT_DIR
CONTENT_DIR = join(REPO_DIR, 'content')
ENGINE_DIR = join(REPO_DIR, 'engine')
TESTS_DIR = join(REPO_DIR, 'tests')
POSTS_DIR = join(CONTENT_DIR, 'posts')



@task
def deploy():
    'Update production with latest changes.'

    test()
    local('git push --force-with-lease dokku HEAD:master')
    visit()


@task
def dev():
    'Run development sever.'

    local('open http://localhost:5000/')

    with lcd(ENGINE_DIR):
        local('python main.py')


@task
def js():
    'Compile CoffeeScript.'

    with lcd(join(CONTENT_DIR, 'javascript')):
        local('./generate-main-js')

@task
def publish():
    'Publish to GitHub and deploy to production.'

    deploy()
    local('git push public')


@hosts('')
@task
def test():
    'Test differences in rendering.'

    reference = 'reference.txt'
    output = 'output.txt'

    with lcd(TESTS_DIR):
        def curl(path):
            local('curl http://localhost:5000%s >> %s' % (path, output))
            stdout.write('.')
            stdout.flush()

        with quiet():
            local('echo > ' + output)
            curl('/')
            curl('/feed')
            curl('/feed.json')
            curl('/posts')

            for root, dirnames, filenames in walk(POSTS_DIR):
                for filename in sorted(filenames):
                    if filename.startswith('.'): continue
                    if not filename.endswith('.md'): continue

                    curl('/posts/%s' % filename[:-len('.md')])

            stdout.write('\n')
            stdout.flush()

        local('git diff --no-index -- %s %s' % (reference, output))


@hosts('')
@task
def test_accept():
    'Accept test results.'

    with lcd(TESTS_DIR):
        local('rm {reference} || true; mv {output} {reference}'.format(**{
            'reference': 'reference.txt',
            'output': 'output.txt',
        }))

@task
def visit():
    'Visit http://narf.pl/.'

    local('open http://narf.pl/')
