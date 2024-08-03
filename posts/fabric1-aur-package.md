---
author: admin
categories:
- Technical
date: 2020-06-04 18:30:31-07:00
has-comments: false
source: wordpress
tags:
- fabric
- linux
- open source
title: fabric1 AUR package
updated: 2021-06-05 15:38:23-07:00
wordpress_id: 542
wordpress_slug: fabric1-aur-package
---
Fabric is a system administration tool used to run commands on remote machines over SSH. You program it using python. In 2018, Fabric 2 came out. In a lot of ways it’s better, but it’s incompatible, and removes some features I really need. I talked to the Fabric dev (bitprophet) and he seemed on board with keeping a Fabric 1 package around (and maybe renaming the current package to Fabric 2).

Here’s an arch package: [https://aur.archlinux.org/packages/fabric1/](https://aur.archlinux.org/packages/fabric1/)

Currently Fabric 1 runs only on Python2. But there was a project to port it to Python 3 (confusingly named fabric3), which is currently attempting to merge into mainline fabric. Once that’s done, I’m hoping to see a ‘fabric1’ and ‘fabric2’ package in all the main distros.
