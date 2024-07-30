---
author: admin
categories:
- Technical
date: 2023-06-09 13:28:55-07:00
markup: html
source: wordpress
tags:
- hacks
- hardware
- zorchpad
title: DIY keyboards (and how keyboards work)
updated: 2023-06-12 13:20:11-07:00
wordpress_id: 1059
wordpress_slug: diy-keyboards-and-how-keyboards-work
---
I’ve been pondering simple input methods for microcontrollers. One obvious idea is, a keyboard! But for some reason, my USB keyboards use a staggering amount of power compared to my microcontrollers–1W of power for my mechanical keyboards, maybe 0.1W for the regular ones.

Let’s look inside a commercial keyboard, and see if we can hook up to it:

[![alt:a photograph of the interior of a commercial keyboard. there is a PCB, with two layers of flexible conductor on top, all clamped down](https://blog.za3k.com/wp-content/uploads/2023/06/commercial-1024x549.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/commercial-scaled.jpg)

Yikes. What’s going on? Well, let’s make our own little keyboard, and explore what’s going on. We’ll build it in three layers, or “index cards”:

[![](https://blog.za3k.com/wp-content/uploads/2023/06/copper_parts-694x1024.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/copper_parts-scaled.jpg)

The bottom layer has 6 vertical stripes. The top layer has 3 horizontal stripes. Each place they cross will be a “key” you can press.

In between them, we add a spacer layer (punched holes) so they keys are “up” by default, and you have to press them to make them connect.

This picture might help explain how they will go together:

[![](https://blog.za3k.com/wp-content/uploads/2023/06/copper_layers-1024x705.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/copper_layers-scaled.jpg)

Now we assemble:

[![](https://blog.za3k.com/wp-content/uploads/2023/06/copper_small.gif)](https://blog.za3k.com/wp-content/uploads/2023/06/copper_small.gif)

The final keyboard has 6 x 3 = 18 “keys”. We write the hex digits plus a couple extra keys with marker.

If I attach alligator clips to the second horizontal screw terminal, and fourth vertical screw terminals, and wire a battery and buzzer with the terminals, I get a connection beep only when I press the key “A”:

[![alt:Two terminals with alligator clips attached to row and column terminals, and a screwdriver pointing at the "A" key addressed.](https://blog.za3k.com/wp-content/uploads/2023/06/address-1024x622.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/address-scaled.jpg)

In a real computer, we obviously can’t just move alligator clips around. Instead, we attach wires to all 9 posts–three outputs wires for the horizontal lines, and six inputs for the vertical lines. We output a signal on the first horizontal line, and see if we can read it from any of the six vertical lines inputs. Then we output a signal on the second horizontal line, and see if we can read it, and so on for the third. Assuming only one key is pressed (or none), we can identify the key. This “scanning” process could be done thousands of times a second, rapidly enough that it can’t miss our slowpoke human fingers.

[![caption:Click to view interactive schematic (credit: Kragen)](https://blog.za3k.com/wp-content/uploads/2023/06/schematic-1024x414.png)](http://falstad.com/circuit/circuitjs.html?ctz=CQAgjCAMB0l3BWK0AckDMYwE4As3sA2SQgdgCYFsQFIaRd0aBTAWiwCgBncQ8bciEK4Q5XHToQALgCcArs24gi-QWFwixE8CFkKllPjkHpIm8VEt7FPMKSMDRY0Rcm75NhmAeDcwl9rSHkro6D4g6Cjmge76PKF8hhFREWaWQXFeiQh8fiKmIm7WSnbZic4F6bGeSUmVlUXBPCpJ6vlpjZneojlC7YU6xfFh4OQoySKlVUNZo+N54PbTTYtGY06TS501vWDrlVPbSip7422ry11r4-6Hg8EA7rxzytdQHE8n61On708-61a60gHx6bwSLxBTwhv1w3V+UOexleqj+KORP0ciMxglaWNBeJMI2RiJhjjh4URFLBERGSVJdN6tV6iOZRiW9NBUySLRZoN5RjKaP8Wj6qUKXI04vAUtF2NlFnOhwJzm5zjlKuiG2lpLS9TSGuhBosBy2oMimz4FoCaOtoutDVBCymC0NDBFFgWjqetyWHokHAASmL-P50IJtBYkNoYAgODIQyJbnt0vBEcnBL6+PLJimlWaE+dblKsBHwGmgzKk5MpeHLHQo-XkHGnuRVSm25b3gnO2Le6XU-BK72RRUyw26NH69AW9KB6bs-HpWG0gPJBXg5UV-lxwxJ03Y+aUvPjwWJmLrWvy0PNykwyk65H9zGZ06M+6uyCEwt-M6U+ubw-MUvV3RsX1ndg3nhYFQUg1F4XxJ44NaIUQQADxAVhxDoUIkEg0haXmFwQBkAB7B4AB0uC4ABjABDAA7KiAHNmAY5gZDoqRSJkDgACNwCQLARFwFBqFMah0JoEhwFCIRVRGcwQAAa2YABPLgHgASykGiAAsOAw2hBUnY9CCYJSAFsuJkLS0MMzDxAgMIRFYUgkDCAilIACjomipC0gA3ZgqIAG3IgAaKjSIABzYqiaNI0LQuYfyeIASgcvYCOocQCJTJTEtCuRLKYrgYrkZK5BiqiZGYLgtK4biZC4BysIwZJBHYchxJQJBJkELSysgcgRvQKipD0xqqOmrg+Mq0KuCmqQoq4OQuBCrg6KoyytJosjEoY2QkpS3iAFkgMqRgiWzURXwuh09QQG7LHIe7tQORwIToN64wevUDQoWlbt+jgLu3CIXp+97zgOFNvruuNvCYLD4SWVgwjOJYED2K16ADZjHO6UVUcSFBxgDJDqVG8ZSZtEFgwx48pSZkQTlEaToaQX7pwghCuoHElYOg2machDgpEc8ZyCB5CgbcXAZ0IbBSHUMAED6nBCDAdA2A1wcQAAE2YAAzOjKqkDhCeQ8nMO6BGvyl0RZZaeXr0RDHRptT2fvliW7dlSBaYHMW3Cw6ACEj7AxJ6tNBAQWAo+jgRCBxlAxDYagwDgI3TfN0LLetkPnHYDtXG7APNCDu2OWrgCPe5aufdEOvYNdrrw19iNYJltQWc7qsK9YUVzmHoHznrq3MLF7w6GH6u7hBSXh8VFmZ6lNwYHM0xVaoMAolIdB8EKaBU8gSOok88Q8CznPjbNi3YIH0fn7NDCx7ZgWZOwfrRhAWK2KsCKilNKMgqKBgACoABkZoMWCjIKQHFWpAA)

And this is how most keyboards work. There are some special keys–Shift, Ctrl, Alt, etc might be on their very own line, since we want to detect key combos. And better keyboards can detect multiple keys being pressed at once (N-key rollover), which I think they do by having a completely separate wire to each key which multiple people tell me they do with a diode next to each key.

For the above project, I used:

-   Three index cards
-   A hole punch
-   Scissors
-   A ruler
-   A pen (NOT a pencil, since graphite is conductive)
-   9 screws, 9 nuts, and 18 washes. I selected #6 American Wire Gauge, which is about 4mm thickness
-   [Copper tape](https://www.amazon.com/dp/B07JNJCNVT)

Did this work perfectly? Definitely not.

-   On some keyboards I’ve made, you have to press quite hard.
-   My multimeter takes a while to register a press. I think a microcontroller would be better.
-   You have to attach the terminals carefully. I think what’s going on is that you can actually put the screw *exactly* through the center of the washer which is actually making contact with the strips, so that only the washer is attached, and the screw doesn’t rub against the washer.
-   It’s of course fairly easy to mis-align anything. This is pretty easy to fix with care. I used the “spacer” grid to draw the centerpoint of the printed letters.
-   The screw heads are a bit thick, so it’s hard to press the keys in the column/row next to the screws. A piece of backing cardboard might fix this.

This was my third attempt. Here’s the second, using aluminium foil. It worked at least as well, maybe better, but it was harder to make. I just taped the foil down, taking care not to cover the contact points. I am told the aluminium will gradually oxidize, making it non-conductive.

<figure class="wp-block-gallery has-nested-images columns-5 is-cropped wp-block-gallery-1 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_parts-150x150.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_parts-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_layers-150x150.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_layers-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_03-150x150.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_03-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_01-150x150.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_01-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_02-150x150.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/aluminium_02-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/side_view-1024x576.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/side_view-scaled.jpg)

</figure>

And here’s one using graphite from drawing hard with a #2 pencil.. Graphite, it turns out, works terribly, and I couldn’t read a signal halfway down the index card. Despite what people have told me, I’m not yet convinced you can make a conductive wire out of it.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-2 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](https://blog.za3k.com/wp-content/uploads/2023/06/graphite_parts-1024x442.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/graphite_parts-scaled.jpg)

[![](https://blog.za3k.com/wp-content/uploads/2023/06/graphite_done-1024x666.jpg)](https://blog.za3k.com/wp-content/uploads/2023/06/graphite_done-scaled.jpg)

</figure>
