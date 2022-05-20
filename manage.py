#!/usr/bin/env python
# encoding: utf-8

from os import walk, system
from os.path import dirname, join, realpath
from sys import argv, stdout


CURRENT_DIR = dirname(realpath(__file__))
REPO_DIR = CURRENT_DIR
CONTENT_DIR = join(REPO_DIR, 'content')
ENGINE_DIR = join(REPO_DIR, 'engine')
LOGS_DIR = join(REPO_DIR, 'logs')
TESTS_DIR = join(REPO_DIR, 'tests')
POSTS_DIR = join(CONTENT_DIR, 'posts')

TASKS = {}


def task(func):
    TASKS[func.__name__] = func
    return func


def get_post_paths():
    for root, dirnames, filenames in walk(POSTS_DIR):
        for filename in sorted(filenames):
            if filename.startswith('.'): continue
            if not filename.endswith('.md'): continue

            yield '/posts/%s' % filename[:-len('.md')]


@task
def deploy():
    'Update production with latest changes.'

    test()
    logs_fetch()
    system('git push --force-with-lease dokku HEAD:master')
    visit()
    system("ssh dokku -t 'rm -rf /tmp/dokku_git.*'")
    populate_cache()


@task
def runserver():
    'Run development sever.'

    system('f() { sleep 0.2; open http://localhost:8000; }; f &')
    system('cd "%s"; python main.py' % ENGINE_DIR)


@task
def js():
    'Generate main JavaScript file.'

    system('cd "%s"; ./generate-main-js' % join(CONTENT_DIR, 'javascript'))


@task
def logs_fetch():
    # logs start at the last deployment
    system("ssh dokku -t 'docker logs $(cat /home/dokku/narf.pl/CONTAINER.web.1)' | gzip > \"{dir}/$(date +%Y-%m-%d_%H%M).txt.gz\"".format(dir=LOGS_DIR))


@task
def logs_show():
    system("cd \"%s\"; gunzip -c $(ls *.txt.gz) | ag -v 'GET /static' | goaccess -o html > index.html && open index.html" % LOGS_DIR)


@task
def populate_cache():
    'Populate cache in production.'

    for path in get_post_paths():
        system('curl http://narf.pl%s > /dev/null' % path)


@task
def publish():
    'Publish to GitHub and deploy to production.'

    deploy()
    system('git push public')


@task
def test():
    'Test differences in rendering.'

    reference = join(TESTS_DIR, 'reference.txt')
    output = join(TESTS_DIR, 'output.txt')

    def curl(path):
        system('curl http://localhost:8000%s 2> /dev/null | sed \'s/ *$//\' >> "%s"' \
              % (path, output))
        system(f'echo >> "{output}"')
        stdout.write('.')
        stdout.flush()

    system('echo > ' + output)
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

    system('git diff --no-index -- "%s" "%s"' % (reference, output))


@task
def test_accept():
    'Accept test results.'

    system('rm "{reference}" || true; mv "{output}" "{reference}"'.format(**{
        'reference': join(TESTS_DIR, 'reference.txt'),
        'output': join(TESTS_DIR, 'output.txt'),
    }))

@task
def visit():
    'Visit http://narf.pl/.'

    system('open http://narf.pl/')


if __name__ == '__main__':
    TASKS[argv[1]]()
