date: 2020-12-21
collections: [procedural]
theme: black
index:
  subtitle: animation

Solstice
========

![](solstice.mp4)

Happy solstice, everyone!

It's the end of week three of [arsiliath][]'s [compute shader
workshop][workshop]. This time we were introduced to stigmergic agents
-- actors that coordinate indirectly, through environment.

  [workshop]: https://paprika.studio/workshops/compute/index.html
  [arsiliath]: https://twitter.com/arsiliath

In my piece, which was meant to resemble a star, I have four million
agents leaving and following a trail, sort of like ants. It still blows
my mind that this runs smoothly in real time and can be altered live. I
based my implementation on [Sage Jenson's post][Sage Jenson], that was
in turn based on [Jeff Jones][]' paper.

  [Sage Jenson]: https://sagejenson.com/physarum
  [Jeff Jones]: https://www.lstmed.ac.uk/about/people/dr-jeff-jones

To create a circle I applied a vignette to the decay factor of the
"chemicals", so that the trail disappears faster near the edge.
The more sudden changes you see are results of me altering sensor
parameters -- the range and "field of view" of each agent.

I cut the footage into three parts and connected them with two fade
transitions to make the video more dynamic and create a seamless
loop. Otherwise the animation is straight from Unity with #nofilter. ;)

As it's often the case, I think I like individual details more than the
whole thing:

<figure class="full-width" style="margin-bottom: 1px">
    <img data='{"max_width": 3043, "max_height": 1350}' src="9x16.jpg"/>
</figure>
