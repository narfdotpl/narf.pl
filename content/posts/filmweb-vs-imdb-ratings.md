2013-12-03

Filmweb vs IMDb: ratings
========================

Recently at a party I was listening to a conversation, when someone said
something along the lines of "it went really well, especially given that
Poland is the country of haters".  "Really?", I interrupted, "Doesn't
every country think that of itself?".  "No, just look at [Filmweb][]:
ratings are about half of a point lower than on [IMDb][]".  So I looked:

![density](density.png)

  [Filmweb]: http://en.wikipedia.org/wiki/Filmweb
  [IMDb]: http://en.wikipedia.org/wiki/Internet_Movie_Database

Indeed, Filmweb ratings are generally lower (57% lower, 9% equal, 33%
higher).  The difference of "about -0.5" seems to be true for the best
IMDb movies, but looks to be closer to -0.2 for movies rated between 7
and 8 on IMDb.  Maybe this is the country of... hmm... moderate haters?

How did I get this data?  Neither Filmweb nor IMDb provide an API, so I
wrote a script that read a list of movies from [Filmweb Top 500][top500]
ranking, searched for each movie on IMDb (by title and release date),
and took first result's rating.  The script matched 456 of 500 movies
(many Polish ones are not on IMDb).  Ratings provided by Filmweb were
rounded to three decimal places; IMDb to only one.  During analysis
I rounded Filmweb ratings to one decimal place, so that values being
compared would have the same precision.

  [top500]: http://www.filmweb.pl/rankings/film/world

[Data and code][] are on GitHub.

  [data and code]: https://github.com/narfdotpl/narf.pl/tree/master/content/assets/filmweb-vs-imdb-ratings
