---
author: admin
categories:
- Technical
date: 2015-12-05 19:25:52-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- backup
- bash
- linux
- sysadmin
title: Archiving all bash commands typed
updated: 2015-12-05 19:25:52-07:00
wordpress_id: 391
wordpress_slug: archiving-all-bash-commands-typed
---
This one’s a quickie. Just a second of my config to record all bash commands to a file (.bash\_eternal\_history) forever. The default bash HISTFILESIZE is 500. Setting it to a non-numeric value will make the history file grow forever (although not your actual history size, which is controlled by HISTSIZE).

I do this in addition:

```
#~/.bash.d/eternal-history
# don't put duplicate lines in the history
HISTCONTROL=ignoredups
# append to the history file, don't overwrite it
shopt -s histappend
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTFILESIZE=infinite
# Creates an eternal bash log in the form
# PID USER INDEX TIMESTAMP COMMAND
export HISTTIMEFORMAT="%s "

PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND ; }"'echo $$ $USER \
"$(history 1)" >> ~/.bash_eternal_history'
```
