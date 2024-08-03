---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-11-11 19:09:16-07:00
has-comments: false
source: wordpress
tags:
- art
- hack-a-day
- mathematics
- november
- throwaway
- video game
title: 'Hack-A-Day: Hack-A-Tile'
updated: 2022-11-13 23:16:17-07:00
wordpress_id: 874
wordpress_slug: hack-a-day-hack-a-tile
---
It’s november, and I’ve decided this month that I’m going to do 30 projects in 30 days. It’s an all-month hack-a-thon!

Today’s project is [Hack-A-Tile](https://tilde.za3k.com/hackaday/tile/) ([demo](https://tilde.za3k.com/hackaday/tile/), [source](https://github.com/za3k/day11_tile)). It’s a tile-matching game like dominos.

[![](/wp-content/uploads/2022/11/screenshot-10.png)](https://tilde.za3k.com/hackaday/tile/)

Hack-A-Tile is based on mathematical [Wang tiles](https://en.wikipedia.org/wiki/Wang_tile). It was very tempting to call it Hack-A-Wang.

If I update it, I would

-   Zoom out as you go. I think that would look cool!
-   Animate shifting over. Right now adding tiles on the top or left is visually confusing.
-   Change the tiles. These are fun mathematically, but not ideal for a game
-   Either add a maximum size, or some constraint to stop you just making one long line.
