2015-07-28

Checkers: Explosion bug
=======================

TODO: embed Instagram

<br>

I had a funny bug.  My brother noticed that explosions of the light
pieces were "weaker" than explosions of the dark pieces.  [One early
morning before the day job][everyday], I decided to look into it.

  [everyday]: http://ejohn.org/blog/write-code-every-day/

Fixing the problem was easy.  Tracking it down, on the other hand, took
about two hours, during which I looked in all the wrong places and had
no luck with the usual "print a lot of stuff and then step into the
debugger" approach.  I won't go into details here, but [tweaking][] the
live system was instrumental in diagnosing the exhibited behavior.

  [tweaking]: /posts/checkers-development-panel

Explosions are implemented like this: first I recursively divide a
piece into small fragments, then I apply an impulse of momentum to each
fragment -- from the center of the piece outwards.  The cause of the
bug was the fact that I applied momentum vectors in the "physics world"
coordinate system, but computed them using positions of fragments in
the coordinate system *of each piece*.  You see, the dark pieces use
the "normal" coordinates and the light pieces are rotated by 180°, so
that the dark triangles and pentagons point downwards and the light ones
point upwards.

Rotating by 180° around the (0,&nbsp;0) point is equivalent to
multiplying both *x* and *y* coordinates by -1.  The moment when I
realized this was the moment when I understood what was happening on
the screen:

After breaking into fragments, the light pieces would be pushed *in the
wrong direction*, inwards instead of outwards.  They would immediately
collide with each other, loose some kinetic energy due to not perfect
elasticity, and bounce outwards, with a smaller velocity.  All of this
whithin a single frame of animation.

A *funny* bug. :)

It's especially visible when I don't randomize impulse magnitudes, as
in the video at the top of this post.  Notice how the "implode and
bounce away from each other" behavior affects not only the velocity
of fragments but also the overall shape of the debris "cloud": normal
explosions create "rings" while the buggy ones are amorphic.

---

*To get new posts subscribe to the [RSS feed](/feed),
or the [Checkers newsletter](/newsletter),
or follow me on [Twitter](https://twitter.com/narfdotpl).*
