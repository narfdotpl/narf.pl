date: 2020-01-25
collections: [procedural]
theme: black

Drzwi
=====

![](drzwi-sound.mp4)

*Drzwi* is an animation based on a dream I had recently.

I'm not a fan of descriptions that tell you what you should see or feel,
but I can tell you that in the dream I opened a door in a dimly lit
narrow apartment and walked down an underground corridor that slowly
became more abstract as I noticed I'm no longer walking but falling.

I created this animation procedurally in Python and Blender. A few
months after making the video I created audio, also procedurally,
in Python and VCV Rack. I wrote about it in a [separate
post](/posts/drzwi-vcv).

To make this project I had to extend my tools with ability to move
the camera and change material properties in Blender. Turns out, it's
hard to get camera movement and timing right. I suspect it's difficult
in the real world as well, but I felt it very strongly when working on
it in code: tweaking timing, curves, and noise of different movements
by tenths of a second makes the difference between a shot that feels
movie-like and something that looks completely artificial. In the end I
decided to remove all instances of looking around, partly because they
were difficult to get exactly right, but also because they didn't work
well in the loop format: camera movement was interesting on the first
watch, but distracting on the next one.

A more technical aspect I had to deal with was rendering time. First of
all I removed from the scene all objects that ware too far away from the
camera, but the most significant improvement came when I made the number
of samples dependent on the velocity of the camera: the faster it falls,
the noisier the frame. It gives higher quality frames when you have time
to watch the light on the wall and the floor, while also making the
middle section of the animation substantially faster to render because
you're less likely to notice any noise or grain on objects that you're
quickly flying past.

The final thing that I want to mention that's a bit unusual about my
code is that it's stateless: each frame is generated independently and
could be rendered in any order. (In practice I render them sequentially
to be able to preview the animation before all frames are done, but
I can start at any point.) This is possible because all movement is
described by formulas instead of being simulated numerically.

I don't track time but the whole project took a few weekends from start
to finish. And about a week (*sic!*) to render in the final quality in
1080p60. (Aren't you a fan of fan noise?)

To wrap this post up, here's me working on the thing:

![](wip2.gif)

And here are a few frames rendered in 5k that I posted [on Instagram](https://www.instagram.com/p/B721h4BnOKc/):

![](frames/0339.jpg)
![](frames/0500.jpg)
![](frames/1319.jpg)
