date: 2022-06-09
collections: [setup]
description: What I install, and in what order, to feel at home.

Mac software: 2022
==================

*[updated][] in the spring of 2024*

  [updated]: https://github.com/narfdotpl/narf.pl/commit/0bdf6a7100fd9ed239ec56d15e65c882be330751c

In May I've set up three different Macs (don't ask) starting from a clean
latest macOS installation. Here's what I do and install, and in what order,
to feel at home:

1. update the OS
1. if this is a laptop, enable "tap to click" in trackpad settings
1. if this is a laptop, enable Touch ID
1. [Things](https://culturedcode.com/things/)
1. [Spotify](https://www.spotify.com/us/download/mac/)
1. [SteerMouse](https://plentycom.jp/en/steermouse/download.php)
    - configure [buttons](steermouse/buttons.png)
    - configure [sensitivity](steermouse/sensitivity.png)
    - enter license
1. tweak macOS settings
    - remove everything from the dock
    - download [wallpaper](/static/assets/pixel-sorting/wallpaper/flipped.jpg) from the [pixel sorting](/posts/pixel-sorting) post
    - configure dock and menu bar
        - [dock](macos/dock.png)
        - [clock](macos/clock.png)
        - [spotlight](macos/spotlight.png)
    - disable [autocorrection](macos/keyboard.png)
    - configure [spaces](macos/spaces.png)
    - configure [hot corners](macos/hot-corners.png)
    - add Stage Manager shortcut in keyboard shortcuts
    - disable "click wallpaper to reveal desktop"
    - configure Finder
    - configure Safari:
        - [general](safari/general.png)
        - [tabs](safari/tabs.png)
        - [advanced](safari/advanced.png)
        - search -- DuckDuckGo
    - open a video call, click on the camera button in the menu bar, and disable reactions
1. [Fira Code](https://github.com/tonsky/FiraCode/wiki/Installing)
1. [MacVim](https://macvim-dev.github.io/macvim/)
1. [iTerm](https://iterm2.com/)
1. copy `~/.zsh_history` from another Mac
1. generate a [new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
    - go through "configure SSO" for this key on GitHub
1. [Homebrew](https://brew.sh)
1. copy Quake 3 sounds (used in git aliases) from another Mac
1. [dotfiles](https://github.com/narfdotpl/dotfiles)
    - configure [iTerm](iterm.png)
1. [Hammerspoon](https://www.hammerspoon.org)
1. [Visual Studio Code](https://code.visualstudio.com)
    - ⇧⌘P sync settings using GitHub
1. [VLC](https://www.videolan.org/vlc/)
1. Xcode
    - [general](xcode/general.png)
    - [text editing](xcode/text-editing.png)
    - install [One Dark theme](https://github.com/bojan/xcode-one-dark)
    - increase the font size to 20
    - change the background color to be the same as in MacVim and VS Code
    - remove the "Print..." key binding
    - remap "Open Quickly..." to ⌘P
    - remove "Move Paragraph Backward/Forward"
    - remap "Move Line Up/Down (Source Code)" to ⌥↑, ⌥↓
    - remove "Duplicate"
    - remap "Show Debug Area" to ⌘D
    - enable Vim mode: help › search › "vim"
    - disable minimap: help › search › "minimap"

This is not a complete list of everything I use or tweak, but it's a solid
starting point that gets me 80–90% of the way there.
