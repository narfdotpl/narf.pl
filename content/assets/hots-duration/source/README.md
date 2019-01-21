## Requirements

- Have a flat directory with HotS replays.
- Use [`pyenv`](https://github.com/pyenv/pyenv).


## Getting data

    pyenv install 2.7.15
    pyenv local 2.7.15
    ln -s ??? replays
    git clone https://github.com/Blizzard/heroprotocol
    python get_data.py > data.csv


## Making graphs

    pyenv install 3.7.2
    pyenv local 3.7.2
    python make_graphs.py


## `mypy` linting in VS Code

Use [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).

    pyenv local 3.7.2
    pyenv virtualenv hots-duration
    pyenv activate hots-duration
    pip install -r requirements.txt
