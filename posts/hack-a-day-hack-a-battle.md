---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-11-22 09:15:34-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- art
- hack-a-day
- music
- november
- throwaway
- video game
- visualizer
title: 'Hack-A-Day: Hack-A-Battle'
updated: 2022-11-22 09:24:22-07:00
wordpress_id: 922
wordpress_slug: hack-a-day-hack-a-battle
---
It’s november, and I’ve decided this month that I’m going to do 30 projects in 30 days. It’s an all-month hack-a-thon!

Yesterday’s project was [Hack-A-Battle](https://tilde.za3k.com/hackaday/battle/) ([demo](https://tilde.za3k.com/hackaday/battle/), [source](https://github.com/za3k/day21_battle)). It’s two dueling music visualizers (sound warning!). Red vs blue. As each hits the other with bullets, they lose heath. As a band takes damage, it gets dimmer and quieter. Eventually one band will win out and be the only one playing.

[![](../wp-content/uploads/2022/11/screenshot-18-1024x222.png)](https://tilde.za3k.com/hackaday/battle/)

I thought this was a cool idea, but I’m not really happy with the implementation

-   It’s a little laggy, especially when explosions happen.
-   It’s probably a little too fast of a battle.
-   I wanted to the things coming out to actually be linked to a music visualizer, which I almost had time to do.
-   It would have been better if the “bands” took turns playing instead of both going at once, for the poor listener.
-   It requires a fairly big display, and beefy computer/phone. It doesn’t work well on a small screen at all.
-   I wasn’t super pleased with the code. It was so-so
-   I wanted you to be able to upload your own songs and duel a friend
