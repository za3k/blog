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

The first part was the design an electronic circuit. I decided I was short on time, so I grabbed an [existing schematic][1].

[![](https://blog.za3k.com/wp-content/uploads/2023/11/continuity_tester-300x204.png)][2]

Next, I downloaded KiCAD, and recreated the circuit there. I found [this video tutorial][3] very helpful to learn kicad.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad_schematic.png)][4]

Next, I made the actual PCB layout.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb.png)][5]

To my surprise, after a little jiggling I got it down to a one-layer design.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb2.png)][6]

That means home-printing would be much easier. No having to line up the two sides carefully.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/printable.png)][7]

I printed out the image on paper (backwards) on my toner printer, and taped it to the copper-clad PCBs.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_024251429-crop-260x300.jpg)][8]

First, I tried laminating it. Almost no ink transferred, and the paper came off easily. Then I tried ironing it, but the paper stick to the iron and not to the PCB. The tape melted on the iron. For both, I dunked them in water after, which is supposed to help loosen the paper.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-169x300.png)][9]

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-2-169x300.png)][10]

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-4-169x300.png)][11]

Next, I tried the standard advice–sand the PCBs (I used 320 grit) and use glossy paper. This time, both pieces of paper stuck very well. I was wary about the iron coming off again, so I just left it on place on the highest heat–this worked fine for adhesion, but I had to iron out wrinkles at the end. The laminated piece had lose edges, while the ironed piece was on there totally flat.

I tried peeling off the laminated paper–oops! It peeled back and most of the ink stayed on the paper. I think if I took it off more carefully, it would have worked.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/image-5-edited.png)][12]

I picked at the ironed paper a bit, but it didn’t budge. I let it sit in dish soap for a while so the paper would fall apart. The first hour didn’t do anything.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_041248880-crop-1024x719.jpg)][13]

Meanwhile, I made an order at PCBWay. It’s still under review.

Edit: after some advice from a friend, I peeled off this paper more aggressively, and scrubbed it off. The ink was fine. It doesn’t look great, but I think this is mostly the wrinkles during transfer. It’s a little blurry, I’ll have to do a third attempt before I try etching.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_044211359-crop-875x1024.jpg)][14]

[1]: https://www.circuits-diy.com/simple-continuity-tester-circuit-using-555-timer-ic/
[2]: https://blog.za3k.com/wp-content/uploads/2023/11/continuity_tester.png
[3]: https://www.youtube.com/watch?v=zK3rDhJqMu0&ab_channel=WindsorSchmidt
[4]: https://blog.za3k.com/wp-content/uploads/2023/11/kicad_schematic.png
[5]: https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb.png
[6]: https://blog.za3k.com/wp-content/uploads/2023/11/kicad-pcb2.png
[7]: https://blog.za3k.com/wp-content/uploads/2023/11/printable.png
[8]: https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_024251429-crop.jpg
[9]: https://blog.za3k.com/wp-content/uploads/2023/11/image.png
[10]: https://blog.za3k.com/wp-content/uploads/2023/11/image-2.png
[11]: https://blog.za3k.com/wp-content/uploads/2023/11/image-4.png
[12]: https://blog.za3k.com/wp-content/uploads/2023/11/image-5.png
[13]: https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_041248880-crop.jpg
[14]: https://blog.za3k.com/wp-content/uploads/2023/11/PXL_20231123_044211359-crop.jpg
