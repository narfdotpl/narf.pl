2015-08-20

Checkers: Swift 1.2 to 2.0 transition in numbers and impressions
================================================================

In my spare time I work on a [futuristic checkers game][glitch] for the
iPad, written purely in Swift and SpriteKit.  Last week I updated the
codebase from Swift 1.2 (Xcode 6.4) to Swift 2.0 (Xcode 7β5).

In this post I outline the process and give some stats about the
conversion, partly to document the experience of making such a
transition in a "real project", and partly to have something to show
besides the [look of disapproval][] the next time I hear someone say
"I&nbsp;won't use Swift, because each time a new Xcode comes out, you
have to rewrite *everything*"...

  [glitch]: https://instagram.com/p/6ZJleoF8fp/
  [look of disapproval]: http://knowyourmeme.com/memes/%E0%B2%A0_%E0%B2%A0-look-of-disapproval


tl;dr
-----

See the summary at the end, if you are not interested in details.


Size
----

First, some context.  I work on Checkers alone in my spare time.  I
started the Swift incarnation of the project 11 months ago (it hurt a
little to find this out).  I strive for "flamboyant minimalism" :wink:,
therefore Checkers might seem like a small project, but I consider
it a Medium on the S-M-L-XL spectrum.  Before the Swift 1.2 to 2.0
conversion, Checkers consisted of:

- 540 commits
- 61 `.swift` files
- 7008 lines of code (keep in mind that Swift is orders of magnitude
  more expressive than Objective-C and as such needs less code)
- 5019 lines of code-code (~72%)
- 553 lines of comments (~8%)
- 1436 blank lines (~20%)
- 36 classes
- 19 `struct`s
- 18 `enum`s
- 278 functions or methods
- unknown number of closures (they are harder to `grep`)


Betas
-----

Before β5 I had a frustrating experience with Xcode 7.  It boils down to
the fact that betas are not final products.  They are not expected to
work (well) all the time.  And they don't.

In β1 and β2, after going through automatic Swift code conversion and
manual fixes, the compiler crashed on me with error messages I didn't
understand.  I couldn't quickly google workarounds for these problems,
so I decided to not spend time on them, continue working in Xcode 6, and
wait for another Xcode 7 beta (they come out roughly every two weeks).

β3 [crashed on launch][crash].  After removing the source of the crash,
I managed to get Checkers to compile, but I had to disable sound.
Unfortunately, the IDE would launch the app on a device/simulator only
on what seemed like every tenth try or so.  Besides that issue, it would
spontaneously bring up all the cores of my MacBook to 100% utilization.
β3 was effectively unusable with this project.

  [crash]: https://twitter.com/narfdotpl/status/619216999105843200

To be fair, I suspect most of the problems I encountered were due to the
fact that I make heavy use of advanced features -- like closures combined
with currying and custom operators in [tweaks][] and [`mutate`][mutate],
big `enum`-based [state machines][], closure-based generic memoization,
etc.

  [tweaks]: /posts/checkers-development-panel
  [mutate]: https://github.com/narfdotpl/doodles/blob/master/doodles/mutate.swift
  [state machines]: https://github.com/macoscope/SwiftyStateMachine

I skipped β4.

β5 fixed the problems of β3.  I now use Xcode 7β5 and iOS 9
to develop Checkers.  It's overall a better experience than using Xcode
6.4, because the language is better, but the compilation time *feels*
a little bit longer to me.  I didn't measure it, though.

Before I start describing the 6.4→7β5 transition steps, I'll mention one
problem I had with β5.  After launching the Xcode beta, `socketfilterfw`
would take 100% of the CPU for about 3 minutes.  This was a large
inconvenience for me because of my workflow, which includes often Xcode
restarts: I commit often and arrange work-in-progress commits using `git
rebase --interactive`.  Each time I do this, I quit Xcode, because for
as long as I remember, it handled such changes *horribly*: it messes
up working directory, or worse, brings Derived Data to an inconsistent
state, which results in reproducible-only-on-this-machine compile-time,
or even worse, run-time bugs.

In my case, the "firewall is trying to set my desk on fire when I
launch Xcode 7" issue was [fixed][heat] by removing Xcode from a list
in firewall options.  (And restarting.  Restarting helps.  I habitually
delete Derived Data and restart everything within the 3&nbsp;meter
radius to fix Xcode issues of all kind, beta or not...)

  [heat]: https://twitter.com/narfdotpl/status/631598385980678145


Automatic conversion
--------------------

The whole transition of the project from Xcode 6.4 to 7β5 took about
two hours, of which the automatic conversion was the fastest -- it
took about half an hour to run, verify changes, manually fix remaining
issues, and do some cleanup.

