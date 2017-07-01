2015-06-03

Checkers: Development panel with tweaks
=======================================

{{ youtube_iframe('IVBQ9l7Sm0E') }}

I created a development panel for my game.  It has two purposes:

- saving and loading game state
- tweaking values responsible for the look, feel, and behavior of the game,
  *while it's running*, without having to change the source code

In this post I will focus on the panel, but first let me mention other
things that I've done since the [previous update][].

  [previous update]: /posts/checkers-update-1


Since the previous update I have:
---------------------------------

- added the development panel
- switched from a 10x10 to an 8x8 board (because it's more fun)
- fixed bugs in the rules found by Karol and Wiola (thanks!)
- updated to Swift 1.2 (including `Set`s, which I've [added matchers for](https://github.com/Quick/Nimble/pull/93) to Quick/Nimble)
- moved operator functions to separate files to [improve compilation time](https://twitter.com/andy_matuschak/status/576165111355723776)
- switched from some of my own operators to the ones from [Prelude][]
- made sure that all the colors are [perfect](http://inaka.net/blog/2014/09/05/getting-the-right-colors-in-your-ios-app/)
- refactored a lot of stuff

  [Prelude]: https://github.com/robrix/Prelude


Development panel structure
---------------------------

First, please watch the whole [video][] from the top of this post, if
you haven't already.

  [video]: https://www.youtube.com/watch?v=IVBQ9l7Sm0E

When designing my own tweaks, my thinking was directed mostly by
annoyances that I've experienced when using [Facebook Tweaks][] in
Objective-C.  Don't get me wrong, they are not awesome but they are OK
and *you should totally use them* if you don't want to roll your own
solution.  Especially if you're in the dark land of objc where there is
only sorrow and eternal sadness...

  [Facebook Tweaks]: https://github.com/facebook/Tweaks

I set myself the following goals for the end-user API:

- arbitrarily nested structure (section in a table in a section in...)
- context-aware code completion (no magic strings!)
- ability to disable tweaks for release builds and running tests

I will start with the last one.

I decided to use the [Service Locator][] pattern after reading about
it in Robert Nystrom's [Game Programming Patterns][] book (which I
recommend).  The brief summary of this pattern is that instead of many
singletons you use one, the service locator, with "the other singletons"
exposed as its properties.  The key part is that these properties can
change and that access to them should always happen through the service
locator.  This allows you to, for example, disable services for release
builds, when running tests, or in some other conditions, at runtime.

  [Service Locator]: http://gameprogrammingpatterns.com/service-locator.html
  [Game Programming Patterns]: http://gameprogrammingpatterns.com/

You might think it's inelegant ("singleton, gah!") but this pattern is a
good fit for tweaks.  A quote from the Service Locator chapter:

> It is an ambient property of the environment, so plumbing it through ten
> layers of methods just so one deeply nested call can get to it is adding
> needless complexity to your code.

In my implementation of the Service Locator, I create the `services`
singleton with a dummy `developmentPanel` property:

    class Services {
        var developmentPanel = DevelopmentPanel(dummy: true)
    }

    let services = Services()

When the app launches, I switch to the real (not dummy) development
panel in an app delegate:

    if !application.isRunningTests {
        services.developmentPanel = DevelopmentPanel()
    }

As I mentioned, the panel table has an arbitrarily nested structure:

![](table.png)

*I'm experimenting with [Paper][]'s Think Kit + [Cosmonaut][] combo.*

  [Paper]: https://www.fiftythree.com/paper
  [Cosmonaut]: http://www.studioneat.com/products/cosmonaut

To take advantage of code completion, I assign sections to properties of
nested classes.  Apart from nesting, I also want to specify the order of
sections and items.  Unfortunately, bare properties don't give me the
ability to express this.  Therefore, I create the structure separately
and then assign its elements to corresponding properties.  I used to
do this by specifying table and section indexes but this turned out
to be too difficult to maintain, so I switched to `inout` arguments
(pragmatism beats purity):

    private let ds: Section = DummySection()


    class DevelopmentPanel {
        let _table: Table

        var colors = ds

        let board = Board(); class Board {
            let rules = Rules(); class Rules {
                var root   = ds
                var custom = ds
            }

            var highlights = ds
            var shake = ds
        }

        // ...

        init(dummy: Bool = false) {
            _table = dummy ? Table() : Table(items: [
                Item("Colors", &colors),

                Item("Board", board) {[
                    Item("Rules", &$0.rules.root, $0.rules) {[
                        Item("Custom", &$0.custom),
                    ]},
                    Item("Highlights", &$0.highlights),
                    Item("Shake", &$0.shake),
                ]},

                // ...
            ])
        }
    }

I know, this looks strange.  It's [DSL][]-ish in the wrong kind of way.
Nevertheless, I'm willing to have some "weird" code isolated in one part
of the app, if it results in the most convenient API exposed to the rest
of the system:

    let dev = services.developmentPanel.board.rules.custom

  [DSL]: http://en.wikipedia.org/wiki/Domain-specific_language


How tweaks work
---------------

I access tweaks through section methods.  They are defined separately
for each type:

    extension Section {
        func tweak(name: String)(x: Bool) -> Bool {
            // ...
        }
    }

I use the application operator from Rob Rix's [Prelude][] to have it so
that the value is first and the most important and the fact that it's
tweakable is secondary:

    let dev = services.developmentPanel.board.shake
    println(20 |> dev.tweak("dx"))

The first time this code is executed, a tweak item called "dx" is added
to the section in the table.  If this tweak has been saved in the past,
its value is read from disk, deserialized, and returned.  If it hasn't
been saved, the supplied value (20) is returned.  On any following call
the "current value", which can be changed in the UI, is returned.

The tweak itself is an object that knows both the current value and
the value provided in the source code.  It also has rows of buttons
that have titles and that can transform values, for example increment
numbers.  Tweak values can be serialized and they have descriptions
visible in the UI:

    class Tweak {
        let sourceCodeValue: TweakValue
        var currentValue: TweakValue
        let buttonRows: [[TweakButton]]

        // init...
    }

    struct TweakValue {
        let value: Any
        let description: String
        let serialized: String
    }

    struct TweakButton {
        let title: String
        let transform: TweakValue -> TweakValue
    }


Example tweak implementation
----------------------------

Tweaks for each type are implemented in separate files as extensions.
I provide here the actual implementation of the boolean tweak.

First, the tweak value has to have a description and support serialization:

    extension TweakValue {
        init(_ x: Bool) {
            value = x
            description = x.description
            serialized = JSON(["value": x]).rawString()!
        }

        init?(serializedBool: String) {
            if let x = JSON(rawString: serializedBool)["value"].bool {
                self.init(x)
            } else {
                return nil
            }
        }
    }

I delegate the actual serialization and deserialization to
[SwiftyJSON][], but it can be done in any other way.

  [SwiftyJSON]: https://github.com/SwiftyJSON/SwiftyJSON

Secondly, the tweak has to have buttons:

    extension Tweak {
        convenience init(_ x: Bool) {
            func button(title: String, f: Bool -> Bool) -> TweakButton {
                return TweakButton(title: title) { TweakValue(f($0.value as! Bool)) }
            }

            let v = TweakValue(x)
            self.init(sourceCodeValue: v, currentValue: v, buttonRows: [[
                button("false") { _ in false },
                button("true")  { _ in true  },
            ]])
        }
    }

Finally, the `Section` class has to be extended with a method providing
the tweak:

    extension Section {
        func tweak(name: String)(x: Bool) -> Bool {
            return isDummy ? x : getOrCreateTweak(
                name: name,
                create: { Tweak(x) },
                deserialize: { TweakValue(serializedBool: $0) }
            ) as! Bool
        }
    }

There are two things that bother me here but I couldn't come up with
a better solution.  First is the use of the `isDummy` property.
`DummySection` is a subclass of `Section` that allows the whole tweaks
functionality to be disabled.  It's not possible to create an extension
of `DummySection` that overrides the `tweak` method to do nothing.
Therefore, `Section` extension has to know about the "dummy feature" --
in the form of the `isDummy` property.

The second thing that bugs me are forced casts (exclamation marks).
They are there because the whole knowledge about the actual type of a
tweak is contained in the `tweak` method — `Tweak`, `TweakValue`, and
`TweakButton` don't use generics.  They can't, because `Tweak` is owned
by `Item` and `Section` can have many `Item`s.  In this relationship all
generic tweaks in a section would have to have the same type and this is
too strong of a restriction for my use case.

On a happier note, I want to point out that the implementation of
tweaks for specific types is reusable.  For example, `CGFloat` and
`HalfOpenInterval<Double>` tweaks both reuse the implementation for
`Double`, including buttons and some subtle rounding that I perform
behind the scenes (try `echo '0.3 - 0.1 - 0.1 - 0.1' | xcrun swift`).


Performance
-----------

Relax.  It's OK.

> I don't know what to make of the continual stream of people in 2015
> with fixations on low-level performance and control.
>
> -- [James Hague](http://prog21.dadgum.com/204.html)

Tweaks make the program a little bit slower, of course, because they are
another thing that has to be done.  I didn't measure it but I didn't
notice any slowness.

Tweaks add an overhead of finding a few properties and calling a few
simple functions.  They are negligible compared to computational cost of
moving things on the screen.  Deserialization happens only on the first
access.  In release builds I use dummy tweaks that return the supplied
value right away and bypass the whole serialization/<wbr/>remembering
mechanism.  I think that `tweak` methods can be optimized by adding an
`#if DEBUG` clause and asking the compiler to inline the method, but I
would have to find the time too look at the assembly to verify this:

    extension Section {
        @inline(__always)
        func tweak(name: String)(x: Bool) -> Bool {
            #if DEBUG
                return isDummy ? x : getOrCreateTweak(
                    name: name,
                    create: { Tweak(x) },
                    deserialize: { TweakValue(serializedBool: $0) }
                ) as! Bool
            #else
                return x
            #endif
        }
    }

Another possible optimization, at the cost of the ease of use, might
be switching from a property access to a function call and #ifDEBUGging
(it's a verb now) and inlining it as well:

    // current version
    let dev = services.developmentPanel.piece.explosion

    // possible optimization
    let dev = services.developmentPanel { $0.piece.explosion }


Open source
-----------

My implementation of tweaks is not open-sourced at the moment and I
don't know if it will ever be.

There are a couple of reasons for that, for example the UI is specific
to my game, the buttons I use for each type are tailored to my needs,
and so on.  The current version is the 5th or 6th implementation -- I
believe it's easier to make big changes in the private rather than in
the open, without feeling the need to justify decisions and layout the
pros and cons.  This aspect is the biggest point against open-sourcing:
making the code public [creates and obligation][puppy], whether real or
imaginary, to maintain it, respond to issues, write documentation, etc.
It is something I don't want to spend time on currently.

  [puppy]: https://twitter.com/trek/status/605079211049512960

Having written this, it doesn't mean that everything is lost.  The point
of this post is to, well... show off... but besides that to present an
idea and start a discussion.  It might materialize in something that
everybody will be able to use.

One of the Checkers' components has already completed this journey.  I
rely heavily on state machines (I should blog about this...) and I went
through several private implementations of them.  I also discussed the
topic with colleagues and thought about the problem a lot.  The result
of this process is the [SwiftyStateMachine][] open source µframework
that I [wrote at Macoscope][Macoscope blogpost].

  [SwiftyStateMachine]: https://github.com/macoscope/SwiftyStateMachine
  [Macoscope blogpost]: http://macoscope.com/blog/swifty-state-machine/


The future
----------

I feel that I'm closer to the end than to the beginning of this project.
It's a good feeling!  I reviewed the list of things that I need to
do before releasing the game and I split remaining tasks (GitHub
Issues: 43 open, 54 closed) into small milestones, each of which should
be achievable in a weekend (yeah, right...).  This also made me feel
good but then I counted the milestones and realised there's about a
dozen of them, which means, given the fact that I work on this game on
every other weekend or so, they might take half a year to complete...
Well, time will tell.

To see how this project unfolds, follow me on Twitter (I am
[@narfdotpl][]), subscribe to the [Checkers newsletter][newsletter] or, even
better, subscribe to the [RSS feed][] of my site.

  [@narfdotpl]: https://twitter.com/narfdotpl
  [newsletter]: /newsletter
  [RSS feed]: /feed


Shattering the fourth wall
--------------------------

> And now for something completely different!

I'm a recovering perfectionist and producing these updates is hard for
me.  Part of me is angry that even though I cut many corners, it still
takes a lot of time (I estimate that creating this post, including the
video, took between 20 and 30 hours).  The other part of me is even more
unhappy, because these things are barely good enough to be published.
But the alternative is to never ship anything, so here we are.

For the sake of documenting the process, or showing some "hacks", I
thought I will summerise how I made the video for this post.

Originally I wanted to go half-[CGP][] and record a very fast-paced
video with many short cuts in rapid succession.  I was thinking about
mixing camera footage with an Xcode screencast, buying or borrowing a
good microphone, a tripod, a GoPro...  Did I mention I'm recovering?

  [CGP]: http://www.cgpgrey.com/

I ended up taking a much more lo-fi approach.  I experimented with what
I wanted to show and wrote down everything I wanted to say, about 1200
words.  I recorded myself reading the script using Voice Memos, the
stock iOS app, on an iPhone 6.  The first take was Good Enough™, so I
didn't try to repeat it.

Then, I played the recording from the speakers and used Instagram's
[Hyperlapse][], also on an iPhone 6, to record myself tapping and
swiping on an iPad, trying to do everything in sync with the prerecorded
voice.  I used Hyperlapse to limit the amount of perceived camera shake.
It went OK, again at the first try, even though I got a bit out of sync
in a few places (especially around the 5:15 mark).

  [Hyperlapse]: https://hyperlapse.instagram.com/

I created the slides you see in the video in the [Deckset][] app, on
OS&nbsp;X, and presented them in the Dropbox app.  Before putting the
slides in Dropbox, I exported them to PDF and converted that PDF into a
series of PNGs, using [ImageMagick][]:

    convert -density 108 slides.pdf slides/%02d.png

  [Deckset]: http://decksetapp.com/
  [ImageMagick]: http://www.imagemagick.org/

I used iMovie to put both recordings together and uploaded the final
video to YouTube from the app.

That's it.  Enjoy the summer in the northern hemisphere and see you next
time!

---

*You can discuss this post on [Reddit][] or message me on [Twitter][].*

  [Reddit]: http://www.reddit.com/r/gamedev/comments/38d4kn/tweaking_values_while_the_game_is_running/
  [Twitter]: https://twitter.com/narfdotpl/status/606086074050461697
