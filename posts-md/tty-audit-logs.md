---
author: admin
categories:
- Technical
date: 2022-08-18 20:14:48-07:00
markup: html
source: wordpress
tags:
- archiving
- linux
- system administration
title: tty audit logs
updated: 2022-08-18 20:14:49-07:00
wordpress_id: 789
wordpress_slug: tty-audit-logs
---
I recently wrote a program that records all tty activity. That means bash sessions, ssh, raw tty access, screen and tmux sessions, the lot. I used [script](https://en.wikipedia.org/wiki/Script_\(Unix\)). The latest version of my software can be found [on github](https://github.com/za3k/short-programs#record-shell).

Note that it’s been tested only with bash so far, and there’s no encryption built in.

To just record all shell commands typed, use the standard eternal history tricks ([bash](https://github.com/za3k/dotfiles/blob/master/.bashrc)).
