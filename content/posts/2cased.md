2016-07-06

Replace booleans with two-cased enumerations
============================================

When programming, we often describe state of objects in terms of
boolean properties, on/off switches.  Using a true/false value is an
*easy* solution, the one at hand, but it might cause problems when our
applications evolve.  Next time you are about to use a boolean value to
describe state, consider creating a two-cased [enumeration][] for that
purpose.  Especially, if your programming language has decent support
for enums.  (In Swift, for example, enums are a pleasure to work with.
In Python, not so much.)

  [enumeration]: https://developer.apple.com/library/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Enumerations.html

I'm writing this post because, admittedly, I don't use enumerations
often enough.  They just aren't as easy to use as booleans.  They have
friction: you have to define enums before you can use them.  You have to
stop for a minute, think about what and how you want to describe, where
to put the enum definition, etc.  It's an entry fee you have to pay, but
it buys you a tool that I think is both more powerful and *simpler* than
booleans in a few important ways:

- **Enumerations are explicit and descriptive.**  When using enums you
  have to name all the possible options instead of just the "true" case
  (e.g. "move.dynamic = gentle/rapid" vs "move.isRapid = true/false").
  It makes it easier to understand the meaning of the value without extra
  information.  One doesn't have to wonder what "not true" means. Being
  explicit protects you against miscommunication in the team and your own
  bad memory.  It is also helpful in situations when what the value stands
  for depends on the context of your application -- because your
  application *will change* with time.

- **Enumerations make growth easier.**  I recommend starting with enums
  rather than booleans because the effort of adding a third case to an
  enum is an order of magnitude smaller than the effort of switching
  from a boolean value to something that supports three-valued logic.
  Of course, this "something" is an enumeration because adding a second
  boolean to support three-valued logic is trap: you end up with four
  possible combinations, one of which is invalid, but the language
  doesn't know about it so it can't protect you against reaching the
  invalid state.  It's less work to start with an enum than to refactor
  a boolean into an enum later on because you might be forced to make
  changes in many places if the boolean value you want to refactor have
  propagated through the system, been passed to functions, gotten stored
  as properties of different objects, etc.  The boolean refactoring cost
  gets even higher if you serialized those values, stored them in a
  database, or if you have to support clients using the old data format.
  In all those situations extending an already existing enum with an
  additional case is trivial.

- **Enumerations are safer.**  You can accidentally use an incorrect
  boolean value -- one from a different property or a different object.
  Type systems in some languages, for example in Swift, won't let you
  make such mistakes if those properties use different enum types.  For
  example, typing "game.state = move.dynamic" doesn't make sense and will
  result in a compilation error.  Typing "game.isPaused = move.isRapid"
  is equally nonsensical but the compiler won't complain about it because
  types match.  There are more benefits still: in Swift the compiler will
  raise errors if you add a new case to an enum but forget to handle it
  in a switch statement somewhere in your code, which allows you to make
  such changes with confidence.  Even in dynamic languages making changes
  is safer when using enumerations because it's easier to grep (or [ag][])
  for enum cases than it is to track down all the uses of a specific
  boolean property.

  [ag]: https://github.com/ggreer/the_silver_searcher

As you can see, enumerations are a useful tool to have in your tool box.
Use them to your advantage.