The most time-consuming part was an optional step of adopting new
language features, which I describe in separate sections.

Before automatic conversion, I had 7008 lines of code.  The conversion
diff has 109 deletions and 113 insertions, which means Xcode
automatically took ~1.5% of the project and replaced it with new code.


Manual cleanup
--------------

After automatic conversion to Swift 2, the project would not compile,
because some changes were needed, which could not be performed
automatically.

My "fix errors and warnings" commit has 90 deletions and 84 insertions
-- change to ~1.5% of the code, including `s/var/let/` in 30 lines.

To finalize the conversion, before using new features, I manually
reverted changes to functions with multiple arguments -- by default
argument names were not used when calling functions in Swift 1.2 and
they got added in Swift 2.0.  I removed them where I didn't want them.
25 deletions and insertions, ~0.5% change.


`enum` representation
---------------------

The first new feature I wanted to use, because it was obvious where to
apply it, were default string representations of `enum` cases.  I use
enumerations in [state machines][] and need their representations when
generating diagrams.

The change was trivial but sound in terms of the number of lines of
code: 167 deletions, 26 insertions.  A ~2% decrease in the vein of:

    +extension DOTLabelable {
    +    var DOTLabel: String {
    +        return "\(self)"
    +    }
    +}

    -extension SquareNodeState: CustomStringConvertible {
    -    var description: String {
    -        switch self {
    -            case Initial:               return "Initial"
    -            case Invisible:             return "Invisible"
    -            case AnimatingIn:           return "AnimatingIn"
    -            case Idle:                  return "Idle"
    -            case AnimatingHighlighting: return "AnimatingHighlighting"
    -        }
    -    }
    -}


`guard`
-------

The next feature I was eager to use was `guard`.  It reduces nesting and
removes instances of force-unwrapping optionals.

In terms of the number of lines it doesn't help much.  In my case it
lead to a slight increase (80 deletions, 84 insertions) as I experiment
with laying out the statement vertically:

    guard let
        s1 = previousSnapshot,
        s2 = snapshot,
        sprite = originalSprite,
        body = sprite.physicsBody
    where
        body.dynamic
    else {
        return
    }


`if case`
---------

`if case` is a good replacement for a `switch` with a single `case` and
a `default` clause.  I don't use pattern matching outside of `enum`s
(yet?), so my diff is rather small.  31 deletions, 14 insertions:

    if case .Idle = currentState {
        originalSprite?.physicsBody?.dynamic = false
    }

    // etc.


`for where`
-----------

`for where` feels weird.  Sometimes I think [`.filter`][filter] would
fit better.  Definitely it looks bizarre when I'm left with a `for` loop
containing only a `return` statement.  But maybe this is a hint from the
language designers that I should use `.lazy.filter{}.first` there...?
*Maybe*...?

  [filter]: http://swiftdoc.org/swift-2/protocol/SequenceType/#func-filter

34 deletions, 26 insertions.


Other features
--------------

Error handling is the elephant in the room.  I don't use it because I
don't think I have operations that could fail in a way that I could
recover from.  (I don't have networking.)

I searched for occurrences of `($0)` and started using things as if
they were functions: `.map(Foo.init)` instead of `.map(Foo($0))`, etc.
3 deletions, 3 insertions.

I removed explicit raw values from string enumerations.  I had only
one such `enum` with only two cases, so 2 deletions, 2 insertions.

`defer` seems like a good idea, but so far I use it in only one place:

    // not actual Checkers source (but close)
    var nextFragments: [PiecePolygonSpriteNode] {
        defer { i = (i + 1) % xs.count }
        return xs[i]
    }

This closes the list of changes specific to the Swift 1.2 to 2.0
transition.


Summary
-------

Betas are problematic.  I had to wait for β5 to be able to work on
Checkers using Swift 2. (Or β4.  I didn't check β4.)

By β5, updating was fast and easy.  In my project of ~7000 lines of
code, ~60 files, and ~70 types, automatic conversion affected ~1.5% of
the codebase.  Manual tweaks/cleanup touched similar amount of code.
Together they took ~30 minutes.

Refactoring to adopt new language features took ~1.5&nbsp;h and resulted
in ~2% less code.  The change in the number of lines of code was mostly
due to my use of [`enum`s with descriptions][state machines], though.

I recommend updating from Xcode 6.4 to 7 today, because a) it can be
actually done now because things work, and b) Swift 2 is better, has
`guard`, protocol extensions, and other nice additions.  By now you
should update anyway to test on iOS 9.

PS When I finished writing this, I had an idea to check how the transition
looks like in terms of the number of characters in the source code
instead of the number of lines.  I don't want to redo calculations
for each step, but before the transition I had 226790 characters and
afterwards I had 6396 less.  A ~3% decrease.
