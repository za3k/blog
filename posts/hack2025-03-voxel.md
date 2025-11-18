---
author: admin
categories:
- Technical
date: 2025-11-03
tags:
- programming
- voxel
- hack-a-day
slug: hack-voxel
title: "Hack-A-Day, Day 03: Voxel Rendering"
---

[Hack-a-Day](https://za3k.com/hackaday) is my self-imposed challenge to do one project a day, for all of November.

How do you render 3D graphics? Here's a picture of a cube:

![caption: a 3D cube](voxel-paper-3d.jpg)

But when you draw it on paper or a screen, it's flattened. All you see are these three faces. 

![caption: a 2D cube](voxel-paper-2d.jpg)

In fact, if you turn off your brain, it's just three weird polygons. And we can figure out the corners of the polygon. For example, I figured out these with a ruler, measuring they they are on the paper in centimeters.

![caption: some polygons](voxel-paper-2dlabels.jpg)

So to draw a cube, we just need to draw polygons. That's the essence of today's project.

---

Here's a minecraft world.

![caption: my minecraft base](voxel-mc.png)

Here's the same thing in my voxel engine. If you squint, you might be able to recognize they're the same thing. Ignore the stripe at the top.

![caption: my "minecraft" base](voxel-mc-render.png)

Here's a much simpler scene. If you click, you can [explore it online](https://za3k.github.io/hackvoxel/)

[![caption: some 3d stuff](voxel-simple.png)](https://za3k.github.io/hackvoxel/)

The source code is [on github](https://github.com/za3k/hackvoxel).

---

This hack wasn't perfect. There's some significant problems, and I worked on it 3 different days. Oh well, live and learn! I had fun.

Thanks to Claude for the code to extract minecraft data -- that was not the exciting part of this project.
