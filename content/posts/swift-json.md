2015-03-01

Swift + JSON
============

Abstract
--------

I deal with JSON deserialization in Swift in a moderately elegant
way, without <strike>polluting codebase with</strike> introducing new
operators and initializers.


Context
-------

This is a short, written hastily on a train, post on a topic that many
have written about.  I wrote it in response to Radek Pietruszewski's
article ["Rethinking JSON in Swift"][radex].  I encourage you to read
Radek's post for more introduction.

  [radex]: http://radex.io/swift/json/


Protocol
--------

In my [checkers game](/checkers) I use JSON to save and load game state.
I use [SwiftyJSON][] to deal with JSON parsing.  On "my side" I
implement `JSONConvertible` protocol:

  [SwiftyJSON]: https://github.com/SwiftyJSON/SwiftyJSON

    protocol JSONConvertible {
        func toJSON() -> JSON
        static func fromJSON(json: JSON) -> Self?
    }


Swift 1.1
---------

In the old days of Swift 1.1, to implement the protocol, I was using
[`unwrapped`][unwrapped] -- an equivalent of Radek's `ensure`:

  [unwrapped]: https://github.com/narfdotpl/doodles/blob/master/doodles/unwrapped.swift

    struct Piece {
        let id: Int
        let player: Player
        let isCaptured: Bool
        let isKing: Bool
    }


    extension Piece: JSONConvertible {
        func toJSON() -> JSON {
            return JSON([
                "id": id,
                "player": player.toJSON().stringValue,
                "isCaptured": isCaptured,
                "isKing": isKing,
            ])
        }

        static func fromJSON(json: JSON) -> Piece? {
            return unwrapped(
                json["id"].int,
                Player.fromJSON(json["player"]),
                json["isCaptured"].bool,
                json["isKing"].bool
            ).map { (id, player, isCaptured, isKing) in
                // newlines added to fit in
                // my narrow blog layout
                Piece(id: id,
                      player: player,
                      isCaptured: captured,
                      isKing: king)
            }
        }
    }


Swift 1.2
---------

In Swift 1.2 I just use `if let` with multiple optionals:

    static func fromJSON(json: JSON) -> Piece? {
        if let id = json["id"].int,
               player = Player.fromJSON(json["player"]),
               isCaptured = json["isCaptured"].bool,
               isKing = json["isKing"].bool {
            return Piece(id: id,
                         player: player,
                         isCaptured: isCaptured,
                         isKing: isKing)
        } else {
            return nil
        }
    }


Advantages
----------

I like this approach because it doesn't involve any new operators while
still being readable -- there's not enough noise to justify removing it
at the cost of introducing new operators.

What I don't like is the fact that I had to type `id`, `player`,
`isCaptured`, and `isKing` three times there, but if I were to implement
a new initializer, I would have to type them this many times anyway.


Limitations
-----------

Because `fromJSON` returns `Self?`, it can be implemented "only" by
structs and final classes.  Using `JSONConvertible` with regular
classes results in `'MyClass' is not convertible to 'Self?'` error
as the compiler can't be sure that subclasses override `fromJSON` (your
class can be in a framework and then its subclasses are not known at
compile time).

For more discussion of this limitation, see Rob Napier's [answer to a
question about returning `Self`][rnapier].

  [rnapier]: http://stackoverflow.com/a/25645689/98763


Update &middot; 2015-03-02
--------------------------

ElvishJerricco [pointed out on Reddit][Reddit comment] that the final class
limitation mentioned above can be worked around by using a required
initializer that accepts `JSON` and returning it from `fromJSON`.
Unfortunately, such initializer can't be defined in an extension, which
destroys the elegance of the solution for me:

  [Reddit comment]: http://www.reddit.com/r/swift/comments/2xlkmy/swift_json_again/cp19x1h

    class MyClass {
        /* ... */
        required init?(json: JSON) { /* ... */ }
    }


    extension MyClass: JSONConvertible {
        func toJSON() -> JSON { /* ... */ }

        static func fromJSON(json: JSON) -> Self? {
            return self(json: json)
        }
    }

I don't have a good answer here, but if one has to use non-final classes
and add code to main class definitions, maybe a better solution is to
get rid of `fromJSON` altogether?

    protocol JSONConvertible {
        init?(json: JSON)
        func toJSON() -> JSON
    }


---

*You can discuss this post on [Reddit][] or message me on [Twitter][].*

  [Reddit]: http://www.reddit.com/r/swift/comments/2xlkmy/swift_json_again/
  [Twitter]: https://twitter.com/narfdotpl/status/572108946485473280
