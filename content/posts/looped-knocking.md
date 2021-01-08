date: 2017-04-24
collections: [sound]

Looped knocking
===============

Quick musical(?) experiment. I recorded knocking on the desk, repeated
it a hundred times, and combined it with two speeds: the original one and
slower by 1%. This way the slower knocking shifts with respect to the
original.

{{ youtube_iframe('Kn7s8z6ACmo') }}

It's simultaneously obvious and magical that a rhythm layered on itself
with some shift gives a new rhythm that is sometimes pleasing to the
ear (or at least acceptable). Every couple dozen of seconds one can
hear something that could be "composed" by a human: around 0:20, 0:44,
1:20, 2:05, 2:25, 2:40... It's great that these new rhythms appear
unexpectedly and after a few seconds they dissolve into noise.

I recorded the knocking using QuickTime. I processed it on the
command line using `ffmpeg` and `sox`:

    ffmpeg -i source.{aifc,wav}
    sox source.wav repeated.wav repeat 100
    sox repeated{,-slower}.wav tempo 0.99
    sox repeated{,-slower}.wav --combine merge combined.wav
    play combined.wav

I combined the audio with an image using `ffmpeg`:

    ffmpeg -loop 1 -i knocking.png -i combined.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out.mp4
