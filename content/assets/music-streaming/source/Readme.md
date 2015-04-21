This app uses the Last.fm API to retrieve data on last.fm listening activity. You'll need to have used last.fm for a while for it to be worthwhile. It downloads weekly track charts and saves them as JSON files, then converts them to CSV. A d3.js-based web page (in the `charts/` subfolder) renders this data as charts.

## How to use

* [Download a copy of this repository](https://github.com/narfdotpl/narf.pl/archive/master.zip)
* `cd narf.pl/content/assets/music-streaming/source/`
* `rm data/api-json/*.json && m data/chart-csv/*.csv` to clear narf's data
* `sudo pip install -r data/requirements.txt`
* Register a new application at [last.fm/api/accounts](http://www.last.fm/api/accounts).
* Add your API key and username to `data/settings.py`
* `python data/download_json.py && python data/generate_csv.py` to download data (this could take a while, but you can cancel (`Ctrl+C`) mid-download and resume later)
* `python -m SimpleHTTPServer` to run a local server
* Open [http://localhost:8000/charts/](http://localhost:8000/charts/) to see your lovely charts

### To move the "Spotify" green line

* Change date on line 180 of `charts/lib.coffee`
* `sudo npm install -g coffee-script` to install Coffeescript
* `coffee -c charts/lib.coffee` to compile JavaScript from Coffeescript
