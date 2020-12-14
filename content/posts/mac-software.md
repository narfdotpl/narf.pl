date: 2016-01-31
collection: Setup series

Mac software
============

Hello and welcome to the second episode of My New Computer!
Previously [I was complaining][iMac] about how great the new iMac is.
This week I'm going to list All The Great Apps that make it better.

  [iMac]: /posts/5k-imac

I'll begin by saying that when I got the new computer, I started from a
fresh OS X El Capitan installation and I didn't use any migration tools.
When setting everything up, I took notes about what software I was
installing.  I grouped apps into a few sections and ordered them in
[Maslow's][Maslow] fashion.  First up: "the core OS stuff".

  [Maslow]: https://en.wikipedia.org/wiki/Maslow%27s_hierarchy_of_needs


System augmentation
-------------------

[f.lux][].  Now, if you don't use any of the apps I list here,
installing f.lux is arguably the best thing you can do for yourself.
What this app does is it basically makes your screen orange at night, which
makes it much easier to look at.  It should also be easier for you to fall
asleep when you finally get to bed.  (À&nbsp;propos: iOS 9.3 will introduce
a f.lux-like feature called Night Shift.  Until then, I use [GammaThingy][]
on iOS 9.2.)

  [f.lux]: https://justgetflux.com/
  [GammaThingy]: https://github.com/thomasfinch/GammaThingy

If making the screen orange sounds ridiculous to you, I dare you to test it:
install f.lux at night, activate it for one minute, and then turn it off.
Don't send me "thank you" emails.  You're welcome.

![](flux.png)


[SteerMouse][].  I use SteerMouse to disable mouse acceleration (which
is super annoying when you're playing, say, [Quake&nbsp;3](/posts/cpma)) and
to assign useful functions to "extra" buttons of my mouse.  I have a
Logitech G400 and I use thumb buttons to switch between spaces.

  [SteerMouse]: http://plentycom.jp/en/steermouse/

![](mouse.jpg)


[Karabiner][] and [Seil][] govern my custom keyboard mappings.  This is
a topic for a whole other post (TODO: blog about custom keyboard mappings),
but I can give you a taste by saying that I often hold caps lock down with
my left pinky, or that the space bar on my keyboard acts as shift.

  [Karabiner]: https://pqrs.org/osx/karabiner/
  [Seil]: https://pqrs.org/osx/karabiner/seil.html.en


[Slate][] is the window manager I use.  I can't really recommend it as
it's unmaintained and uses [JavaScript configs][Slate config].  But it
still works, so I still use it.

  [Slate]: https://github.com/jigish/slate
  [Slate config]: https://github.com/narfdotpl/dotfiles/blob/9cf8d929609d81766f82aaef7c1a87c77479d749/home/.slate.coffee


[MenuMeters][] sit in my [menu bar](/posts/menu-bar) and let me know if
something is using network or CPU.  It's useful in cases where apps don't
provide appropriate amount of feedback themselves.

  [MenuMeters]: http://www.ragingmenace.com/software/menumeters/


[Bartender][] is a piece of software that I used to run, but on this
computer it has some issue with a license.  More importantly though, on El
Cap it's possible to hide the menu bar altogether, so I don't really need
Bartender to hide what's already hidden.  (TODO: blog about the [faux full
screen mode](https://twitter.com/narfdotpl/status/670211461059354624).)

  [Bartender]: https://www.macbartender.com/



Consumption
-----------

[Chrome][].  Nuff' said.  I use Google's browser with three extensions:

  [Chrome]: https://www.google.com/chrome/browser/desktop/

- [Ghostery](https://chrome.google.com/webstore/detail/ghostery/mlomiejdfkolichcflejclcbmpeaniij),
- [Instapaper](https://chrome.google.com/webstore/detail/instapaper/ldjkgaaoikpmhmkelcgkgacicjfbofhh),
- and [Google Dictionary](https://chrome.google.com/webstore/detail/google-dictionary-by-goog/mgijmajocgfcbeboacabfgobmjgjcoja).


[Spotify][].  I listen to [a lot of music](/posts/music-streaming) on
Spotify.

  [Spotify]: https://www.spotify.com/pl/


[VLC][] is the video player I use.  It can deal with files in virtually
any video format.

  [VLC]: http://www.videolan.org/vlc/download-macosx.html


[uTorrent][] is useful when one wants to download Ubuntu.  (uBuntu?)

  [uTorrent]: http://www.utorrent.com/


Communication
-------------

[Messenger][].  When I chat with my favourite humans, it's usually over
Facebook.  There is an official Messenger.com website that is wrapped by
this nice app that I use.  I even have a [fork][] where I fixed switching
between tabs with ⌘1...9.

  [Messenger]: https://github.com/rsms/fb-mac-messenger/releases
  [fork]: https://github.com/narfdotpl/fb-mac-messenger/tree/fix-command-number-switching


[Slack][].  Slack is eating the world.

  [Slack]: https://slack.com/


Productivity
------------

[Dropbox][] might [not be sexy anymore][Dropbox on The Verge], but
it's still a fairly reliable way to quickly move files between my  iOS
devices and OS X.

  [Dropbox]: https://www.dropbox.com/
  [Dropbox on The Verge]: http://www.theverge.com/2015/9/22/9372563/dropbox-really-is-a-feature


[iA Writer Classic][] is the text editor that I use when I need to sync
text with my iPhone.  2016-06-02 update: a few weeks ago I removed iA
Writer and switched to [Editorial][] on iOS.  It's very impressive.  I
use MacVim on my Mac and sync notes via Dropbox.  The sync seems faster,
provides visual feedback (a tiny spinner is better than nothing), and
can be triggered manually.  Overall, Editorial is a better app and
Dropbox is more reliable and less frustrating than iCloud.

  [iA Writer Classic]: https://itunes.apple.com/bf/app/ia-writer-classic/id439623248?mt=12
  [Editorial]: http://omz-software.com/editorial/


[Clear][] is the to-do app that I still use from time to time, even though
I have moved "the serious stuff" to [OmniFocus][] for iOS.

  [Clear]: https://www.realmacsoftware.com/clear/
  [OmniFocus]: https://www.omnigroup.com/omnifocus


[Skitch][] is Good Enough™ when I want to add an arrow to a screen shot.

  [Skitch]: https://evernote.com/skitch/


[Pixelmator][], on the other hand, is good enough when I want to do
something more advanced, like edit a selfie:

  [Pixelmator]: http://www.pixelmator.com/mac/

![](selfie.jpg)


[iTerm][] replaced Terminal for me so long ago that I don't remember the
reasons anymore.  I use it with the [Solarized Dark][iTerm Solarized]
theme.

  [iTerm]: https://www.iterm2.com/
  [iTerm Solarized]: https://github.com/altercation/solarized/blob/master/iterm2-colors-solarized/Solarized%20Dark.itermcolors


[Dotfiles][], which I keep public on GitHub, shape my command line
experience.  I also use various CLI apps installed via [Homebrew][].
Shell history search is a feature that I rely heavily upon (I have it mapped
to the up and down arrows).  One lifehack I can share that relates to this is
copying the `~/.zsh_history` file over from the old computer.  Nothing makes
the new machine feel more like home.

  [Dotfiles]: https://github.com/narfdotpl/dotfiles
  [Homebrew]: http://brew.sh/


[MacVim][] is my text editor of choice for everything apart from iOS
development and an occasional note in iA Writer.

  [MacVim]: http://macvim-dev.github.io/macvim/


[Xcode][] is the IDE I use for iOS development.  I [download it
manually][Xcode download] from the Developer Portal because automatic Mac
App Store updates can be disruptive, e.g. when a new Xcode version introduces
a new backwards-incompatible version of Swift, which I can't adopt right away
because I have to wait for my dependencies to be updated first.  In
Xcode, I also use [Solarized Dark][Xcode Solarized].  In fact, I like
Solarized Dark so much that I made an [iPad game][Glitchy Checkers] that
uses it.  Apart from this theme, I use two other plugins: [XVim][], which
saves my sanity, and [Fuzzy Autocomplete][], which soon will be made
redundant by a built-in feature of Xcode 7.3.

  [Xcode]: https://developer.apple.com/xcode/
  [Xcode download]: https://developer.apple.com/downloads/
  [Xcode Solarized]: https://github.com/ArtSabintsev/Solarized-Dark-for-Xcode
  [Glitchy Checkers]: /checkers
  [XVim]: https://github.com/XVimProject/XVim
  [Fuzzy Autocomplete]: https://github.com/FuzzyAutocomplete/FuzzyAutocompletePlugin


Gaming
------

The 5k iMac is capable of running games, so I have [Steam][] installed.
I play some of them with a wireless Xbox 360 controller.  Unfortunately,
the controller doesn't work with OS X out-of-the box.  To make it work, one
has to install a kernel extension (the horror!).  For that I use
[360Controller 0.14][360Controller], which, at the moment of writing, is
their latest non-beta release available on GitHub.

To my not-that-great sadness, after turning the controller on, it
very often doesn't register as player one.  Surprisingly, this doesn't
affect its ability to control games, but has annoying consequences of
force feedback not working and player selection lights blinking on the
controller.

  [Steam]: http://store.steampowered.com/
  [360Controller]: https://github.com/360Controller/360Controller/releases

Rebooting the Mac fixes the problem.
¯\\\_(ツ)\_/¯


That's all Folks!
-----------------

This sums up my list of Mac apps.  Let me know on [Twitter][] if you have
any app recommendations.  See you next time, in another hilarious
installment of My New Computer!

  [Twitter]: https://twitter.com/narfdotpl/status/693740837923061760
