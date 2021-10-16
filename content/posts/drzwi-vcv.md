date: 2020-11-21
collections: [sound, procedural]
theme: black

VCV Rack sound design/simulation
================================

{{ youtube_iframe('j6qeedHYA7w') }}

I've been playing with virtual modular synthesisers in VCV Rack and I
decided to use them to create audio for my [*Drzwi*](/posts/drzwi)
animation from roughly a year ago.

Designing sound for it was entertaining and intellectually stimulating
for a couple of reasons.

First of all, modular synths are awesome. It is mindblowing to me that
these things can create such an incredible variety of sounds and that
you can use them as building blocks to essentially create your own
instruments. When you stop seeing them as a random mess of wires and you
start consciously tweaking and connecting them -- this moment is very
gratifying. Being able to come up with ideas and build
tools to realize them feels great.  If you're interested in learning
how to use modular synthesisers, I highly recommend the [*Learning
Synths*][Ableton] website from Ableton.

  [Ableton]: https://learningsynths.ableton.com/

Secondly, VCV Rack is a digital system. Simulating analog electronics.
Connected using virtual wires... Let that sink in. Now, think about the
fact that [some of the modules][Vult] numerically solve differential
equations on the fly to replicate the behaviour of real circuits.

  [Vult]: https://modlfo.github.io/VultModules/

Finally, this approach is interesting to me because of the contrast.
On one hand, all this setup is abstract and made up by me. The original
animation is abstract as well. On the other hand, both in the video
and in the audio I'm trying to simulate and convey aspects of physical
reality. I made the animation in code and I adapted my program to take
into account velocity and position of all the elements in 3D space. I
use this information to send MIDI CC signals from my program to VCV
Rack to control 30-something knobs and sliders in the synthesiser. I
implemented things like the Doppler effect, different amplitudes for
each ear based on position, doors that muffle sound coming from behind
them, and so on.  I dialed some of these effects down so they are quite
subtle, but I believe that combined together they create a convincing
feeling of being immersed in something that could be a form of reality.
