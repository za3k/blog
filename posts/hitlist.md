---
author: admin
categories:
- Technical
date: 2025-04-04
tags:
- ocd
- time management
- dubious
title: 'hitlist'
---

I like to keep my home directory pretty small ideally. Just what I'm currently working on, plus maybe one or two permanent directories like `docs` or the like.
But, it accumulates! Just like a real desk, it gets covered in junk and needs cleaned off.

**hitlist** ([source](https://github.com/za3k/short-programs#hitlist)] is a small program I wrote today to make the process of cleaning it up more fun.

![caption: cleaning up my home directory](hitlist.png)

It functions similarly to the classic unix command `watch`. The idea is that you have a list of problems, and cross them off one by one.

- Cleaning up your home directory by running `hitlist -- ls ~`
- Complete your daily todo list with `hitlist -- grep '[ ]' ~/documents/TODO.txt`
- Fix a list of compilation errors with... okay, I haven't figured this one out yet. But it seems doable!

Unlike a real list, it "crosses off" problems for you, once they disappear from the command output, and lists how long you took to solve each one.

You could use this as a race. Or you could do some analysis after one run, and decide "actually, this took too long to fix--next time I'll give up on a bug if it takes more than 5 minutes to solve."

On-screen output is optionally saved to a file on exit.

![caption: cleaned up laptop homedir](hitlist-laptop-home.png)
![caption: desktop is even smaller](hitlist-desktop-home.png)
