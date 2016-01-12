2016-01-12

Lenses in Swift, or how to change parts of immutable objects
============================================================

Previous Sunday, over breakfast, I watched Brandon Williams' talk [Lenses in Swift][talk].  It wasn't the first time I've heard about the idea, but it was as if Brandon's explanation had suddenly opened my eyes.  I finally got it!  I couldn't stop thinking about this topic.

I started to wonder: could one design a lenses API that was more familiar to non-functional-programming crowd?  Would creating a code generator mentioned by Brandon be much work?

It led me to start experimenting.  I gathered results of these experiments here, in this post, and in [Lenso][], a Swift µframework and code generator that I published on GitHub.  Stay here and continue reading for more story and more information about lenses.  Visit GitHub for a shorter and much more dry version.

  [talk]: https://www.youtube.com/watch?v=ofjehH9f-CU
  [Lenso]: https://github.com/narfdotpl/lenso

[![](github.png)][Lenso]


Immutable objects
-----------------

Before we talk about what lenses *are*, let's discuss what they are *for*.  They are for immutable compound objects: structs and classes that have all properties declared as constants.

There are practical advantages to using immutable objects in many situations.  Because those objects can't change, code that is dealing with them is more predictable and can be isolated from other pieces of the system.  With immutable entities, there are no implicit dependencies on other owners of an object, because even if there any are other owners, they can't change the object.  You don't have to worry that an entity you're dealing with will suddenly get modified by the OS, by the user, or by your own code running on another thread.

Sometimes you want to make a change, though.  Say you have a person living under a given address and you want them to move to some other street.

    struct Person {
        let name: String
        let address: Address
    }

    struct Address {
        let street: String
    }

    let author = Person(
        name: "Maciej Konieczny",
        address: Address(street: "Sesame Street")
    )

Because you can't change anything, you have to create a new `Address`, and then create a whole new `Person`, using the new address and pieces of the old person:

    let author2 = Person(
        name: author.name,
        address: Address(street: "Baker Street")
    )

This code is not particularly nice to read or write.  It gets worse when objects have more properties, especially when they are nested.

This is where lenses come to help.


"Lenses"?
---------

Lenses are "functional getters and setters".  This was the main thing I remembered from the talk.  I finished breakfast, ran out of the apartment, and hopped on a train.  I was trying to reimplement what I've heard and come up with a better API: first, scribbling in a notebook during my journey; later, silently in my head while seated at a family dinner at my girlfriend's.  I returned in the evening and started typing away in a playground, confident that I have a grasp of the topic.

Lenses are "functional getters and setters".  A lens is implemented for a `Whole` object and its `Part`.  You can "look through" the lens at an object to get its part, to "zoom in on it" — the lens acts as a getter.  You can also use the lens to change a part of an object, then it acts like a setter.  Of course, we're talking about immutable objects, so after "setting" a value, the lens returns a new `Whole` object with the new part swapped in:

    struct Lens<Whole, Part> {
        let get: Whole -> Part
        let set: (Part, Whole) -> Whole
    }

I want to thank Brandon for introducing the `Whole` and `Part` nomenclature in his talk.  It made it much easier for me to understand than generic `A`s and `B`s.

Given a model from the previous section, a lens for a person's name is implemented and used like this:

    let personNameLens = Lens<Person, String>(
        get: { $0.name },
        set: { (newName, person) in
            Person(name: newName,
                   address: person.address)
        }
    )

    let author3 = personNameLens.set("narf", author)

