date: 2019-06-18
collections: [procedural]
theme: black

Metal trees
===========

For quite some time I've been revisiting the idea of procedurally
creating images of stylized trees.  I went through a number of
approaches, techniques, and aesthetics.  At one point I was working
on a custom SVG renderer with a 3D projection.  Different display
issues in different browsers forced me to abandon this route and go
full 3D.  Turns out, this was just what I needed.  This is my first
generative project in 3D and I'm very pleased with the results. (I even
[3D-printed](https://www.instagram.com/p/BwrbYAnlCcz/) one of the trees
and I keep it on my desk.)

In this post I include a selection of images I created when working
on this project: different algorithms, different seeds, different
techniques.

My favourite are the ones with mirrored and repeated branches.  They
exemplify qualities that I like the most in generative art: patterns
emerging from a large number of simple elements, organic shapes
contrasted against unnatural precision.

{% for i in range(1, 8) %}
<figure class="full-width">
    <img data='{"max_width": 3240, "max_height": 1920}' src="triptychs/{{ i }}.png"/>
</figure>

{% if i == 5 %}
<figure class="full-width">
    <img data='{"max_width": 3240, "max_height": 2778}' src="big.png"/>
</figure>
{% endif %}

{% if i in [1, 2, 7] %}
<br/>
<br/>
{% endif %}
{% endfor %}


Technical notes
---------------

- I wrote everything in Python. I save binary PLY files with edges
  (no faces) and load them in Blender.
- Blender can be scripted. I run it from the command line and make it
  execute a Python script that loads the PLY, adds volume to edges, sets
  materials, etc.
- Everything is automated. I make a change to the code, press ⌘S,
  and new images start appearing in the web browser next to the editor.
- The generation process is divided into two main phases.  First, I create
  a "low poly" geometry with the overall shape.  Then, I create individual
  "high poly" spaghetti strings, twist them around, bring them closer
  together near the tips, etc.
- To speed up iteration, I wrote a simple Redis-based queue to use
  multiple computers.  Each machine creates geometry and renders an
  individual image.  This approach works great for creating many renders
  at once, but it doesn't help when I want to make a single high resolution
  image.
