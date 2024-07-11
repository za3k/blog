---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-07-08 12:02:57-07:00
markup: html
source: wordpress
tags:
- archiving
- software
- youtube
title: youtube-autodl
updated: 2022-07-08 12:02:57-07:00
wordpress_id: 745
wordpress_slug: youtube-autodl
---
I just wrote the first pass at [youtube-autodl][1], a tool for automatically downloading youtube videos. It’s inspired by Popcorn Time, a similar program I never ended up using, for automatically pirating the latest video from a TV series coming out.

You explain what you want to download, where you want to download it to, and how to name videoes. youtube-autodl takes care of the rest, including de-duplication and downloading things ones.

The easiest way to understand it is to take a look at the example [config file][2], which is my actual config file.

Personally, I find youtube is pushing “watch this related” video and main-page feeds more and more, to the point where they actually succeed with me. I don’t want to accidentally waste time, so I wanted a way to avoid visiting youtube.com. This is my solution.

[1]: https://github.com/za3k/youtube-autodl
[2]: https://github.com/za3k/youtube-autodl/blob/master/config.yaml
