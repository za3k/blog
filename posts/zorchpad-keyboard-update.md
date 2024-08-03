---
author: admin
categories:
- Technical
date: 2024-05-26 18:25:37-07:00
has-comments: false
source: wordpress
tags:
- hardware
- zorchpad
title: Zorchpad keyboard update
updated: 2024-05-26 18:28:14-07:00
wordpress_id: 1372
wordpress_slug: zorchpad-keyboard-update
---
The Zorchpad needs a custom keyboard. Its power budget is only 1mW, and there’s just nothing available in that range. So, I need to make a custom keyboard. I started reading up on how to make your own–especially the electronics.

I don’t know how to make a PCB:

![caption:PCB from HacKeyboard](../wp-content/uploads/2024/05/image-1.png)

Or how to attach headers to the inside of an existing keyboard, which looks like this–:

![alt:Mapping the Innards of a Keyboard : 7 Steps (with Pictures) - Instructables](https://content.instructables.com/FOM/VMTN/HZN0VZGV/FOMVMTNHZN0VZGV.jpg?auto=webp&frame=1&width=2100)

But I found a project called [GOLEM](https://golem.hu/guide/keyboard-build-logs/) with an excellent guide to making your own keyboard. Here is their wiring:

![GOLEM Macropad](../wp-content/uploads/2024/05/image.png)

I can do that! They got me out of a major rut.

---

[Their advice](https://golem.hu/guide/first-macropad) walks you through how to do a small keyboard in a cardboard plate. I did a few keys, gauged the effort, and decided to use my 3D printer. Cutting out 50-60 keys precisely by hand doesn’t sound easy. Worse, if you mess up, you have to start over. In plastic, I can’t mess up halfway, and the spacers to support the keyboard can be part of the print.

[![](../wp-content/uploads/2024/05/2024-05-20-233106_2560x1440_scrot-1024x576.png)](../wp-content/uploads/2024/05/2024-05-20-233106_2560x1440_scrot.png)

Above, I’m designing a “sampler” keyboard in CAD (OpenSCAD). I want to iron out problems in my process before I try a full-size keyboard. Below, Prusa-Slic3r is slicing the finished model for my 3D printer to print.

[![](../wp-content/uploads/2024/05/2024-05-20-235849_1920x1080_scrot-1024x576.png)](../wp-content/uploads/2024/05/2024-05-20-235849_1920x1080_scrot.png)

Here’s the finished sampler keyboard:

[![](../wp-content/uploads/2024/05/tiny_keyboard2-1-1024x747.jpg)](../wp-content/uploads/2024/05/tiny_keyboard2-1.jpg)

Currently I’m waiting on keycaps and switches ordered from China, and then I’ll put together my finished keyboard. But I have been making some progress in the meantime. Here’s the layout I’m going to try.

[![](../wp-content/uploads/2024/05/keyboard57.png)](../wp-content/uploads/2024/05/keyboard57.png)

And I’ve started streaming some development of a case and keyboard on [Twitch](https://www.twitch.tv/za3k) (Tue/Thu 12pm noon, EDT). Feel free to join! Anyone can watch, but you need an account to chat.

[![](../wp-content/uploads/2024/05/stream-1024x576.png)](../wp-content/uploads/2024/05/stream.png)
