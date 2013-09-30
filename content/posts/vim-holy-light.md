2013-07-18

Vim: Holy Light
===============

I'm a [Solarized][] fan.  In Vim, I used to manually switch between the
dark and the light modes depending on the [lighting conditions][].  Two
weeks ago, while browsing [usevim][]'s feed, I found [Holy Light][] --
"a plugin for Macs that changes the `background` variable based on the
amount of ambient light recorded by Mac's light sensor."

  [Solarized]: http://ethanschoonover.com/solarized
  [lighting conditions]: http://youtu.be/OobUV9q0aDA?t=1m17s
  [usevim]: http://usevim.com/2013/07/03/holy-light/
  [Holy Light]: https://github.com/Dinduks/vim-holylight

To use Holy Light, you have to set a threshold for the ambient light
level.  When measured value is above that threshold, the light
background is used; when it's below the threshold, the background
is dark.  Access to the light sensor data is provided by the
`holylight-checker` binary bundled with the plugin.

What caught my attention is that the measured values are in the range of
millions[1] (of unknown units).  This suggests an incredible fidelity!
I decided to investigate.  I recorded the light level every five seconds
during a day at the office.  Here are my results[2].

![Ambient light level](ambient-light-level.png)

As expected, measurements aren't precise.  You can safely discard last
five digits of that million.  Or even six:

![Ambient light level, last 5 and 6 digits discarded](ambient-light-level-discarded.png)

------------------------------------------------------------------------------

1. Measured values might be hardware related.  I got them on a late 2011
   13-inch MacBook Air.

2. [Data and code][] are on GitHub.

  [data and code]: https://github.com/narfdotpl/narf.pl/tree/master/content/assets/vim-holy-light
