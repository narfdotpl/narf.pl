2017-04-23

Quadruped robot movement
========================

I want to build a "four-legged spider" robot. It's a fun project because
1) robots are cool and 2) I have very little experience with hardware,
so I get to learn a lot of new things and be creative in new ways. Many
areas are unknown unknowns to me -- I don't know what I don't know.

I pick topics in a semi-random order and I build skills
and create proof-of-concepts that I think will be
useful for the final machine.  So far I've played with
[soldering](https://www.instagram.com/p/BOhV70egSlt/),
[3D graphics](https://www.instagram.com/p/BOzqQzPDTP9/),
[electronics](https://www.instagram.com/p/BQxIbDxjjmY/),
[batteries](https://www.instagram.com/p/BRjAw1xjTpG/),
[3D printing](https://www.instagram.com/p/BRq6aQVjZ7n/), and
[remote control](https://www.instagram.com/p/BR9C63LDSCq/).
Last week I was working on movement:

![](loop.mp4)

I was figuring out where to move legs, and in what order, to achieve a
given move. It was a fun way to challenge spatial imagination. I built a
repertoire of moves: get up, look around, walk forward, turn in place,
walk sideways, walk in a circle (turn), lay down. Each of the moves
is implemented as a separate routine that can be parametrized with
different arguments: direction, angle, step length, duration, etc. I
plan to use this work in the future application that will control the
robot based on inputs from the user.

I focused on statically stable movement: only one leg is in the air at
time. The other three form a triangle on the ground and the center of
mass is inside it so that the robot won't fall off. The movement can be
stopped at any time and the robot will be stable.

In the future I want to experiment with dynamically stable movement so
that the robot could move faster and more smoothly. I didn't do it now
because I don't have the infrastructure to simulate gravitation and
ground collisions in a way that won't interfere with my movement logic
yet -- what you see is an animation, there's no gravity. I also don't
know the final dimensions or weight distributions of the robot because I
haven't built it yet. (But once I do I will be able to immediately test
the moves you've seen above, so it made sense to prepare them first.)

I modeled the skeleton in Blender and implemented the animation as a
Python plugin for Blender. In Python I set the location of the tip
of each leg, location of the body, and body's rotation. Blender's
inverse kinematics engine takes care of moving individual joints of
the skeleton. When my plugin starts, it generates the full state for
each frame of the animation. Blender reads the states frame by frame
and updates the display. This way I can easily "crop" the animation to
see only the fragment I am currently working on. I can also loop it or
play it slower or faster without touching the code responsible for the
movement itself.

That's all for today. See you in the future in another robot post. ✌️🤖
