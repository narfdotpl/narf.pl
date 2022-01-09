date: 2017-04-04
collections: [procedural]
is_selected: true
index:
  subtitle: graphics and animations
  sorting_key: 2017-06-12

Procedural graphics: trees and circuit boards
=============================================

A year ago I started playing with procedural graphics -- a way of
creating images where you write a program that does the drawing for
you.  Initially I wanted to make images that would look like insides of
a computer.  I ended up creating animations of circuit-board-like
trees.

In this post I share my thoughts about creating images indirectly,
present my results, and outline the technique I came up with.


![](keyboard.jpg)

*One of the big trees on the left, early&nbsp;notes on the right.*


Procedural graphics
-------------------

First: what is "procedural graphics"?  It's a way of creating images
where you don't draw manually.  Instead you come up with a procedure, a
list of instructions for how to create an image.  Then you ask someone
to follow the procedure.  Usually that "someone" is a computer.

You can imagine procedural graphics as a board game: you come up with
the rules, you design the board, you set up the pieces.  After you're
done, someone plays it.  The act of playing the game, or executing the
procedure, is when you get to see what you've really created.  It might
seem surprising, but often you don't know exactly what you will get
until you see it.  It's a matter of complexity: you design the rules
with a specific goal in mind, imagining how the board will look like
after a couple of moves, but you can't imagine it after ten thousand
moves.  You have to see the game play out dozens of times to get a sense
for what you've created.  (This is not true if there's no randomness
in the procedure — if you don't roll any dice you always get the same
end result for the same initial conditions.)

For me, watching a procedure in action is a fascinating experience.
It's captivating to watch how complex patterns arise from simple rules.

I've been admiring procedural works for years and I've finally decided
to try to create some myself.  I first used procedural graphics in my
iOS game [Glitchy Checkers][], where I created all the images in code.
I'm particularly happy with the procedure for breaking pieces into
fragments:

[![](glitchy-checkers.png)][Glitchy Checkers]

*Screenshots from [Glitchy Checkers][].  Procedurally broken pieces on
the left, glitchy shader on the right.*

  [Glitchy Checkers]: /checkers


Before settling on the "screen malfunction glitch" I considered many
different approaches for how to distinguish kings from regular pieces.
One solution I was thinking about involved a circuit board pattern.
I looked at a number of motherboard photos and I wondered if I could
create such patterns procedurally.  A couple of weeks after releasing
version 1.0 of the game I decided to explore this subject.

Without further ado, let me show you what I've made.


Big tree
--------

I ended up creating a few kinds of images.  The ones I like the most are
"big trees".  I call them that because they have a thick trunk, more
than one main branch, and some roots sticking from the ground.  Here's
an animation of one "growing":

![](big-trees/growth.mp4)

Aside: I didn't plan to make animations, I just wanted the final image.
<strike>Un</strike>Fortunately, I made a programming error that caused
many images to look bad.  I couldn't deduce what the source of the issue
was, so I added the ability to save the image after each procedure step
in order to track the issue down visually. Turns Out™, stitching these
images together makes for cool videos. ;) The lesson learned is that
it's helpful to be able to see the iterative process in action.


How it works
------------

How is this big tree created? It consists of a bunch of paths.  In order
to achieve the printed circuit board look, paths are straight lines with
45° turns and circles at the end. They have different lengths and they
never cross. Some of them end and spawn other, shorter paths. They are
all independent in a sense that they don't coordinate, but their growth
is limited by the available space: they live on a grid and they can't
take a place that is already taken. They avoid collisions but can look
only two steps ahead and take only 45° turns. I programmed them to
keep moving in a given direction with a small chance of making a random
turn on each step.

![](avoidance.gif)

*Navigation example.  The path grows on a grid and keeps the direction.
It avoids obstacles (blue squares) by looking two moves ahead.  It can
make only 45° turns.  The path ends after reaching its final length or
when there are no possible moves, for example when reaching a dead end.*

When there's more than one path, each of them takes one step and waits
for the next turn. The order of paths is chosen randomly each turn.