I admit, the last line doesn't look like a big improvement yet, especially given that we had to write extra code.  Keep in mind though, that some of it is library code and the rest is so simple it can be generated.  My tool, [Lenso][], generates such lenses for each specified model and puts them in a `Lenses` struct inside a model extension:

    extension Person {
        struct Lenses {
            static let name = ...

    let author3 = Person.Lenses.name.set("narf", author)

Before we get to the final API, we have to take a few more steps.  First, we have to talk about a crucial property of lenses: the fact that they can be composed.


Lens composition
----------------

If you have a lens from A to B and a lens from B to C, you can compose them to make a new lens, from A to C:

    let personStreetLens = Person.Lenses.address.compose(Address.Lenses.street)
    let author2 = personStreetLens.set("Baker Street", author)

This was when I started to see the benefits of lenses.  I would prefer to write such code instead of nested `init`s.  I think the syntax can be improved, but I'll get to that in the next section.  Here I will only note that composition implementation is surprisingly straightforward and easy to follow when you break the getter and the setter into local constants:

    extension Lens {
        func compose<Subpart>(other: Lens<Part, Subpart>) -> Lens<Whole, Subpart> {
            return Lens<Whole, Subpart>(
                get: { whole in
                    let part = self.get(whole)
                    let subpart = other.get(part)

                    return subpart
                },
                set: { (newSubpart, whole) in
                    let part = self.get(whole)
                    let newPart = other.set(newSubpart, part)
                    let newWhole = self.set(newPart, whole)

                    return newWhole
                }
            )
        }
    }


Syntax
------

I would argue that the above API is already an improvement over nested initializers, but it still requires a lot of typing and feels "indirect".  To make it readable you almost have to introduce a lens as local constant before you can use it.  In his talk, Brandon proposed a solution to this problem employing custom operators:

    let author2 = author |> Person.Lenses.address * Address.Lenses.street *~ "Baker Street"

It reads better, from left to right with a subject in the first position, but I think using custom operators is going a little bit too far.  I worry they will discourage people who are not used to functional programming style.

Now, I really like `|>`, the application operator.  I really, *really* like it.  There are many situations where it makes code much more readable.  It allows to rewrite `g(f(x))` as `x |> f |> g`, which can be extremely useful, depending on the importance, number, and actual names of your `f`s and `g`s.  I shipped an iPad game called [Glitchy Checkers][] where I used this operator 191 times.  (Mostly because of my [tweaks][] system, but not exclusively.  I used Rob Rix' implementation from [Prelude][].)

  [Glitchy Checkers]: http://GlitchyCheckers.com/
  [Prelude]: https://github.com/robrix/Prelude
  [tweaks]: /posts/checkers-development-panel

So, I am not against custom operators.  However, they introduce a significant cost: their "names" usually consist of only one or two characters, which convey almost no information by themselves.  Therefore, they have to be memorized by members of the team.  If I am to pay such a price, I prefer operators to be useful in more than one context.  Most importantly though, I want the resulting API to be better with custom operators than it is possible without them.

In the above example I think this is not the case, as there is boilerplate involved in combining lenses and finding them in their namespaces.  I think this can be improved.

I wanted an API where an object is in the first place and where I don't have to repeat the word "lens".  I wanted the address lens to somehow know that it can be followed by a street lens.  Given that we already use a code generator, something like this should be possible, I thought:

    let author2 = author.throughLens.address.street.set("Baker Street")

Enter *bound lenses*.


Bound lenses
------------

Bound lenses are lenses that are already "used half way".  They already have a `Whole` instance associated with them.  This allows for a much nicer, more familiar syntax:

    let author3 = author.throughLens.name.set("narf")

instead of

    let author3 = Person.Lenses.name.set("narf", author)

Furthermore, I defined [`BoundLensType`](https://github.com/narfdotpl/lenso/blob/deb4620f3cb6cbd98891ef7500966dadafc0bbd4/example/example.playground/Contents.swift#L51-L93) as a protocol.  Bound lenses are required to have `get` and `set` methods, but they can also have custom properties.  For example, [`BoundLensToPerson`](https://github.com/narfdotpl/lenso/blob/deb4620f3cb6cbd98891ef7500966dadafc0bbd4/example/example.playground/Contents.swift#L130-L141) has properties `name` and `address`, which are also bound lenses.

Details of this don't make for an incredibly interesting blog post, but
I encourage you to have a look at the [code generated by Lenso](https://github.com/narfdotpl/lenso/blob/deb4620f3cb6cbd98891ef7500966dadafc0bbd4/example/example.playground/Contents.swift#L128-L163).  It allows access to properties further down the object chain, without having to manually compose lenses:

    let author2 = author.throughLens.address.street.set("Baker Street")

I think this is a big win and it makes working with immutable objects easier.


Code generation
---------------

The entire lenses API that I described would require writing a whole lot of boilerplate if it wasn't for code generation.  Having to rely on external software, though, is a huge obstacle on the road to adopting this solution in a "real world" project.  Unfortunately, I don't know how to achieve similar results (including code completion and type safety) without creating custom code for objects that are going to be used.

Currently, my code generator requires models to be specified in a JSON
format:

    {
      "models": [
        {
          "name": "Person",
          "properties": [
            {"name": "name", "type": "String"},
            {"name": "address", "type": "Address"}
          ]
        },
        {
          "name": "Address",
          "properties": [
            {"name": "street", "type": "String"}
          ]
        }
      ]
    }

This is far from ideal, but good enough for an experiment.  In the future I would love to be able to inspect source files and generate lenses without extra configuration.


Further reading
---------------

If you want to learn more about lenses or more about immutable objects in general, I recommend these resources:

- [Lenses in Swift][talk] talk by Brandon Williams
- [Lenses in Swift](http://chris.eidhof.nl/posts/lenses-in-swift.html) post by Chris Eidhof
- [A Warm Welcome to Structs and Value Types](https://www.objc.io/issues/16-swift/swift-classes-vs-structs/) by Andy Matuschak

Also, check out [Lenso][], my framework/generator.  The part that will probably interest you the most is the [example playground](https://github.com/narfdotpl/lenso/tree/master/example).

Happy lensing!

<br/>
*Follow me on [Twitter](https://twitter.com/narfdotpl/status/686912983969173504) and discuss this post on [Reddit](https://www.reddit.com/r/swift/comments/40mjpw/lenses_in_swift_or_how_to_change_parts_of/).*

*Thanks to Arek Holko for reading drafts of this.*
