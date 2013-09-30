2013-07-06

How to play CPMA on OS X
========================

[This][Vo0] is CPMA and *this* is a rough guide on how to run it on OS X.
The target audience are people who play CPMA on other platforms or, like
me, stopped playing many years ago, knew the game and its ecosystem well,
and would like to revive memories of the good old days.

If you're not a ProMode veteran, I suggest you look at other great
Quake-derived shooters (but with a lower barrier of entry), like [Urban
Terror][] or [Warsow][].  I recommend UrT especially if you want to play
with the noobs from your office... ;)

To play "robots and lasers", read on.

  [Vo0]: http://www.youtube.com/watch?v=YiX9d_j1Xao
  [Urban Terror]: http://www.urbanterror.info/home/
  [Warsow]: http://www.warsow.net/


Fix your mouse
--------------

The step zero is to fix your mouse by removing acceleration introduced by
the OS.  I achieved this with [SteerMouse][], which was recommended in
[this article][mice setup].

  [SteerMouse]: http://www.plentycom.jp/en/steermouse/download.php
  [mice setup]: http://www.technobuffalo.com/2011/02/02/how-to-setup-gaming-mice-for-mac-os/


Download everything
-------------------

To play Quake, you need the Quake itself, which boils down to getting
the `pak0.pk3` from your original game CD or The Pirate Bay.

Once you have the core, you will have to download a client. I use
[ioquake3][], which works on modern hardware and supports wide screens.

Finally, you have to download CPMA.  Wonderful people of
[playmorepromode.org][pmm] provide a [ZIP archive][zip] with maps and
the mod itself.

  [ioquake3]: http://ioquake3.org/
  [pmm]: http://playmorepromode.org/
  [zip]: http://playmorepromode.org/CPMA148.zip


Take advantage of the whole screen
----------------------------------

You can make the game run in resolutions that people didn't dream of
in 1999 by issuing following commands:

    r_mode -1
    r_customwidth 1920
    r_customheight 1080
    vid_restart

Unfortunately, custom resolutions and aspect ratios work "only" for 3D
elements.  Everything that's 2D seems to be drawn using the 4:3 ratio
and stretched.  You can fix this for HUD elements by writing custom HUD
configs (see `cpma/docs/HUD.txt`).


Adjust FOV
----------

If you switch to a wider screen, you should switch to a wider FOV too.
I used simple trigonometry to compute how big my new 16:9 FOV *β* should
be, if I used to play with FOV *α* on a 4:3 screen:

![FOV formula](fov-formula.png)

Resulting formula is hard to do in the head, but Google can help with
the [computation][] (replace "110" with your 4:3 FOV and "16/9" with
"16/10" if you use a 16:10 screen).

  [computation]: http://google.com/search?q=atan(%2016%2F9%20*tan(%20110%20%2F2%2F180*pi)%2F(4%2F3))*180%2Fpi*2
