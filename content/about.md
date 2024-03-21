I create software, make procedural graphics, and compose [music][].
I'm an experienced engineer and I like making cool stuff, so if my taste resonates with you, let's build something great together! Email me at [{{ email }}][email].

That's the tldr ^ (turns out, it's bloody difficult to write an /about page for your own website). For my professional history, check out my [LinkedIn][] or continue reading.

—

I enjoy working on projects requiring a holistic/multidisciplinary approach and I like learning new techniques and technologies, especially when they open possibilities for exciting results. During two decades of building software, I have worked on web backends, web frontends, native iPhone and iPad apps, an iPhone and iPad [game][], a four-legged spider [robot][], [2D][] and [3D][] procedural animations, GPU-based [simulations][], interactive experiments, data visualization that was on the front page of [Reddit][], as well as countless internal and open-source tools, libraries, microframeworks, and plugins.

For the last five+ years, I've been working remotely with [Ro][], a health tech startup focused on goal-oriented healthcare, headquartered in New York. I joined Ro as the fourth engineer focused on Python backend services and I've been a part of many teams as I've witnessed the company grow 15x from dozens to hundreds of people and a $7B valuation.  Over the years, I have worked on many aspects of our systems, touching applications for patients, doctors, and pharmacists.  Some of the highlights include a data-change tracking microframework, that I've built on top of Django, and my tenure in the mobile team. I've joined the iOS effort as the first backend engineer when we started working on our first mobile app for patients, after years of offering the web experience on mobile. The iOS app was our first product to showcase Ro's rebranding and it set a new benchmark for patient experience on our platform. I co-designed and implemented the way the app communicates with our systems, helped create our server-driven UI architecture, and contributed native iOS code in addition to working primarily on the backend.

Check out my personal projects linked below and feel free to browse the rest of my [blog][]. When it comes to other online presence, I also have a~[link blog][] and I am on{% for p in profiles.values() %}{% if loop.last %} and{% endif %} [{{ p.name }}][]{% if loop.last %} too.{% else %},{% endif %}{% endfor %}

-- [narf](/)

  [music]: /music
  [game]: /checkers
  [robot]: /posts/its-alive
  [2D]: /posts/procedural-trees
  [3D]: /music/maladaptive
  [simulations]: /posts/tears-in-rain
  [Reddit]: https://www.reddit.com/r/dataisbeautiful/comments/33clwk/music_streaming_impact_number_of_artists_i/

  [Ro]: https://ro.co

  [email]: mailto:{{ email }}
  [blog]: /posts
  [link blog]: http://links.narf.pl/

{% for p in profiles.values() %}
  [{{ p.name }}]: {{ p.url }}
{% endfor %}
