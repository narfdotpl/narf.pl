#!/usr/bin/env python
# encoding: utf-8

from os import walk, system
from pathlib import Path
from sys import argv, stdout


CURRENT_DIR = Path(__file__).absolute().parent
REPO_DIR = CURRENT_DIR
CONTENT_DIR = REPO_DIR / 'content'
LOGS_DIR = REPO_DIR / 'logs'
TESTS_DIR = REPO_DIR / 'tests'
POSTS_DIR = CONTENT_DIR / 'posts'

TASKS = {}


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


@task
def deploy():
    'Update production with latest changes.'

    test()
    logs_fetch()
    system('git push --force-with-lease dokku HEAD:master')
    visit()
    populate_cache()


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
    # logs start at the last deployment
    system(f"ssh dokku -t 'docker logs $(cat /home/dokku/narf.pl/CONTAINER.web.1)' | gzip > \"{LOGS_DIR}/$(date +%Y-%m-%d_%H%M).txt.gz\"")


@task
def logs_show():
    system(f"cd \"{LOGS_DIR}\"; gunzip -c $(ls *.txt.gz) | ag -v 'GET /static' | goaccess -o html > index.html && open index.html")


@task
def populate_cache():
    'Populate cache in production.'

    for path in get_post_paths():
        system(f'curl http://narf.pl{path} > /dev/null')


@task
def publish():
    'Publish to GitHub and deploy to production.'

    deploy()
    system('git push public')


@task
def test():
    'Test differences in rendering.'

    reference = TESTS_DIR / 'reference.txt'
    output = TESTS_DIR / 'output.txt'

    def curl(path):
        system(f'curl http://localhost:8000{path} 2> /dev/null | sed \'s/ *$//\' >> "{output}"')
        system(f'echo >> "{output}"')
        stdout.write('.')
        stdout.flush()

    system(f'echo > "{output}"')
    curl('/')
    curl('/404')
    curl('/feed')
    curl('/feed.json')
    curl('/music')
    curl('/posts')

    for path in get_post_paths():
        curl(path)

    stdout.write('\n')
    stdout.flush()

    system(f'git diff --no-index -- "{reference}" "{output}"')


@task
def test_accept():
    'Accept test results.'

    reference = TESTS_DIR / 'reference.txt'
    output = TESTS_DIR / 'output.txt'
    system(f'rm "{reference}" || true; mv "{output}" "{reference}"')

@task
def visit():
    'Visit http://narf.pl/.'

    system('open http://narf.pl/')


if __name__ == '__main__':
    TASKS[argv[1]]()
