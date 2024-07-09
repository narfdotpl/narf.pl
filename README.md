# [narf.pl](https://narf.pl)

## Running locally

- Install [`pyenv`](https://github.com/pyenv/pyenv).
- Install [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).

```
brew install zlib
export LDFLAGS="-L/opt/homebrew/opt/zlib/lib"
export CPPFLAGS="-I/opt/homebrew/opt/zlib/include"

pyenv install $(cat .python-version)
pyenv virtualenv narf.pl
pyenv activate narf.pl

pip install -r requirements.txt

./manage.py runserver
```


## Running on [Render](https://render.com)

#### build command

    pip install -r requirements.txt

#### start command

    gunicorn engine.main:app --workers=2

#### Python version

specified using `PYTHON_VERSION` environment variable
