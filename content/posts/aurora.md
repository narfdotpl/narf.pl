date: 2022-08-23
collections: [procedural, music]
theme: black
index:
  subtitle: computer hallucination
music:
  section: soundtracks

Aurora
======

{{ youtube_iframe('mCrPPmJoARk') }}

<br/>
*Aurora* is a computer hallucination created with custom software.
An attempt at hypnosis with color, movement, and wave interference.
Controlled by code and changing through time, these elements combined
create complex patterns and fascinating transient shapes that fluidly
form for brief serendipitous moments and smoothly dissolve into
their next silhouette after a few short seconds.


Technical notes
---------------

*Aurora* is built on three pillars: 2D, 3D, and sound.

The 2D part is the simulation you see on the virtual screen. It is a
compute shader running on the GPU in realtime-interactive-4k-60fps in
a custom Metal + Swift environment that I've built in order to create
animations like this one. (*Aurora* is literally the "hello world"
sketch for this environment.  I just didn't stop at the "hello" -- it
pulled me in and I kept adding to it. An accidental first project.)  I
can change the code live while the simulation is running, rewind time,
adjust various parameters using knobs and pads of a MIDI controller,
etc.  It's great.  I'm very happy I invested time in building a custom
solution for this and future simulations.

The sound is realtime as well: MIDI sent to Ableton. Finally, all
of this is wrapped in a definitely-not-realtime 3D scene that is
path-traced in Blender at about 0.08 FPS.

I'm looking forward to building more with these tools. Subscribe to my
[RSS feed](/feed) to be notified about my next projects.


Elsewhere on the web
--------------------

Discuss this project on TODO (updating soon).


Stills
------

![](5k/01337.jpg)
![](5k/08792.jpg)
![](5k/13110.jpg)
![](5k/13370.jpg)
