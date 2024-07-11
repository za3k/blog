---
author: admin
categories:
- Non-Technical
date: 2022-03-10 09:11:11-07:00
markup: html
source: wordpress
tags:
- archiving
- research
- slow
- usb
title: "USB Flash Longevity Testing \u2013 Year 2"
updated: 2022-03-10 09:22:34-07:00
wordpress_id: 726
wordpress_slug: usb-flash-longevity-testing-year-2
---
[Year 0][1] – I filled 10 32-GB Kingston flash drives with random data.  
[Year 1][2] – Tested drive 1, zero bit rot. Re-wrote the drive with the same data.  
Year 2 – Re-tested drive 1, zero bit rot. Tested drive 2, zero bit rot. Re-wrote both with the same data.

They have been stored in a box on my shelf, with a 1-month period in a moving van (probably below freezing) this year.

Will report back in 1 more year when I test the third 🙂

FAQs:

-   Q: Why didn’t you test more kinds of drives?  
    A: Because I don’t have unlimited energy, time and money :). I encourage you to!
-   Q: You know you powered the drive by reading it, right?  
    A: Yes, that’s why I wrote 10 drives to begin with. We want to see how something works if left unpowered for 1 year, 2 years, etc.
-   Q: What drive model is this?  
    A: The drive tested was “Kingston Digital DataTraveler SE9 32GB USB 2.0 Flash Drive (DTSE9H/32GBZ)” from Amazon, model DTSE9H/32GBZ, barcode 740617206432, WO# 8463411X001, ID 2364, bl 1933, serial id 206432TWUS008463411X001005. It was not used for anything previously–I bought it just for this test.
-   Q: Which flash type is this model?  
    A: We don’t know. If you do know, please tell me.
-   Q: What data are you testing with?  
    A: ([Repeatable][3]) randomly generated bits
-   Q: What filesystem are you using? / Doesn’t the filesystem do error correction?  
    A: I’m writing data directly to the drive using Linux’s block devices.

[1]: https://www.reddit.com/r/DataHoarder/comments/e3nb2r/longterm_reliability_testing/
[2]: https://www.reddit.com/r/DataHoarder/comments/lwgsdr/research_flash_media_longevity_testing_1_year/
[3]: https://github.com/za3k/short-programs#prng
