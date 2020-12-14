date: 2016-09-22
collection: Procedural series

Summer of Creative Coding
=========================

Well, I don't mean *the entire* summer, but I did some "creative coding"
in the last months and today was the first day of autumn, so I couldn't
resist to use this title.

"Creative coding" is a funny term that implies that "normal coding" is
not creative.  From [Wikipedia][]:

> Creative coding is a type of computer programming in which the goal is
> to create something expressive instead of something functional.

I made some images. I gathered them in this post with some rough
descriptions.

  [Wikipedia]: https://en.wikipedia.org/wiki/Creative_coding


Start
-----

First I stumbled upon an *absolutely amazing* YouTube channel called
[Coding Rainbow][] where Daniel Shiffman teaches various things related
to creating artistic programs. He implements most of his examples in
[p5.js][] and Processing.

My first p5.js sketch created after watching Daniel's video was this tree:

![](p5-tree.jpg)

*Some images here are photos of the screen.<br/>
Because I think they look cool. 😎*

  [p5.js]: http://p5js.org/
  [Coding Rainbow]: http://codingrainbow.com/



Fermat's spiral
---------------

Next, I created a looped animation of a [Fermat's spiral][]:

![](fermats-spiral.gif)

Saving GIFs from p5 turned out to be hard. To get the that perfect
loop, I ended up pausing the animation after each frame, posting the
canvas data to a [Python server][], saving image data in a PNG file, and
combining PNGs into a GIF using [ImageMagick][].

  [Fermat's spiral]: https://en.wikipedia.org/wiki/Fermat%27s_spiral
  [Python server]: https://github.com/narfdotpl/narf.pl/blob/master/content/assets/summer-of-creative-coding/gif-export/server.py
  [ImageMagick]: https://github.com/narfdotpl/narf.pl/blob/master/content/assets/summer-of-creative-coding/gif-export/make-gif


Superformula
------------

After watching a Coding Rainbow video about [2D supershapes][supershapes],
I&nbsp;made this loop:

![](superformula.gif)

  [supershapes]: https://youtu.be/ksRoh-10lak


HSB (hue, saturation, brightness)
---------------------------------

After watching [p01's talk][p01], I started experimenting with additive
blending of particle trails.

  [p01]: http://www.p01.org/FrontTrends_2016/

![](hsb/comet.jpg)

![](hsb/nebula.jpg)

![](hsb/fire-ball.jpg)

![](hsb/iris.jpg)


Fun story: around the time that I was posting these images on social
media, I took a photo of a drying tray in the kitchen.  Residues formed
a pattern resembling a galaxy.  My brother thought I generated it in p5. 😊

![](hsb/kitchen.jpg)


Folds
-----

Tomasz Sulej wrote a [fun tutorial][folds], based on which I created a
couple of images:

![](folds/tan.jpg)

![](folds/star.jpg)

![](folds/tiles.jpg)

  [folds]: https://generateme.wordpress.com/2016/04/11/folds/


L-systems
---------

On vacation
I was reading [The Algorithmic Beauty of Plants][abop]
(link to a&nbsp;17&nbsp;MB PDF)
on an iPad.
I struggled to simulate the presented systems in my head. I wanted to see them in action, see what they do step by step.
A friend created an LTE hotspot for me and I downloaded the [Pythonista][] app.
It was the first time I used Pythonista. I'm very impressed.
I'm amazed that thanks to this app I was able to *comfortably* create a program to interactively explore examples from the book.
Complete with UI and image generation. All of this *on an iPad* (a book reading device!) and offline (no Stack Overflow).
Pythonista is a very good creative environment with interface builder (!), documentation, custom keyboard keys, and great code completion.
I was surprised how not-painful it was to code on a tablet. Of course I'm faster on a physical keyboard but code completion helps a lot.
I think the difference in comfort is even smaller if you're not a Vim user.

![](l-systems.png)

  [abop]: http://algorithmicbotany.org/papers/abop/abop.pdf
  [Pythonista]: http://omz-software.com/pythonista/
