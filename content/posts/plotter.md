date: 2017-10-04
collections: [robotics]

Prusa i3 MK2S pen plotter
=========================

Two weekends ago I experimented with changing my [3D printer][] into
a pen plotter. I designed a holder for the pen and attached it to the
extruder motor. As it's often the case with my designs, the third
version worked OK...

{{ youtube_iframe('M6ilalRPrgk') }}

I modified two of my generators ([tree][] and [fireball][]) to output
[gcode][] to control the printer. The results are good for a weekend
hack, but they're nowhere near the [AxiDraw][] level.

- ![](test.jpg)
- ![](tree.jpg)
- ![](fireball.jpg)

If I ever return to this project, I'll try to modify the holder to allow
some vertical movement -- the current version often presses the paper
too strongly. I'll also try using a pen a little bit more fancy than an
orange BIC. 😉

  [3D printer]: /posts/prusa
  [gcode]: https://en.wikipedia.org/wiki/G-code
  [AxiDraw]: https://www.axidraw.com/
  [tree]: /posts/procedural-trees
  [fireball]: /summer-of-creative-coding
