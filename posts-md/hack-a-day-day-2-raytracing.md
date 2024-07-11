---
author: admin
categories:
- Technical
date: 2023-11-02 21:38:58-07:00
markup: html
source: wordpress
tags:
- graphics
- hack-a-day
- raytracing
title: 'Hack-A-Day, Day 02: Raytracing'
updated: 2023-11-11 11:39:34-07:00
wordpress_id: 1141
wordpress_slug: hack-a-day-day-2-raytracing
---
Today I wrote a simple raytracer. A raytracer is a very simple way to draw excellent graphics. For each pixel, it follows an imaginary “line” out from the viewer through that pixel into the computer world. Then it colors the pixel based on what the line hits. Unfortunately, it also takes a lot of computing power.

Mine is based on the explanation (and code) from “[Ray Tracing in One Weekend][1]“, and the code from “[My Very First Raytracer][2]“.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v11b.png)][3]

Matte spheres in different shades of grey. The blue in the spheres is reflected from the sky.

The motivation for this project was to learn how to make things run faster on a graphics card. I quickly realized (before I wrote a line of code) that I’d need the basic raytracer to be its own project. Having it run faster will have to be a job for another day!

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v15c.png)][4]

A final demo scene, showing off reflectivity and metal surfaces.  
Note the pincushion distortion of the overall render, and striations on the ground.

[1]: https://raytracing.github.io/books/RayTracingInOneWeekend.html
[2]: http://canonical.org/~kragen/sw/aspmisc/my-very-first-raytracer.html
[3]: https://github.com/za3k/ha3k-02
[4]: https://github.com/za3k/ha3k-02
