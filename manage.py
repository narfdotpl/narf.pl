#!/usr/bin/env python
# encoding: utf-8

from os import system as os_system, walk
from pathlib import Path
from sys import argv

CURRENT_DIR = Path(__file__).absolute().parent
REPO_DIR = CURRENT_DIR
CONTENT_DIR = REPO_DIR / 'content'
LOGS_DIR = REPO_DIR / 'logs'
TESTS_DIR = REPO_DIR / 'tests'
POSTS_DIR = CONTENT_DIR / 'posts'

TASKS = {}


def system(command):
    """
    Run a shell command and exit if it fails.
    """

    result = os_system(command)
    if result > 0:
        exit(1)


def task(func):
    TASKS[func.__name__] = func
    return func


def get_post_paths():
    for root, dirnames, filenames in walk(POSTS_DIR):
        for filename in sorted(filenames):
            if filename.startswith('.'): continue
            if not filename.endswith('.md'): continue

            slug = filename[:-len('.md')]
            yield f'/posts/{slug}'


def get_all_paths():
    yield from [
        '/',
        '/404',
        '/feed',
        '/feed.json',
        '/about',
        '/music',
        '/posts',
    ]
    yield from get_post_paths()


@task
def deploy():
    'Update production with latest changes.'

    test()
    logs_fetch()
    system('git push --force private HEAD:master')
    visit()
    system('open https://dashboard.render.com')


@task
def runserver():
    'Run development sever.'

    system('f() { sleep 0.2; open http://localhost:8000; }; f &')
    system('cd "%s"; PYTHONPATH="${PYTHONPATH}:$(pwd)" python engine/main.py' % REPO_DIR)


@task
def js():
    'Generate main JavaScript file.'

    js_dir = CONTENT_DIR / 'javascript'
    system(f'cd "{js_dir}"; ./generate-main-js')


@task
def logs_fetch():
    # TODO: get logs from Render
    pass
    # logs start at the last deployment
    # system(f"ssh dokku -t 'docker logs $(cat /home/dokku/narf.pl/CONTAINER.web.1)' | gzip > \"{LOGS_DIR}/$(date +%Y-%m-%d_%H%M).txt.gz\"")


@task
def logs_show():
    system(f"cd \"{LOGS_DIR}\"; gunzip -c $(ls *.txt.gz) | ag -v 'GET /static' | goaccess -o html > index.html && open index.html")


@task
def publish():
    'Publish to GitHub and deploy to production.'

    deploy()
    system('git push public')


@task
def test():
    'Run Python tests and test differences in rendering.'

    reference = TESTS_DIR / 'reference.txt'
    output = TESTS_DIR / 'output.txt'

    # run doctests
    system('cd "%s"; PYTHONPATH="${PYTHONPATH}:$(pwd)" python engine/main.py test' % REPO_DIR)

    def curl(path):
        system(f'curl -L http://localhost:8000{path} 2> /dev/null | sed \'s/ *$//\' >> "{output}"')
        system(f'echo >> "{output}"')
        print('.', end='', flush=True)

    system(f'echo > "{output}"')
    for path in get_all_paths():
        curl(path)

    print()

    system(f'git diff --no-index -- "{reference}" "{output}"')


@task
def test_accept():
    'Accept test results.'

    reference = TESTS_DIR / 'reference.txt'
    output = TESTS_DIR / 'output.txt'
    system(f'rm "{reference}" || true; mv "{output}" "{reference}"')


@task
def visit():
    'Visit https://narf.pl/.'

    system('open https://narf.pl/')


if __name__ == '__main__':
    TASKS[argv[1]]()
