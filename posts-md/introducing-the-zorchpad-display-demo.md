---
author: admin
categories:
- Technical
date: 2023-06-07 16:42:28-07:00
markup: html
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
A friend of mine, [Kragen Javier Sitaker][1] has been designing something he calls the zorzpad (see link below). I can never remember the name, so as a joke my version became the “zorch pad”. We live on opposite sides of the globe, but we’ve picked up the same or similar hardware, and have been having fun developing the hardware and software together.

The basic idea of the Zorchpad is to have one computer, indefinitely. It should keep working until you die. That means no battery that runs out, and no parts that go bad (and of course, no requirements to “phone home” for the latest update via wifi!). This is not your standard computer, and we’ve been trying a lot of experimental things. One of the main requirements is that everything be very low-power. He picked out the excellent [apollo3][2] processor, which theoretically runs at around 1mW. In general, the zorchpad is made of closed-source hardware.

Since I’ve realized this will be a long project, I’m going to post it piece-by-piece as I make progress. Below is a demo of the display.

The graphics demo shows, in order:

-   a title screen
-   a flashing screen (to show graphics-mode framerate)
-   a demo of font rendering. we’re using the fixed-width font [tamsyn][3].
-   a [munching squares][4] animation
-   a demo of how fast “text-mode” updates would be

We’re using a [memory-in-pixel LCD][5]. The only manufacturer is Sharp LCD. You have have seen these before in things like the Pebble watch–they’ve very low-power except when you’re updating. This particular screen is quite tiny–240x400px display (which is fine with me), but only 1.39×2.31 inches (35x59mm). The only bigger screen available in this technology is 67x89mm, a bit lower resolution, and out of stock. As soon as it’s in stock I plan to switch to it.

According to the datasheet, the screen consumes 0.05-0.25mW without an update, and perhaps 0.175-0.35mW updating once per second. We haven’t yet measured the real power consumption for any of the components.

The most obvious alternative is e-ink. E-ink has a muuuch slower refresh rate (maybe 1Hz if you hack it), and uses no power when not updating. Unfortunately it uses orders of magnitude more power for an update. Also, you can get much larger e-ink screens. The final zorchpad might have one, both or something else entirely! We’re in an experimentation phase.

Datasheets, a bill of materials, and all source code can be found in my [zorchpad][6] repo. Also check out Kragen’s [zorzpad][7] repo.

1.  ![](https://secure.gravatar.com/avatar/a1e9d69b1d8b0a1fd3a90f03a40de162?s=40&d=mm&r=g)JenniferRM says:
    
    [April 20, 2024 at 9:52 am][8]
    
    Very cool idea. I was imagining form factors, and was thinking briefly about somehow having a sort of laptop arrangement where an e-ink screen is visible through glass when it is closed and in some kind of “protective storage mode”, and then visible directly from “the proper side of the e-ink screen” after it opens up. This is probably impossible using default hardware options, but searching around to confirm this lead to some interesting links and unusual design demos.
    
    Here’s ~12 year old thread from someone who wants a computer to use in an off grid cabin.  
    [https://forums.tomshardware.com/threads/ultra-low-power-pc-to-run-off-solar-power.1375469/][9]
    
    Here is a 2023 video about the revived product “GVUIDO” (pronounced Guido) optimized for musicians where part of the UI involves covering a light sensor.  
    [https://www.youtube.com/watch?v=wTIf9wjm0y8][10]
    
    One thing that struck me is that a lot of people might want a Xorchpad to stick INSIDE a larger system (out in nature? as part of a science package?) that might install a rugged solar panel and battery. Then a small USB-C cord might provide a Xorchpad inside the unit with power, and want some intelligence to come out of the same cord, in exchange?
    
    I’m not sure if a USB-C is consistent with the vision, however. Maybe the “minimum power” for that is far above the “maximim power” that would not blow the Sourcepad’s circuits?
    
    [Reply][11]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [April 20, 2024 at 10:24 am][12]
        
        Try using numbers, instead of words! It works better for comparing power usage.
        
        The “low-power computer” someone wants from 12 years ago should be 3W. The Zorchpad is designed to run at 0.001W.
        
        I’m not sure what GVUIDO has to do with anything, was there a reason you linked that?
        
        The Zorchpad could easily be powered by any standard cable, yes. But if you need a larger system to power it, you’re missing the point.
        
        “Blowing circuits” is not a correct intuition for designing low-power electronics. Go learn about Ohm’s Law!
        
        [Reply][13]
        

[1]: http://canonical.org/~kragen/
[2]: https://www.sparkfun.com/categories/tags/apollo3
[3]: http://www.fial.com/~scott/tamsyn-font/
[4]: https://en.wikipedia.org/wiki/Munching_square
[5]: https://www.sharpsde.com/products/displays/model/ls027b7dh01/#productview
[6]: https://github.com/za3k/zorchpad
[7]: http://canonical.org/~kragen/sw/zorzpad/
[8]: https://blog.za3k.com/introducing-the-zorchpad-display-demo/#comment-11338
[9]: https://forums.tomshardware.com/threads/ultra-low-power-pc-to-run-off-solar-power.1375469/
[10]: https://www.youtube.com/watch?v=wTIf9wjm0y8
[11]: https://blog.za3k.com/introducing-the-zorchpad-display-demo/?replytocom=11338#respond
[12]: https://blog.za3k.com/introducing-the-zorchpad-display-demo/#comment-11339
[13]: https://blog.za3k.com/introducing-the-zorchpad-display-demo/?replytocom=11339#respond
