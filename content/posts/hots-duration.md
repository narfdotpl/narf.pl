date: 2019-02-12
collections: [visualization]

HotS: impact of XP changes on match duration
============================================

In 2018 I've been playing a lot of [Heroes of the Storm][hots] with
friends.  HotS is a fast-paced MOBA with a focus on map-specific
objectives and 5v5 team fights.

  [hots]: https://heroesofthestorm.com/


December was an emotional month for all of us in the Nexus:

- first, there were Quick Match team composition changes (which I won't get
  into the details of)
- then, among a lot of controversy and heated Reddit discussions, Blizzard
  made [a huge change to how experience is gained][xp] during a match
- and finally, two weeks before Christmas, they [cancelled the official
  e-sport league and moved some developers to other projects][hgc]

It was quite a ride and for a moment we didn't know if we still had our
game.  Despite the obvious negative reaction to the last piece of news,
the game is very much alive and I play it regularly.  In this post I
wanted to reflect on how it felt to play HotS in December and January:
specifically to think about how the XP changes affected my experience
(wink).

  [xp]: https://heroesofthestorm.com/en-us/blog/22821338/heroes-of-the-storm-patch-notes-december-11-2018-2018-12-11/
  [hgc]: https://news.blizzard.com/en-us/blizzard/22833558/heroes-of-the-storm-news

The crux of the XP changes is that now destroying enemy buildings grants
a small bonus to experience gained over time -- instead of giving a big
amount of XP immediately.  With this modification Blizzard wanted to
make matches closer and reduce the snowball effect that the team in the
lead is always trying to take advantage of.  This wasn't a problem in my
opinion, but of course the game creators have more insight into the game
and can make decisions informed by a lot of data.

From my perspective (I'm an average player, Gold in Europe) matches
after the XP patch got less dynamic. It's harder to push in the
mid-game, easier to defend, there are fewer dramatic power swings
between the two teams...  This might be in line with the stated goal of
the patch.  However, sometimes it feels like both sides are just waiting
for the level 20, so that the final team fight can decide which team
wins the game, regardless of what was going on on the map for the past
twenty-plus minutes...  Which brings me to the main focus of this post:
the match duration.

I *feel* that matches after the experience changes are longer.  Of
course, being the person that I am, a feeling for me is *a)* not enough,
and *b)* something I want to verify against data. Therefore, I analyzed my
replays and graphed their durations. (BTW take a look at technical
notes at the end of this post if you think, as I did, that getting the
duration of a match out of a HotS replay is easy.)  I looked at my games
in Team League and Quick Match from November, December, and January.  (I
don't do Hero League because I play almost exclusively with friends.)
Here are normalized histograms of my results:

<img data='{"max_height": 1792}' class="max-height-initial" src="graphs.png"/>

Well. I didn't expect to see *this*.  Quick Match is similar between
patches.  The median Team League game is actually 1.5 minute *shorter*.
What the hell?  Does it mean that my perception doesn't match the
reality?  (Wouldn't be the first time...)

I assume what's occurring here is that my intuition is skewed because
the games I remember the most are the ones that were the longest and
that the new smooth-out-the-differences XP system allows (at least in
the lower ranks).  In TL in particular we had a couple of matches in the
30–38 minutes range. This didn't happen in the previous season.

![](perception.png)

Or it might be that the sample size is too small, that my friends and I
are different (better? 🤞) players now, etc., etc.

"And on that bombshell..."


Technical notes
---------------

- HotS automatically saves replays of all games.
- I used Blizzard's [heroprotocol.py][protocol] tool to transform replays
  into JSON dictionaries.
- It quickly turned out that Blizzard's data layout is far from intuitive
  and lacks documentation.  Thankfully, I found Evan Shimizu's [parser][],
  on which I based my Python implementation.
- I made the charts with Python, SVG, and Pixelmator.  I like tinkering
  with such things.

  [protocol]: https://github.com/Blizzard/heroprotocol
  [parser]: https://github.com/ebshimizu/hots-parser

What surprised me about this project is how absurdly difficult it is to
get the match duration from a HotS replay.  I expected it to be a value
in a dictionary.  But no.  To get the duration in seconds you have to:

1. Sequentially read through all of the game events.
1. Wait for the "unit born" events for cores. (BTW cores on Alterac Pass have
   different names than on all other maps.  You have to handle this.)
1. Remember core IDs (that consist of two separate keys).
1. Wait for the "gates open" event.
1. Remember the index of its game loop.
1. Wait for the "unit died" event with the object ID of one of the cores.
1. Read its game loop index and subtract the index of the "gates open" event.
1. Divide the result by 16 (apparently HotS logic runs at 16 FPS).
1. [owl-yiss.gif](https://www.google.com/search?q=owl+yiss+gif&tbm=isch)

---

*Thanks to jhgrng, plasticbag, and sabr for reading drafts of this.*
