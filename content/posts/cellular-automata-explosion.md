date: 2020-12-09
collections: [procedural]
theme: black

Cellular automata: explosion
============================

![](explosion.mp4)

I’m taking part in an eight weeks long [compute shader workshop][workshop] by [arsiliath][]. This is my take on “The Edge of Chaos”, the first assignment.

  [workshop]: https://paprika.studio/workshops/compute/index.html
  [arsiliath]: https://twitter.com/arsiliath

Everything here is created in real time by a 200-line shader running on the GPU. (Such demoscene, wow.) I layered multiple techniques to achieve the final effect.

The goal of the assignment was to implement a one-dimensional cellular automaton. It’s the edge of the explosion in my piece. We were supposed to display the automaton in such a way that one can see its history, for example pixels from each iteration could be in a separate row/column.

I decided to map the automaton to a semi-circle and use random iteration rules that I change over time. Random rules is how I get these bands in the pattern. Also, this is how I dodged the difficult part of the assignment: coming up with rules that create interesting results.

Next, I added waves and reflections in the bottom half of the image. Having the idea about reflections in the water and figuring out how to implement them was the most enjoyable part of this project.

To make the piece more engaging, as the final layer I added another, this time two-dimensional, cellular automaton. It’s the flashy/fast part in the center of the explosion. The 2D automaton is delayed by a few seconds and works in the “historical area” of the 1D one — it modifies the few-seconds-old parts of the pattern. It’s also heavily randomized, turned on and off.

So yeah, the first week was fun. I like how shaders force you to think in a different way, from the perspective of an individual pixel. I’m looking forward to more.
