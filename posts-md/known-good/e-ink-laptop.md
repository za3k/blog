---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-10-12 15:45:27-07:00
markup: html
source: wordpress
tags:
- eink
- electronics
- physical
- prototype
title: "e-ink \u201Claptop\u201D"
updated: 2022-10-13 10:30:55-07:00
wordpress_id: 801
wordpress_slug: e-ink-laptop
---
I’ve been prototyping an e-ink laptop.

[![alt:a wooden box with a keyboard inside and an e-ink screen mounted to it](https://blog.za3k.com/wp-content/uploads/2022/10/front_view_open-1024x768.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/front_view_open-scaled.jpg)

[![caption:Closed “laptop”](https://blog.za3k.com/wp-content/uploads/2022/10/front_view-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/front_view-scaled.jpg)

I’m not the first, there have been many other such devices before. I came up with the idea independently, but the specifics are heavily inspired by the [Ultimate Writer](https://alternativebit.fr/posts/ultimate-writer/) by NinjaTrappeur in 2018. Similar to him, my use case is typing without distractions, and reading books. E-ink displays are quite slow to update, so I don’t think it can serve as a general purpose computer. Here’s a video of it in action. It operates at one frame per second.

<video controls="" src="https://za3k.com/archive/eink_typing1.mp4"></video>

The electronics are not fully done. They need better secured, and I’m going to redo the cabling and power back.

[![caption:I broke a screen over-tightening a nut. That said, I like this look pretty well! If the lid was thicker, I know how to avoid screws on the other side, too.](https://blog.za3k.com/wp-content/uploads/2022/10/screen_closeup-1024x768.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/screen_closeup-scaled.jpg)

[![caption:Early screen progress. I got something to display, but not what I wanted.](https://blog.za3k.com/wp-content/uploads/2022/10/early_garbage-crop-300x224.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/early_garbage-crop-scaled.jpg)

[![caption:I found a really nice, cheap mechanical keyboard on ebay. The main downside is that it’s heavy–730g. It also consumes heavy amounts of power, even when not in use. I have a nearly identical keyboard that doesn’t, which I’ll use for v2.](https://blog.za3k.com/wp-content/uploads/2022/10/keyboard_closeup-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/keyboard_closeup-scaled.jpg)

[![caption:I made my own lithium-ion battery pack. It works well, but it doesn’t quite fit so I’m going to redo it with one less cell. It also needs an on/off switch and a right angle USB cable.](https://blog.za3k.com/wp-content/uploads/2022/10/battery_back_closeup-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/battery_back_closeup-scaled.jpg)

[![caption:The prototype is powered by a Raspberry Pi 3. The final version will use a microcontroller to save power. The Pi Zero can also be swapped in with no changes, and uses a third of the power. But it’s noticeably slower and takes 30 seconds to boot. For prototyping I’m using the Pi 3 for now.](https://blog.za3k.com/wp-content/uploads/2022/10/pi_closeup-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/pi_closeup-scaled.jpg)

I’m not the best woodworker, but I’m slowly learning. Here are pictures of case and lid action.

[![caption:Hinged lid. The screen is on the bottom of the lid.](https://blog.za3k.com/wp-content/uploads/2022/10/added_back_stops-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/added_back_stops-scaled.jpg)

[![caption:A wooden stop on each side](https://blog.za3k.com/wp-content/uploads/2022/10/back_stop-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/back_stop-scaled.jpg)

[![caption:Wooden stop with lid open. It hits the bottom, bringing the lid/screen to a rest at vertical.](https://blog.za3k.com/wp-content/uploads/2022/10/back_stop_action-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/back_stop_action-scaled.jpg)

[![caption:Latches on the side](https://blog.za3k.com/wp-content/uploads/2022/10/hinge-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/hinge-scaled.jpg)

[![caption:Don’t put hinges sideways into plywood. But if you do, drill big pilot holes. Out of six screw, one cracked a little.](https://blog.za3k.com/wp-content/uploads/2022/10/hinge_crack-300x225.jpg)](https://blog.za3k.com/wp-content/uploads/2022/10/hinge_crack-scaled.jpg)

On the software end, shout outs to:

-   the creator of the [ultimate-writer](https://github.com/NinjaTrappeur/ultimate-writer) software, NinjaTrappeur, who has been encouraging (and explained the right way to rewrite the stack, if you wanted to today).
-   Ben Krasnow, who made a [video](https://www.youtube.com/watch?v=MsbiO8EAsGw&ab_channel=AppliedScience) about how to hack partial refresh on an e-ink display.

There’s a few things I’d like to polish still–even as a prototype this isn’t fully done.

-   The raspberry pi and battery pack are currently sitting loose. They need secured, especially since they can fall out the open front.
-   The software has some major problems. It doesn’t support Control-C, etc in linux, a must, and it doesn’t update the screen at boot until you press a key, which would be nice to fix.
-   There’s no power switch. Right now you have to unplug it manually.
-   I’d like to add a carrying handle.
-   I’d like to tuck away the electronics behind a panel. They’re ugly.
-   The wood looks rough in a few places. I want to hide some splintered wood, screw holes, etc.
-   The USB cables have too much stress on them. I need to make a little more room in the wood, and use a right-angled connector in one place.

There’s also no default software, but that’s a feature. A prototype is for figuring out how I want the interface to work, and what I want it to do.

Parts list

-   [7.5 inch e-ink screen](https://www.waveshare.com/7.5inch-e-paper-hat.htm) from Waveshare (not particularly good) – $60
-   Raspberry Pi 3 (Pi Zero, etc also work with no changes) – $35 (but unavailable)
-   microsd card – $7
-   Plywood and boards, wood glue – $15
-   [Plexiglass](https://www.amazon.com/gp/product/B088LXM1P1) (to cover screen) – $10
-   Bolts, washers, and nuts to secure it. – $5
-   Circular [window latch](https://www.amazon.com/dp/B000CSGD1U) x2 – $8 (or use $10 smaller [version](https://www.amazon.com/dp/B09ZTLLC6K))
-   Hinge x2 – $2
-   Total: $142

Power budget (at 5V):

-   Keyboard: 500mW. Other USB keyboards use zero to within my measurement abilities.
-   Screen: 0-250mW when updating. Hard to measure.
-   Pi 3: 2000mW. I have the wifi chip enabled (the default) but I’m not actively connected to wifi.
-   Pi Zero W: 650mW

A real-life test showed 5-6 hour battery life. Theory says (13Wh/battery \* 4 batteries / 2.7 watts)=20 hours battery life. I’m investigating the discrepancy. In theory, swapping for a Pi Zero W and a better keyboard would give 72-hour battery life.
