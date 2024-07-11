---
author: admin
categories:
- Technical
date: 2023-11-07 07:33:14-07:00
markup: html
source: wordpress
tags:
- graphics
- hack-a-day
- raytracing
title: 'Hack-A-Day, Day 06: Raytracing Redux (realtime video)'
updated: 2023-11-11 11:39:03-07:00
wordpress_id: 1152
wordpress_slug: hack-a-day-day-06
---
Today’s update is a short one. I ported my raytracer from [day 02][1], to the Nvidia GPU: [ha3k-06-raytracer][2]

The visuals are pretty much the same. Incidentally I discovered the striations on the ground disappear if we increase the floating point precision.

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v15b-300x225.png)][3]

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v16-300x225.png)][4]

Render on the GPU is 30x faster (0.05 fps -> 3 fps). That’s still not very fast.

I didn’t get video working yesterday, or anything else visually new. I will call this one a failure overall, because I have nothing interesting to show off. I learned stuff and made progress though, so it’s not so bad.

Here’s a working video!

[1]: https://blog.za3k.com/hack-a-day-day-2-raytracing/
[2]: https://github.com/za3k/ha3k-06-raytracer
[3]: https://blog.za3k.com/wp-content/uploads/2023/11/v15b.png
[4]: https://blog.za3k.com/wp-content/uploads/2023/11/v16.png
