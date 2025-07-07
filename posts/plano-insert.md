---
author: admin
categories:
- Non-Technical
date: 2025-07-07
tags:
- organizing
title: Plano 3600 Inserts
---

I'm not sure what the correct name for these parts organizers is. I usually call them "Tackle Boxes", even though that's not quite right. People tend to use them to store tiny screws and so on. I use them for electronics.

Today I designed little paper insert to go into them (in CAD), so I can label which electronics are which and find them more easily.

![](plano-usletter.jpg)

Sadly, US letter is not quite big enough to cover the whole box.

Printable PDF is available [in A4](https://za3k.com/archive/plano-insert-a4.pdf) or [in US letter](https://za3k.com/archive/plano-insert-usletter.pdf). You can also [see the SVG](https://za3k.com/archive/plano-insert-usletter.svg) I was given originally which inspired this.

I recomment holding the paper in place with double-stick tape. If you don't have that, the usual trick is to roll normal tape into a small loop facing outwards.

P.S., to crop a PDF from A4 to US letter (assuming everything fits on both) without inflating the file size, use:

```
# Keeps all physical dimensions the same
pdfcrop --bbox "0 0 792 612" smallthing-on-A4.pdf smallthing-on-usletter.pdf
```

