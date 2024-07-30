---
author: admin
categories:
- Technical
date: 2023-11-22 21:15:14-07:00
markup: html
source: wordpress
tags:
- circuits
- electronics
- hack-a-day
- pcb
title: 'Hack-a-Day, Day 22: Homemade PCBs'
updated: 2023-11-22 21:45:57-07:00
wordpress_id: 1208
wordpress_slug: hack-a-day-day-22-homemade-pcbs
---
Today I learned how to make PCBs. I didn’t invent anything here, this is all pretty well known by the PCB-making community, but it’s not well-known to *me*. So I taught myself a bit!

The first part was the design an electronic circuit. I decided I was short on time, so I grabbed an [existing schematic](https://www.circuits-diy.com/simple-continuity-tester-circuit-using-555-timer-ic/).

[![](https://blog.za3k.com/wp-content/uploads/2023/11/continuity_tester-300x204.png)](https://blog.za3k.com/wp-content/uploads/2023/11/continuity_tester.png)

Next, I downloaded KiCAD, and recreated the circuit there. I found [this video tutorial](https://www.youtube.com/watch?v=zK3rDhJqMu0&ab_channel=WindsorSchmidt) very helpful to learn kicad.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad_schematic.png)](https://blog.za3k.com/wp-content/uploads/2023/11/kicad_schematic.png)

Next, I made the actual PCB layout.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb.png)](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb.png)

To my surprise, after a little jiggling I got it down to a one-layer design.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-1 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb2.png)](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb2.png)

</figure>

That means home-printing would be much easier. No having to line up the two sides carefully.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/printable.png)](https://blog.za3k.com/wp-content/uploads/2023/11/printable.png)

I printed out the image on paper (backwards) on my toner printer, and taped it to the copper-clad PCBs.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_024251429-crop-260x300.jpg)](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_024251429-crop.jpg)

First, I tried laminating it. Almost no ink transferred, and the paper came off easily. Then I tried ironing it, but the paper stick to the iron and not to the PCB. The tape melted on the iron. For both, I dunked them in water after, which is supposed to help loosen the paper.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-2 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-169x300.png)](https://blog.za3k.com/wp-content/uploads/2023/11/image.png)

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-2-169x300.png)](https://blog.za3k.com/wp-content/uploads/2023/11/image-2.png)

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-4-169x300.png)](https://blog.za3k.com/wp-content/uploads/2023/11/image-4.png)

</figure>

Next, I tried the standard advice–sand the PCBs (I used 320 grit) and use glossy paper. This time, both pieces of paper stuck very well. I was wary about the iron coming off again, so I just left it on place on the highest heat–this worked fine for adhesion, but I had to iron out wrinkles at the end. The laminated piece had lose edges, while the ironed piece was on there totally flat.

I tried peeling off the laminated paper–oops! It peeled back and most of the ink stayed on the paper. I think if I took it off more carefully, it would have worked.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-5-edited.png)](https://blog.za3k.com/wp-content/uploads/2023/11/image-5.png)

I picked at the ironed paper a bit, but it didn’t budge. I let it sit in dish soap for a while so the paper would fall apart. The first hour didn’t do anything.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_041248880-crop-1024x719.jpg)](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_041248880-crop.jpg)

Meanwhile, I made an order at PCBWay. It’s still under review.

Edit: after some advice from a friend, I peeled off this paper more aggressively, and scrubbed it off. The ink was fine. It doesn’t look great, but I think this is mostly the wrinkles during transfer. It’s a little blurry, I’ll have to do a third attempt before I try etching.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_044211359-crop-875x1024.jpg)](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_044211359-crop.jpg)
