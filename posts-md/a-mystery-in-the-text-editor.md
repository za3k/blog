---
author: admin
categories:
- Technical
date: 2024-05-12 19:59:50-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- command-line
- linux
title: A mystery in the text editor
updated: 2024-05-13 12:49:32-07:00
wordpress_id: 1351
wordpress_slug: a-mystery-in-the-text-editor
---
Hello, Linux terminal users! Let me present you a simple feature you’ve all seen, but might not have noticed.

[![](https://blog.za3k.com/wp-content/uploads/2024/05/01-mystery.png)](https://blog.za3k.com/wp-content/uploads/2024/05/01-mystery.png)

You’re on the terminal, and you open a text editor of chice–nano, vim, emacs, acme etc.

[![](https://blog.za3k.com/wp-content/uploads/2024/05/02-mystery.png)](https://blog.za3k.com/wp-content/uploads/2024/05/02-mystery.png)

After you edit for a bit, you close the editor.

[![](https://blog.za3k.com/wp-content/uploads/2024/05/03-mystery.png)](https://blog.za3k.com/wp-content/uploads/2024/05/03-mystery.png)

Now you’re back where you left off. My question is, *how?* How does nano remember what used to be on screen? How does it get restored? Is nano doing this, or bash?

Well, I took at look at the [source code](https://github.com/madnight/nano/blob/master/src/nano.c) to *nano*. Then I thought, “whoa! that’s way too complicated.” So I found a much simpler project called *ted* someone made to educate themselves. That was [also](https://github.com/madnight/nano/blob/master/src/nano.c) a little complicated, but both seemed to use ncurses. So I wrote the following simple program, which *also* displays something and then restores the screen. Even though it’s very simple, it still works.

```
// Compile with: gcc -lncurses editor.c -o editor

#include <curses.h>
#include <stdio.h>

int main(int argc, char **argv) {
    initscr();

    refresh();
    printw("Hello world");
    getch();

    endwin();
    return 0;
}
```

Aha, so it’s something in ncurses, maybe. Let’s dive deeper.

So *initscr()* presumably saves the state in some fashion. *endwin()* definitely restores it, because if we comment that out, the terminal stops being restored. Since *initscr()* probably does lots of other irrelevant logic, we could take a look at *endwin()* to dive in. But let’s do something even simpler first.

As background, the linux command line is pretending to be an obsolete piece of hardware called a [terminal](https://en.wikipedia.org/wiki/Computer_terminal). Specifically, it’s pretending to be a model called the DEC VT100 (or a later one, but they’re mostly backwards compatible). The terminal accepted text over a wire, and printed it to the screen.

When it got special text, it would do special things. These are captured today as “escape codes”–special non-printable characters, which cause your software terminal to also do special things. What kind of special things? Well one example escape code is “Backspace”, which deletes the last character. Another code is “\\r\\n” (carriage return; new line), which goes to the beginning of the line, and down one.

I suspect the answer to what’s happening with save and restore of my terminal might be some magic escape codes. So let’s just redirect the output to a file, and see what data is being center over the virtual wire to our virtual terminal.

```
$ ./editor >magic.txt
$ xxd < magic.txt
00000000: 1b28 421b 2930 1b5b 3f31 3034 3968 1b5b  .(B.)0.[?1049h.[
00000010: 313b 3530 721b 5b6d 0f1b 5b34 6c1b 5b48  1;50r.[m..[4l.[H
00000020: 1b5b 4a48 656c 6c6f 2077 6f72 6c64 6a1b  .[JHello worldj.
00000030: 5b35 303b 3148 1b5b 3f31 3034 396c 0d1b  [50;1H.[?1049l..
00000040: 5b3f 316c 1b3e                           [?1l.>
```

Well, that’s certainly a bunch of magic. Now something cool happens:

```
$ cat magic.txt
```

This command does *nothing visible*. It doesn’t print “Hello world”, even though that’s in the file. In other words, it’s printing Hello world, then really quick resetting the terminal. Just too fast for my poor human eyes to see.

We’ve confirmed the escape code theory! This file has everything we need. We can look at the source code to ncurses if we’re curious, but we don’t need to (and I won’t).

One thing I immediately see in this file, is that it *doesn’t* seem to contain the words that were on screen. So it’s not that the program read what was on screen, and printed it back later. Rather, there are some magic escape sequences happening to save and restore the terminal.

Okay, so somewhere in those 70 bytes is a magic code or two we want. Let’s examine all the bytes.

What kinds of escape codes appear here? Hex **0x1b** is ESC, basically *the* escape sequence–it cues the terminal in that a special escape code is coming. **0x1b9b** ( **ESC** followed by **\[** )is the CSI escape code. [DEC private codes](https://en.wikipedia.org/wiki/VT100) refer to other escape sequences used by the DEC terminals like the VT00 (I’ll just shorten this to “DEC” below).

Without further ado, let’s break down those 70 bytes. Apologies for any errors below–correct me in the comments.

-   **0x1b** (B
    -   Set first character set to US ASCII \[[xterm DEC guide](https://www.xfree86.org/current/ctlseqs.html)\]
-   **0x1b** )0
    -   Set second character set to “DEC Special Character and Line Drawing Set” \[[xterm DEC guide](https://www.xfree86.org/current/ctlseqs.html)\]
-   **0x1b9b** ?1049h
    -   **Save cursor as in DECSC and use Alternate Screen Buffer, clearing it first.** \[[xterm CSI guide](https://www.xfree86.org/current/ctlseqs.html)\]
-   ****0x1b**9b** 1;49r
    -   DECSTBM: Set scrolling region to rows 1-49 \[[xterm CSI guide](https://www.xfree86.org/current/ctlseqs.html)\]  
        (When I ran the program, my terminal was 49 lines tall inside tmux–so the whole terminal in other words.)
-   **0x1b9b** m
    -   (Empty) color and style set comand \[[ANSI/CSI](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)\]  
        I think this could be left out entirely.
-   **0x0f (Ctrl-O)**
    -   Shift In. Use the standard character set. \[[xterm](https://www.xfree86.org/current/ctlseqs.html)\]
-   **0x1b9b** 4l
    -   RM: Replace Mode / IRM \[[xterm CSI guide](https://www.xfree86.org/current/ctlseqs.html)\]  
        Typing doesn’t shift everything over, it writes over existing content.
-   **0x1b9b** H
    -   Move the cursor to “home” (top left of the screen) \[[ANSI/CSI](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)\]
-   **0x1b9b** J
    -   Clear the screen \[[ANSI/CSI](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)\]
-   Hello worldj
    -   The program prints “Hello world”. The final j was echoed when I pressed “j” to exit.
-   **0x1b9b** 49;1H
    -   Move the cursor to line 49, column 1 — the bottom-left corner \[[ANSI/CSI](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)\]
-   **0x1b9b** ?1049l
    -   **Use Normal Screen Buffer and restore cursor as in DECRC** \[[xterm CSI guide](https://www.xfree86.org/current/ctlseqs.html)\]
-   **0x0d (\\r or Ctrl-M)**
    -   Carriage return \[[xterm](https://www.xfree86.org/current/ctlseqs.html)\]  
        Moves cursor to column 0
-   ****0x1b**9b** ?1l
    -   DECCKM reset: Re-enables the cursor? \[[VT100](https://vt100.net/docs/vt220-rm/chapter4.html#S4.6.18)\]
-   **0x1b** \>
    -   DECONM: Normal Keypad \[[xterm DEC guide](https://www.xfree86.org/current/ctlseqs.html), [VT100](https://vt100.net/docs/vt220-rm/chapter4.html#S4.6.18)\]

OK, solved. The magic save bytes are **1b 9b 3f 31 30 34 39 68** (<ESC> \[?1049h). The magic restore bytes are **1b 9b 3f 31 30 34 39 6c** (<ESC> \[?1049l). And xterm or tmux is doing the save/restore magic, based on seeing this escape mode.

Hmm, how minimal can we get a working file, I wonder?

```
#!/bin/sh
echo -ne '\x1b[?1049h' # Save terminal
echo -ne '\x1b[H'      # Home the cursor
echo "Hello world"
sleep 1
echo -ne '\x1b[?1049l' # Restore terminal
```

Yep. That works fine.

ANSI: [https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)  
DEC: [https://vt100.net/emu/ctrlseq\_dec.html](https://vt100.net/emu/ctrlseq_dec.html)  
DEC: [https://vt100.net/docs/vt220-rm/chapter4.html#S4.6.18](https://vt100.net/docs/vt220-rm/chapter4.html#S4.6.18)  
xterm’s control sequences: [https://www.xfree86.org/current/ctlseqs.html](https://www.xfree86.org/current/ctlseqs.html)
