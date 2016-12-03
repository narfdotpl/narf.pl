2015-07-28

Checkers: Explosion bug
=======================

<blockquote class="instagram-media" data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div><p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://instagram.com/p/5qzsJHF8Rl/" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none;" target="_top">A video posted by Maciej Konieczny (@narfdotpl)</a> on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-07-28T05:56:16+00:00">Jul 27, 2015 at 10:56pm PDT</time></p></div></blockquote>
<script async defer src="//platform.instagram.com/en_US/embeds.js"></script>

<br/>

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
