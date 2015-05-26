2015-01-25

Checkers: Update 1
==================

Let's open with half a minute of unedited gameplay footage.

<figure>
    <div class="video-wrapper">
        <iframe src="//www.youtube.com/embed/-WltJzujyk8" frameborder="0" allowfullscreen></iframe>
    </div>
</figure>

I'm happy with how things look and work at this stage, although I'm sure
I'll spend a lot of time polishing everything.  In particular, I expect
to make many small changes when working on sound.  What you hear at the
beginning are just placeholders, but they give a good taste of the direction
I want to go in.

On a less happy note, the Christmas break is over and I don't have much
time to work on checkers.  Here's a graph from GitHub, showing the
number of changes in the project (per week?):

![](commits.png)

Since the [previous post](/posts/checkers-teaser), I've improved
responsiveness, tweaked animations, and made touch sizes and "drag
targets" bigger.  I have also made debris stay much longer on the board.

On the side invisible to the player, I have started working on a
development panel for switching between board states and tweaking
animations while the game is running.  I will write more about this
in the next update.  As of today, I have implemented game state
(de)serialization using [SwiftyJSON][] and [`unwrapped`][unwrapped], a
little helper I've created for dealing with multiple optionals.

  [SwiftyJSON]: https://github.com/SwiftyJSON/SwiftyJSON
  [unwrapped]: https://github.com/narfdotpl/doodles/blob/master/doodles/unwrapped.swift

That's all for today.  Sign up for a [newsletter][] to get more updates
about the project and email me at <checkers@narf.pl> if you want early
access to the game.

  [newsletter]: http://eepurl.com/baKQjf
