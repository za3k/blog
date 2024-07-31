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
Today’s update is a short one. I ported my raytracer from [day 02](https://blog.za3k.com/hack-a-day-day-2-raytracing/), to the Nvidia GPU: [ha3k-06-raytracer](https://github.com/za3k/ha3k-06-raytracer)

The visuals are pretty much the same. Incidentally I discovered the striations on the ground disappear if we increase the floating point precision.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-1 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v15b-300x225.png)](https://blog.za3k.com/wp-content/uploads/2023/11/v15b.png)

[![](https://blog.za3k.com/wp-content/uploads/2023/11/v16-300x225.png)](https://blog.za3k.com/wp-content/uploads/2023/11/v16.png)

</figure>

Render on the GPU is 30x faster (0.05 fps -> 3 fps). That’s still not very fast.

<s>I didn’t get video working yesterday, or anything else visually new. I will call this one a failure overall, because I have nothing interesting to show off.</s> I learned stuff and made progress though, so it’s not so bad.

Here’s a working video!

<iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/y4TcrxRg4aw?si=ca7wFptQ99gffghI" title="YouTube video player" width="560"></iframe>
