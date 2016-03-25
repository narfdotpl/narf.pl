2016-03-20

Sketchy procedures lead to a beautiful catastrophe
==================================================

Last night I wanted to create a program that could make images that
looked like pencil sketches.  I started with drawing edges of polygons
and it was OK, I quite liked the results.  Then I moved to "coloring" the
polygons, filling them with a zigzag.  I noticed an unexpected behavior
related to rotation of the zigzag.  At first I wanted to find the bug
and solve it, but in the end I decided to embrace it.  With a little bit
of tweaking it produces beautiful forms, some of which look
three-dimensional:


![](catastrophe@max-height.png)

*The results of applying "divide edges" and "zigzag" procedures multiple
times.  Most rows show the same algorithm applied to a triangle, square,
and pentagon, but there are a few images that don't follow this rule.*


<br>


![](fill.mp4)

*Fill procedure development progress.
[YouTube mirror](https://youtu.be/B-MeRtQcQU0).*


<br>


![](stroke.mp4)

*Stroke procedure development progress.
[YouTube mirror](https://youtu.be/5maIezJxZQs).*


Update • 2016-03-26
-------------------

I posted this to the [Procedural Generation subreddit][Reddit post].
I've never had [a 100%](reddit.png). :)

  [Reddit post]: https://www.reddit.com/r/proceduralgeneration/comments/4b7str/sketchy_procedures_lead_to_a_beautiful_catastrophe/
