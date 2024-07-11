---
author: admin
categories:
- Technical
date: 2022-03-22 09:28:49-07:00
markup: html
source: wordpress
tags:
- backup
- github
- qr codes
- qr-backup
- software
title: qr-backup
updated: 2022-03-22 09:29:32-07:00
wordpress_id: 731
wordpress_slug: qr-backup-2
---
qr-backup is a program to back up digital documents to physical paper. Restore is done with a webcam, video camera, or scanner. Someday smart phone cameras will work.

I’ve been making some progress on [qr-backup][1] v1.1. So far I’ve added:

-   `--restore`, which does a one-step restore for you, instead of needing a bash one-line restore process
-   `--encrypt` provides password-based encryption
-   An automatic restore check that checks the generated PDF. This is mostly useful for me while maintaining qr-backup, but it also provides peace-of-mind to users.
-   `--instructions` to give more fine-tuned control over printing instructions. There’s a “plain english” explanation of how qr-backup works that you can attach to the backup.
-   `--note` for adding an arbitrary message to every sheet
-   Base-64 encoding is now per-QR code, each QR is self-contained.
-   Codes are labeled N01/50 instead of 01/50, to support more code types in the future.
-   Code cleanup of QR generation process.
-   Several bugfixes.

v1.1 will be released when I make qr-backup feature complete:

-   Erasure coding, so you only need 70% of the QRs to do a restore.
-   Improve webcam restore slightly.

v1.2 will focus on adding a GUI and support for Windows, Mac, and Android. Switching off zbar is a requirement to allow multi-platform support, and will likely improve storage density.

[1]: https://github.com/za3k/qr-backup
