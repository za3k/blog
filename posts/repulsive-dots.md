---
author: admin
categories:
- Non-Technical
- Technical
date: 2024-06-25 13:33:31-07:00
has-comments: false
source: wordpress
tags:
- godot
- programming
- throwaway
title: Repulsive Dots
updated: 2024-06-25 13:33:32-07:00
wordpress_id: 1407
wordpress_slug: repulsive-dots
---
[![](/wp-content/uploads/2024/06/geodesic_screenshot-1024x566.jpg)](/wp-content/uploads/2024/06/geodesic_screenshot.jpg)

Lately I’ve been messing about in [Godot](https://godotengine.org/), a framework for making video games (similar to Unity).

I wanted to make a 3D game. In my game, you live in a geodesic dome, and can’t go outside, because *mumble mumble mumble poisonous atmosphere?*.

A geodesic dome, I learned, is related to the *icosahedron*, or d20 from RPGs.

<figure class="wp-block-gallery has-nested-images columns-default wp-block-gallery-1 is-layout-flex wp-block-gallery-is-layout-flex" markdown="1">

[![](/wp-content/uploads/2024/06/image-150x150.png)](/wp-content/uploads/2024/06/image.png)

[![](/wp-content/uploads/2024/06/image-1-150x150.png)](/wp-content/uploads/2024/06/image-1.png)

[![](/wp-content/uploads/2024/06/image-3-150x150.png)](/wp-content/uploads/2024/06/image-3.png)

</figure>

A simple dome is the top half of the icosahedron. As they get more complex, you divide each triangle into more and more smaller triangles.

[![caption:Icosahedron getting more and more detailed. Geodesic domes are the top half of each sphere.](/wp-content/uploads/2024/06/sphere-crop.jpg)](/wp-content/uploads/2024/06/sphere-crop.jpg)

So to make a nice geodesic dome, we could find one (I failed), make one in Blender (too hard), or use some math to generate one in Godot. And to do that math, we need to know the list of 20 icosahedron faces. Which basically just needs the list of the 12 vertices!

Now, obviously you could look up the vertices, but I thought of a more fun way. Let’s put 12 points on a sphere, make them all repel each other (think magnetically, I guess), and see where on the sphere they slide to. Maybe they will all be spaced out evenly in the right places. Well, here’s what it looks like:

<iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="456" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" src="https://www.youtube.com/embed/kDoWaa-xilA?feature=oembed" title="icosahedron calculator" width="810"></iframe>

So… kinda? It was certainly entertaining.

By the way, the correct coordinates for the vertices of an icosahedron inside a unit sphere are:

-   the top at (0, 1, 0)
-   the bottom at (0, -1, 0)
-   10 equally spaced points around a circle. they alternate going up and down below the center line.  
    (**±**1/√5, sin(angle), cos(angle)) \[projected onto the sphere\]
