---
author: admin
categories:
- Technical
date: 2015-03-12 19:09:37-07:00
markup: html
source: wordpress
tags:
- command-line
- ide
- lightweight
- linux
- screen
- tmux
- unix
title: Screen and Tmux IDEs
updated: 2015-03-12 19:09:37-07:00
wordpress_id: 98
wordpress_slug: screen-and-tmux-ides
---
I don’t usually like IDEs. They’re hard to switch off of, they do too much. They don’t let me customize things, and I always have to use external tools anyway. I’d really rather do things with a bunch of small tools, the linux way. The problem is, if I close everything, I’ll have trouble getting started back up again. Saving state is one solution. Quick start-up is another. Basically, write a checklist for myself to make starting things up easy (open such-and-such files in the editor, start the server in debug mode, etc).

But we’re programmers, so obviously we’re not going to use a literal checklist. Instead, we’re going to write a little script to auto-start things in a new screen session:

```
#!/usr/bin/screen -c
# game_development.screen.conf
# Run stand-alone or with screen -c game_devel.screen.conf
screen -t "Vim" 2 bash -c "vim -p *.t"
bind "r" screen -t "Game" 2 bash run.sh
```

Or if you prefer tmux:

```
# game_development.tmux.conf
# Run with tmux -f game_development.tmux.conf attach
new-session -s game_development
new-window -n "Vim" "bash -c 'vim -p *.t'"
bind r new-window -n "Game" "bash run.sh"
```

Note the main features being used: a shebang line hack for screen, to let this file be self-contained and executable. Opening files in vim in place of a text editor. Binding keys for unit tests, running the program, restarting the server, etc. Now, a similar approach is to add new key bindings to the text editor, but I feel like text editors should edit text, and I like being able to document all the additions with help menus (which screen and tmux both support).

Note: [ratpoison](http://www.nongnu.org/ratpoison/) is similar to screen/tmux so you can do similar things in X.

One thing I’d love is if this kind of file was easy to dump from the current state, especially for things like positioning windows, etc. A little assistance is available, but not too much. Ratpoison and tmux let you dump sizing information. Nothing outputs keybindings or a list of running programs with their windows.

There **is** a program called [tmuxinator](https://github.com/tmuxinator/tmuxinator) to let you write the same config in nested [YAML](http://yaml.org/) of sessions, panes, and windows, which might appeal to some users.

Also, check out [dtach](http://dtach.sourceforge.net/) if you don’t need panes and windows, and just want a detachable process.
