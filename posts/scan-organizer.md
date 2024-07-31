---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-07-20 21:43:15-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- archiving
- linux
- physical
- software
title: Scan Organizer
updated: 2022-07-27 08:22:53-07:00
wordpress_id: 760
wordpress_slug: scan-organizer
---
I scan each and every piece of paper that passes through my hands. All my old to-do lists, bills people send me in the mail, the manual for my microwave, everything. I have a lot of scans.

**[scan-organizer](https://github.com/za3k/scan-organizer)** is a tool I wrote to help me neatly organize and label everything, and make it searchable. It’s designed for going through a huge backlog by hand over the course of weeks, and then dumping a new set of raw scans in whenever afterwards. I have a specific processing pipeline discussed below. However if you have even a little programming skill, I’ve designed this to be modified to suit your own workflow.

## [](https://github.com/za3k/scan-organizer#input-and-output)Input and output

The input is some raw scans. They could be handwritten notes, printed computer documents, photos, or whatever.

[![alt:A movie ticket stub](https://github.com/za3k/scan-organizer/raw/master/screenshots/sample_image.jpg)](https://github.com/za3k/scan-organizer/blob/master/screenshots/sample_image.jpg)

The final product is that for each file like `ticket.jpg`, we end up with `ticket.txt`. This has metadata about the file (tags, category, notes) and a transcription of any text in the image, to make it searchable with `grep` & co.

```
---
category: movie tickets
filename: seven psychopaths ticket.jpg
tags:
- cleaned
- categorized
- named
- hand_transcribe
- transcribed
- verified
---
Rialto Cinemas Elmwood
SEVEN PSYCHOPAT
R
Sun Oct 28 1
7:15 PM
Adult $10.50
00504-3102812185308

Rialto Cinemas Gift Cards
Perfect For Movie Lovers!
```

Here are some screenshots of the process. Apologizies if they’re a little big! I just took actual screenshots.

At any point I can exit the program, and all progress is saved. I have 6000 photos in the backlog–this isn’t going to be a one-session thing for me! Also, everything has keyboard shortcuts, which I prefer.

### [](https://github.com/za3k/scan-organizer#phase-1-rotating-and-cropping)Phase 1: Rotating and Cropping

[![alt:Phase 1: Rotating and Cropping](https://github.com/za3k/scan-organizer/raw/master/screenshots/phase1.png)](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase1.png)

First, I clean up the images. Crop them, rotate them if they’re not facing the right way. I can rotate images with keyboard shortcuts, although there are also buttons at the bottom. Once I’m done, I press a button, and *scan-organizer* advanced to the next un-cleaned photo.

### [](https://github.com/za3k/scan-organizer#phase-2-sorting-into-folders)Phase 2: Sorting into folders

[![alt:Phase 2: Sorting into folders](https://github.com/za3k/scan-organizer/raw/master/screenshots/phase2.png)](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase2.png)

Next, I sort things into folders, or “categories”. As I browse folders, I can preview what’s already in that folder.

### [](https://github.com/za3k/scan-organizer#phase-3-renaming-images)Phase 3: Renaming Images

[![alt:Phase 3: Renaming images](https://github.com/za3k/scan-organizer/raw/master/screenshots/phase3.png)](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase3.png)

Renaming images comes next. For convenience, I can browse existing images in the folder, to help name everything in a standard way.

### [](https://github.com/za3k/scan-organizer#phase-4-tagging-images)Phase 4: Tagging images

[![alt:Phase 4: Tagging images](https://github.com/za3k/scan-organizer/raw/master/screenshots/phase4.png)](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase4.png)

I tag my images with the type of text. They might be handwritten. Or they might be printed computer documents. You can imagine extending the process with other types of tagging for your use case.

### [](https://github.com/za3k/scan-organizer#not-done-ocr)Not yet done: OCR

Printed documents are run through OCR. This isn’t actually done yet, but it will be easy to plug in. I will probably use [tesseract](https://github.com/tesseract-ocr/tesseract).

### [](https://github.com/za3k/scan-organizer#phase-5-transcribing-by-hand)Phase 5: Transcribing by hand

[![alt:Phase 5a: Transcribing by Hand](https://github.com/za3k/scan-organizer/raw/master/screenshots/phase5.png)](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase5.png)

I write up all my handwritten documents. I have not found any useful handwriting recognition software. I just do it all by hand.

The point of **scan-organizer** is to filter based on tags. So only images I’ve marked as needing hand transcription are shown in this phase.

### [](https://github.com/za3k/scan-organizer#phase-6-verification)Phase 6: Verification

[](https://github.com/za3k/scan-organizer/blob/master/screenshots/phase6.png) At the end of the whole process, I verify that each image looks good, and is correctly tagged and transcribed.
