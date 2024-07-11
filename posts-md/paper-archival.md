---
author: admin
categories:
- Non-Technical
- Technical
date: 2015-04-24 16:58:38-07:00
markup: html
source: wordpress
tags:
- armchair
- backup
- barcodes
- information theory
- qr codes
title: Paper archival
updated: 2015-04-24 17:04:06-07:00
wordpress_id: 187
wordpress_slug: paper-archival
---
Previous work:

-   [Optar][1] (OPTical ARchive), a 2-D barcode format ([github][2])
-   [Paperback][3]

I wanted (for fun) to see if I could get data stored in paper formats. I’d read the previous work, and people put a lot of thought into density, but not a lot of thought into ease of retreival. First off, [acid-free][4] paper lasts 500 years or so, which is plenty long enough compared to any environmental stresses (moisture, etc) I expect on any paper I have.

Optar gets a density of 200kB / A4 page. By default, it requires a 600dpi printer, and a 600+dpi scanner. It has 3-of-12 bit redundancy using [Golay][5] codes, and spaces out the bits in an okay fashion.

Paperback gets a (theoretical) density of 500kB / A4 page. It needs a 600dpi printer, and a ~900dpi scanner.  It has configurable redundancy using [Reed-Solomon][6] codes. It looks completely unusable in practice (alignment issues, aside from being Windows-only).

Okay, so I think these are all stupid, because you need some custom software to decode them, which in any case where you’re decoding data stored on paper you probably don’t have that. I want to use standard barcodes, even if they’re going to be lower density. Let’s look at our options. I’m going to skip linear barcodes (low-density) and color barcodes (printing in color is expensive).  Since we need space between symbols, we want to pick the biggest versions of each code we can. For one, whitespace around codes is going to dominate actual code density for layout efficiency, and larger symbols are usually more dense. For another thing, we want to scan as few symbols as possible if we’re doing them one at a time.

[Aztec][7] From 15×15 to 151×151 square pixels. 1914 bytes maximum. Configurable Reed-Solomon error correction.

Density: 11.9 pixels per byte

[Data Matrix][8] From 10×10 to 144×144 square pixels. 1555 bytes maximum. Large, non-configurable error correction.

Density: 13.3 pixels per byte

[QR Code][9] From 21×21 to 177×177 square pixels. 2,953 bytes maximum. Somewhat configurable Reed-Solomon error correction.

Density: 10.6 pixels per byte

[PDF417][10] 17 height by 90-583 width.  1100 bytes maximum. Configurable Reed-Solomon error correction. PDF417 is a stacked linear barcode, and can be scanned by much simpler scanners instead of cameras. It also has built in cross-symbol linking (MacroPDF417), meaning you can scan a sequence of codes before getting output–handy for getting software to automatically link all the codes on a page.

Density: 9.01 pixels per byte

QR codes and PDF417 look like our contenders. PDF417 turns out to not scan well (at all, but especially at large symbol sizes), so despite some nice features let’s pick QR codes. Back when I worked on a [digital library][11] I made a component to generate QR codes on the fly, and I know how to scan them on my phone and webcam already from that, so it would be pretty easy to use them.

What density can we get on a sheet of A4 paper (8.25 in × 11.00 in, or 7.75in x 10.50in with half-inch margins)? I trust optar’s estimate (600 dpi = 200 pixels per inch) for printed/scanned pages since they seemed to test things. A max-size QR code is 144×144 pixels, or 0.72 x 0.72 inches at maximum density. We can fit 10 x 14 = 140 QR codes with maximum density on the page, less if we want decent spacing. That’s 140 QR codes x (2,953 bytes per QR code) = 413420 bytes = 413K per page before error correction.

That’s totally comparable to the other approaches above, and you can read the results with off-the-shelf software.  Bam.

[1]: http://ronja.twibright.com/optar
[2]: https://github.com/colindean/optar
[3]: http://ollydbg.de/Paperbak/index.html
[4]: http://en.wikipedia.org/wiki/Acid-free_paper
[5]: http://en.wikipedia.org/wiki/Binary_Golay_code
[6]: http://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction
[7]: http://en.wikipedia.org/wiki/Aztec_Code
[8]: http://en.wikipedia.org/wiki/Data_Matrix
[9]: http://en.wikipedia.org/wiki/QR_code
[10]: http://en.wikipedia.org/wiki/PDF417
[11]: https://blog.za3k.com/the-double-lives-of-books/ "The Double Lives of Books"
