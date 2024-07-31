---
author: admin
categories:
- Technical
date: 2024-01-01 11:55:32-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- archiving
- research
- slow
- usb
title: "Flash media longevity testing \u2013 4 years later"
updated: 2024-01-01 11:55:32-07:00
wordpress_id: 1271
wordpress_slug: flash-media-longevity-testing-4-years-later
---
-   [Year 0](https://www.reddit.com/r/DataHoarder/comments/e3nb2r/longterm_reliability_testing/) – I filled 10 32-GB Kingston flash drives with random data.
-   [Year 1](https://www.reddit.com/r/DataHoarder/comments/lwgsdr/research_flash_media_longevity_testing_1_year/) – Tested drive 1, zero bit rot. Re-wrote drive 1 with the same data.
-   [Year 2](https://www.reddit.com/r/DataHoarder/comments/tb26cy/flash_media_longevity_testing_2_years_later/) – Tested drive 2, zero bit rot. Re-tested drive 1, zero bit rot. Re-wrote drives 1-2 with the same data.
-   [Year 3](https://www.reddit.com/r/DataHoarder/comments/102razr/flash_media_longevity_testing_3_years_later/) – Tested drive 3, zero bit rot. Re-tested drives 1-2, zero bit rot. Re-wrote drives 1-3 with the same data.
-   [Year 4](https://www.reddit.com/r/DataHoarder/comments/18w3bxw/flash_media_longevity_testing_4_years_later/) – Tested drive 4, zero bit rot. Re-tested drives 1-3, zero bit rot. Re-wrote drives 1-4 with the same data.

Will report back in **2 more years** when I test the fifth. Since flash drives are likely to last more than 10 years, the plan has never been “test one new one each year”.

The years where I’ll first touch a new drive (assuming no errors) are: **1, 2, 3, 4,** 6, 8, 11, 15, 20, 27

The full test plan:

```
YEAR 1: read+write  1                           [1s]
YEAR 2: read+write  1, 2                        [1s]
YEAR 3: read+write  1, 2, 3                     [1s]
YEAR 4: read+write  1, 2, 3, 4                  [2s] (every 2nd year)
year 5: read+write  1, 2, 3,
YEAR 6: read+write  1, 2, 3, 4  5               [2s]
year 7: read+write  1, 2, 3,
YEAR 8: read+write  1, 2, 3, 4, 5, 6            [2s]
year 9: read+write  1, 2, 3,
year 10: read+write 1, 2, 3, 4, 5, 6
YEAR 11: read+write 1, 2, 3,         7          [4s]
year 12: read+write 1, 2, 3, 4, 5, 6
year 13: read+write 1, 2, 3
year 14: read+write 1, 2, 3, 4, 5, 6
YEAR 15: read+write 1, 2, 3,         7, 8       [4s]
year 16: read+write 1, 2, 3, 4, 5, 6
year 17: read+write 1, 2, 3
year 18: read+write 1, 2, 3, 4, 5, 6
year 19: read+write 1, 2, 3,         7, 8
YEAR 20: read+write 1, 2, 3, 4, 5, 6       9    [8s]
year 21: read+write 1, 2, 3
year 22: read+write 1, 2, 3, 4, 5, 6
read 23: read+write 1, 2, 3          7, 8
year 24: read+write 1, 2, 3, 4, 5, 6
year 25: read+write 1, 2, 3
year 26: read+write 1, 2, 3, 4, 5, 6
YEAR 27: read+write 1, 2, 3          7, 8,   10 [8s]
year 28: read+write 1, 2, 3, 4, 5, 6       9
year 29+: repeat years 21-28
```

FAQ: [https://blog.za3k.com/usb-flash-longevity-testing-year-2/](https://blog.za3k.com/usb-flash-longevity-testing-year-2/)
