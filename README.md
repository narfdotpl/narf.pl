# [narf.pl](http://narf.pl)

## Running locally

- Install [`pyenv`](https://github.com/pyenv/pyenv).
- Install [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).

```
pyenv virtualenv narf.pl
pyenv activate narf.pl

brew install zlib
export LDFLAGS="-L/opt/homebrew/opt/zlib/lib"
export CPPFLAGS="-I/opt/homebrew/opt/zlib/include"

pip install -r requirements.txt

./manage.py runserver
```