![](growth.gif)

*Growth example.  The path ends and creates three new, shorter paths
using the “if you grow ↑, split into ↖↑↗” branching rule. Each path
makes one step and waits for the next turn.  The order of paths is
chosen randomly each turn.*


More big trees
--------------

The big tree you've seen above is one of many. I created it by manually
placing trunk paths and a few "branch seeds" inside the trunk. This is
what it looked like before the start of the procedure:

![](big-trees/initial-conditions.png)

From this exact initial conditions I got many different results because
I randomize path length, growth order, number of new paths spawned from
the tip, etc. I love that the range of results is wide even though they
all use the same settings. Some trees even look like they were chopped
down or broken by wind:

<img data='{"max_height": 3108}' class="max-height-initial" src="big-trees/mosaic.png"/>


Different branching rules
-------------------------

All of the examples so far used the same branching rule: "if you grow
↑, split into ↖↑↗". The absolutely great thing about this generator is
the fact that using different branching rules leads to fantastically
different results, different kinds of plants!

![](triptych.mp4)

*A single stem creating different trees because of different
branching rules.  From left to right: a leafy tree&nbsp;(↖↑↗),
a conifer&nbsp;(↙↑↘), and a bush&nbsp;(←↑→).  Speed adjusted
for each video to take ten seconds.*

![](bush.mp4)

*A bush created using the "split into&nbsp;X" branching rule.*

Playing with the system at this stage was very satisfying. It
highlighted the strength of procedural generation: it's often faster
to create a thing by hand rather than making a program, but once you
write the code, you can produce many more things much faster, either by
tweaking the procedure or by using randomness.  Animations in particular
would be very time-consuming to create manually.

The procedural approach allows to explore new kinds of imagery,
including simulations of natural or imaginary phenomena or kinds that
otherwise create appealing results from thousands of applications of
strict rules -- something that would be too hard for a human to keep
track of.  It also blurs the line between creation, invention, and
discovery.


Failures
--------

Because my procedures use randomness and because I didn't implement
any form of automatic validation of the final results, sometimes I get
images that are far from what I wanted to create.  Here are some of my
favourite failed trees:

![](failures.png)


Technical notes
---------------


- I wrote the whole thing from scratch in Swift as a command line Mac
  application.  (I didn't use the command line to run it, I just
  pressed ⌘R in Xcode.)
- If I were to start this project today, I would use [p5.js][] because it
  would be faster to get something on the screen and start iterating.
- In the beginning I spent many hours not knowing how to tackle path growth.
  I split the code into models and renderers. I created an ASCII renderer
  and started writing navigation unit tests using ASCII diagrams (I also
  used this technique in [Glitchy Checkers][] in tests for rules). It made
  fixing bugs easier later on.
- I have entities with names like `PathGrowthStrategy` and
  `AvoidingNavigator`. :partyparrot:
- I used `NSOperationQueue` to run many simulations or many renders in
  parallel. Immutable models made parallelism easy.
- I rendered PNGs and either converted them to a movie using `ffmpeg` or
  displayed dozens of images (the same procedure with different random seeds)
  on a simple web page.
- I used [`peat`][peat] to show results after the procedure was done.
  As the final step of the program I modified a `peat-trigger` file that
  I watched with `peat`. It made the work quicker because the workflow was:
  tweak the procedure, press ⌘R, see a dozen of images, press ⌘⇥ to go back
  to Xcode, repeat.
- I used random number generators from GameplayKit.

  [p5.js]: https://p5js.org/
  [peat]: https://github.com/sjl/peat


Questions
---------

That's all folks!  If you have any questions, don't hesitate to ask me
on Twitter, via email, or in person.  You can also discuss this post
[on the procedural generation subreddit][Reddit].  Cheers.

  [Reddit]: https://www.reddit.com/r/proceduralgeneration/comments/63e66h/procedural_graphics_trees_and_circuit_boards/

*Thanks to Tomek Falkiewicz for reading drafts of this.*
