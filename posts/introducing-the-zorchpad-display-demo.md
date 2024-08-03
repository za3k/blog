---
author: admin
categories:
- Technical
date: 2023-06-07 16:42:28-07:00
has-comments: true
source: wordpress
tags:
- computers
- hardware
- microcontroller
- zorchpad
title: Introducing the Zorchpad (+ display demo)
updated: 2023-06-07 17:00:00-07:00
wordpress_id: 1043
wordpress_slug: introducing-the-zorchpad-display-demo
---
A friend of mine, [Kragen Javier Sitaker](http://canonical.org/~kragen/) has been designing something he calls the zorzpad (see link below). I can never remember the name, so as a joke my version became the “zorch pad”. We live on opposite sides of the globe, but we’ve picked up the same or similar hardware, and have been having fun developing the hardware and software together.

The basic idea of the Zorchpad is to have one computer, indefinitely. It should keep working until you die. That means no battery that runs out, and no parts that go bad (and of course, no requirements to “phone home” for the latest update via wifi!). This is not your standard computer, and we’ve been trying a lot of experimental things. One of the main requirements is that everything be very low-power. He picked out the excellent [apollo3](https://www.sparkfun.com/categories/tags/apollo3) processor, which theoretically runs at around 1mW. In general, the zorchpad is made of closed-source hardware.

Since I’ve realized this will be a long project, I’m going to post it piece-by-piece as I make progress. Below is a demo of the display.

<iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="456" src="https://www.youtube.com/embed/CXOpiH0CqLo?feature=oembed" title="Zorchpad Graphics Demo (pre-alpha)" width="810"></iframe>

The graphics demo shows, in order:

-   a title screen
-   a flashing screen (to show graphics-mode framerate)
-   a demo of font rendering. we’re using the fixed-width font [tamsyn](http://www.fial.com/~scott/tamsyn-font/).
-   a [munching squares](https://en.wikipedia.org/wiki/Munching_square) animation
-   a demo of how fast “text-mode” updates would be

We’re using a [memory-in-pixel LCD](https://www.sharpsde.com/products/displays/model/ls027b7dh01/#productview). The only manufacturer is Sharp LCD. You have have seen these before in things like the Pebble watch–they’ve very low-power except when you’re updating. This particular screen is quite tiny–240x400px display (which is fine with me), but only 1.39×2.31 inches (35x59mm). The only bigger screen available in this technology is 67x89mm, a bit lower resolution, and out of stock. As soon as it’s in stock I plan to switch to it.

According to the datasheet, the screen consumes 0.05-0.25mW without an update, and perhaps 0.175-0.35mW updating once per second. We haven’t yet measured the real power consumption for any of the components.

The most obvious alternative is e-ink. E-ink has a muuuch slower refresh rate (maybe 1Hz if you hack it), and uses no power when not updating. Unfortunately it uses orders of magnitude more power for an update. Also, you can get much larger e-ink screens. The final zorchpad might have one, both or something else entirely! We’re in an experimentation phase.

Datasheets, a bill of materials, and all source code can be found in my [zorchpad](https://github.com/za3k/zorchpad) repo. Also check out Kragen’s [zorzpad](http://canonical.org/~kragen/sw/zorzpad/) repo.
