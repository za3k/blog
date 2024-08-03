---
author: admin
categories:
- Technical
date: 2024-05-17 10:04:12-07:00
has-comments: false
source: wordpress
tags:
- zorchpad
title: 'Zorchpad Update: Cardboard mockup, mk1'
updated: 2024-05-17 10:05:55-07:00
wordpress_id: 1363
wordpress_slug: zorchpad-update-cardboard-mockup-mk1
---
I’ve gotten to the point in Zorchpad development where I’d like to see how the whole thing fits together and if there will be any insurmountable problems. We’re still trying to figure out some things like–will it have one screen or two? What form factor will it be? Will the keyboard fold in half? So I put together a cardboard model.

[![](../wp-content/uploads/2024/05/v0_cardboard_zorchpad-1024x576.jpg)](../wp-content/uploads/2024/05/v0_cardboard_zorchpad.jpg)

This model has:

-   A power switch. I’m assuming the very first prototype will run on battery, not solar like the final one.
-   Two memory-in-pixel screens (total power usage: 0.001 W)
-   One e-ink display (total power usage: variable/unknown)
-   An apollo3 artemis board, which includes RAM, CPU, microphone, and BTLE (not pictured, total power usage about 0.0005 W)
-   One flash chip (not pictured, power usage variable)
-   A battery slot. I’m using AAA for my convenience (Holds: 3000 joules = ~20 days power)
-   An audio jack for headphones
-   A microSD slot
-   A custom keyboard (total power usage: variable/unknown)  
    The keyboard is closely modeled off a standard one, for now.

[![](../wp-content/uploads/2024/05/v0_keyboard.jpg)](../wp-content/uploads/2024/05/v0_keyboard.jpg)

Immediately, a few problems pop out:

-   It’s fairly long. This will stick out of my pocket. This is with very closely spaced keys on a somewhat reduced keyboard.
-   There’s not really a great place to put solar panels. It’s has almost zero free space, plus there’s going to be a lot of wiring. Are we going to drill holes through the solar panel to let wires pass through? Also, I **really** haven’t been able to figure out how many cm2 of solar we need.
-   It’s hard to get the screen to stay propped up on my cardboard model. I’d like a solution that doesn’t use hinges, since those tend to loosen over time.

My next step will probably be to make a custom working keyboard. Then, I’ll make an entire working zorchpad. Both will be either cardboard or 3d-printed (whichever is easier).
