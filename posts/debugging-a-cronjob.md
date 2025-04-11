---
author: admin
categories:
- Technical
date: 2025-04-11
tags:
- debugging
- war story
title: 'Debugging a cronjob'
---

Join me, and learn about how to debug cron jobs, as well as a little about `env` and `strace`.

---

I have a cronjob on my desktop which plays audible reminders for me of various events. For example, my wakeup alarm is:

```
#minute hour  day of month  month  day of week  user     command
0       10    *             *      *            zachary  chronic notify --here "alarm time. wake up"
```

Every morning, [notify](https://github.com/za3k/short-programs?tab=readme-ov-file#notify) speaks aloud "Alarm time. Wake up.". It speaks on my laptop... and then my laptop again... and finally my desktop. It's not supposed to do the laptop step twice. It should speak two times, not three. It's just one of those small things that niggle at you over time.

In fact, I run on my desktop manually:

```
chronic notify --here "Alarm time. Wake up"
```

And... it plays on my laptop... then my desktop. Two times. That's what it's supposed to do. Um, what gives?

I do my usual trick to re-create the (kind of weird) cron environment:

```
#minute hour  day of month  month  day of week  user     command
*       *     *             *      *            zachary  env > /tmp/cronenv
0       10    *             *      *            zachary  chronic notify --here "alarm time. wake up"
```

I wait a minute, and read /tmp/cronenv. Yep, looks good.

```
SHELL=/bin/sh
PWD=/home/zachary
LOGNAME=zachary
HOME=/home/zachary
LANG=en_US.UTF-8
USER=zachary
SHLVL=1
MAILTO=za3k@za3k.com
PATH=/usr/local/sbin:/usr/local/bin:/usr/bin
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
_=/usr/bin/env
```

I turn that back off, and run again, using the cron environment.

```
env -i $(cat /tmp/cronenv) chronic notify --here "Remember to do review" # 3 times
```

Okay, that speaks three times. Problem reproduced.

Incidentally, I found something interesting reading the man page to `env`. As you may or may not be aware, shebang lines at the top of a program execute the script listed there:

```
#!/bin/python

import os
...
```

when run as an executable, is the same as calling

```
/bin/python <path/to/script.py>
```

And

```
#!/bin/python -i
```

(which runs the script, then lets you interactively look at variables) is the same as

```
/bin/python -i <path/to/script.py>
```

Incidentally, the `/bin/` is optional -- you can just use `python`. But it's better for security to use full paths.

So far, so good. But what about

```
#!/bin/python -i -q
```

Nope. It prints the confusing:

```
Unknown option: -
usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
Try `python -h' for more information.
```

Why? That's actually the output of `python "-i -q" <path/to/script.py>`. Why does python print this message? It's trying to parse short-form options (`-abcd` as `-a -b -c -d`) and it sees the second short-form option is a space. It's... not the best error message, certainly ([#132414](https://github.com/python/cpython/issues/132414)).

Going back to our original digression, the point is that shebang lines can contain zero one or arguments to their command-line program, but not more.

`env -S` is a neat little option that fixes this:

```
#!/bin/env -S /bin/python -i -q
```

Huh, you learn something new every day. Anyway, back to that alarm clock. What's going on? Well, let's bisect.

```
env >normalenv
```

Give us a long, long list of environment variables. I delete two that I can't figure out how to get to work correctly because of spaces:

```
RPROMPT=%(?,%F{green}:%),%F{yellow}%? %F{red}:()%f
PS1=%m:%1~ $
```

and run:

```
env -i $(cat normalenv) chronic notify --here "Remember to do review" # 2 times
env -i $(cat cronenv)   chronic notify --here "Remember to do review" # 3 times
```

OK! That works. So I have a working case, and a non-working case, and the only different are the two env files. This should be straightforward, if tedious, from here on out.

I delete a few lines... still works. Those lines didn't matter. Delete a few more... works, those lines weren't important. Delete a few more... it breaks now. Guess one of those was important. I'll return to that section later, restore it for now. Delete a few more... those didn't matter.

At the end of the day, only one line mattered. I can reproduce with a one-line environment file.

```
PATH=/home/zachary/.opam/default/bin:/home/zachary/.opam/default/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/cuda/bin:/opt/cuda/nsight_compute:/opt/cuda/nsight_systems/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/usr/lib/rustup/bin:/opt/android-sdk/tools/adbfs:/home/zachary/.cabal/bin:/opt/clojurescript/bin:/opt/miniconda3/bin/:/usr/share/fslint/fslint:/home/zachary/games/factorio/bin/x64:/home/zachary/.local/bin:/home/zachary/.bin:/home/zachary/script:/var/local/media-player:/home/zachary/.projects/short-programs/:/home/zachary/.xmonad:/opt/android-sdk/tools/adbfs:/home/zachary/.cabal/bin:/opt/clojurescript/bin:/opt/miniconda3/bin/:/usr/share/fslint/fslint:/home/zachary/games/factorio/bin/x64:/home/zachary/.local/bin:/home/zachary/.bin:/home/zachary/script:/var/local/media-player:/home/zachary/.projects/short-programs/:/home/zachary/.xmonad
```

Yeah, yeah. I have a gross PATH. There are bigger things in life.

OK, so... hmm. What's going on. Am I calling an external program inside of `notify`? Let's strace it.

**strace** is a tool which shows all system calls a program makes. I could read my code carefully... or I could just print what it does. I trust the latter more (and if you didn't write the program, it's handy).

```
juice:~ $ env -i $(cat normalenv) strace --silence=attach,exit -f -e trace=execve notify --here "Remember to do review" 2>&1 | grep -v SIGCHLD | tee correct.log

execve("/usr/bin/notify", ["notify", "--here", "Remember to do review"], 0x7fff82957da0 /* 1 var */) = 0
[pid 512920] execve("/usr/bin/which", ["which", "sendmail"], 0x616259d51d30 /* 4 vars */) = 0
[pid 512921] execve("/usr/bin/id", ["id", "-u"], 0x616259d53920 /* 4 vars */) = 0

[... many more lines ... ]

[pid 512949] execve("/home/zachary/.opam/default/bin/speak", ["speak", "Remember to do review"], 0x59833be8ac40 /* 6 vars */) = -1 ENOENT (No such file or directory)
[pid 512949] execve("/usr/local/sbin/speak", ["speak", "Remember to do review"], 0x59833be8ac40 /* 6 vars */) = -1 ENOENT (No such file or directory)
[pid 512949] execve("/usr/local/bin/speak", ["speak", "Remember to do review"], 0x59833be8ac40 /* 6 vars */) = -1 ENOENT (No such file or directory)
[pid 512949] execve("/usr/bin/speak", ["speak", "Remember to do review"], 0x59833be8ac40 /* 6 vars */) = 0

juice:~ $ env -i $(cat cronenv) strace --silence=attach,exit -f -e trace=execve notify --here "Remember to do review" 2>&1 | grep -v SIGCHLD >incorrect.log
```

OK, so we have the correct and incorrect calls. We diff them, and the difference is... everything. Whoops, because we have all kinds of raw pointers and process numbers. Hmm, how do other people do this?

Googling it... it's not a super solved problem. I'll just replace all the numbers by question marks.

```
for f in correct.log incorrect.log; do
  sed -r -E 's/^(.+)pid [0-9]+(.+)$/\1pid-xxxx\2/;s/0x[0-9a-f]{12}/0x????????????/;s/[0-9]+ vars?/? vars/;' -i $f
done
diff correct.log incorrect.log
```

And we see something I should have already spotted:

```
> /usr/bin/notify: line 75: beepz: command not found
```

If I had just run the program outside of `chronic`, I would have seen this output already. Oops. Hindsight is 20-20.

Aha. So beepz is not in the cron path. 

```
juice:~ $ env -i $(cat cronenv) beepz
env: ‘beepz’: No such file or directory
```

We'll add it to the path. Done. Uh oh, beepz still doesn't work. What else do we need? I pull the environment bisecting trick again, and add to cron:

```
XDG_RUNTIME_DIR=/run/user/1000
PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/home/zachary/.projects/short-programs
```

And a quick test confirms I get one wakeup alarm per computer now, just as I like it.

As a last step, why did it break? Well, I know the answer to that one. I used to install all the programs from `~/.projects/short-programs` to `/bin`. But when I was working on developing the programs, the two would get out of sync, so I deleted the system versions. Guess it broke something. Oops.
