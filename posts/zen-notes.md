---
author: admin
categories:
- Non-Technical
date: 2025-12-29
tags:
- ai did it
- programming
title: Zen Notes
---

I've been trying various challenges this month. Some more object-level, like "Learn Redstone". Some more meta-level, like "orient everything I do toward goals".

The first have been going pretty well. The second, not so much -- they start good, and I lose steam an hour or two in.

My working theory is that I'm not losing enthusiasm -- it's just easy to forget, and there's no specific deliberable I have in mind. I'm essentially working on a habit.

Yesterday's challenge was "constantly take notes". I decided to have Claude code me up a note-taking application, which is available [online here](https://tilde.za3k.com/notes/). It's a basic note-taking app, with all the usual stuff. Additionally, it's got an automatic "Zen Mode", meaning it hides all the menus and stuff when you're actually typing.

![caption: menus mode](zen-notes1.png)
![caption: typing/Zen mode](zen-notes2.png)

It has a few killer features I wanted:

- If you stop typing for a long time (think an hour), it start beeping at you
- It then keeps beeping at you until you "catch up" to a total rate of 2 wpm or so -- that is, about 100 words an hour. As longas you're actively typing, it doesn't beep.
- The beep is subtle enough that I don't want to throw it out a window (your mileage may vary)
- You can turn on "typewriter" mode where you can't backspace. I haven't tried that yet--it would be more for something like writing a rough draft of a document and less for taking notes.
- You can work on two computers (it has cloud storage with no login)
- It saves locally and you don't need the internet

We added a couple features later:

- The weirdest by far is my request for a very subtle indicator of how much you need to "catch up" when it's not beeping. The result is a glowing bar on the bottom, which fades and disappears when you are all caught up on typing.
- A "working hours" settings, where it automatically doesn't beep between certain hours.
- It support multiple document editing with tabs. This may have been a mistake.


![caption: type a lot more words](zen-notes3.png)
![caption: type a few more words](zen-notes4.png)
