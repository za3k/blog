---
author: admin
categories:
- Technical
date: 2022-09-22 16:38:08-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- announcements
- qr-backup
- release
title: qr-backup v1.1
updated: 2022-11-05 15:50:36-07:00
wordpress_id: 792
wordpress_slug: qr-backup-v1-1
---
[qr-backup](https://github.com/za3k/qr-backup) v1.1 is released. qr-backup is a **command-line Linux program**. You can use it to back up a file as a series of QR codes. You can restore the QR codes using a webcam or scanner, and get back the original file.

[![](../wp-content/uploads/2022/09/image-1024x614.png)](../wp-content/uploads/2022/09/image.png)

The main features of qr-backup are ease-of-use and futureproofing (restore does not require qr-backup).

Please report any bugs [on github](https://github.com/za3k/qr-backup/issues). Once this is stable, I will do the first pip/package manager release. To test the alpha, check out the [latest code](https://github.com/za3k/qr-backup) using git.

See also [USAGE](https://github.com/za3k/qr-backup/blob/master/docs/USAGE.md) and *extensive* [FAQ](https://github.com/za3k/qr-backup/blob/master/docs/FAQ.md).

New features in v1.1:

-   Feature complete. New features are unlikely to be added. Future efforts will focus on quality, GUIs, and porting.
-   restore using qr-backup. Previously, the only restore was a bash one-liner (which still works).
    -   `qr-backup --restore` restores using the webcam
    -   `qr-backup --restore IMAGE IMAGE IMAGE` restores from scanned images
-   After generating a PDF backup, qr-backup automatically does a digital test of the restore process
-   Erasure coding. Lose up to 30% of QRs and restore will still work, as long as you are using qr-backup to restore
-   Increased code density, which about cancels out the erasure coding.
-   Back up directories and files. qr-backup makes a .tar file for you
-   Option to use password protection (encryption)
-   Option to print multiple copies of every QR code
-   Option to randomize order of QR codes
-   Optionally print extra cover sheet instructions on how to restore. For long-term archivists.
-   Option to add custom notes and labels to each page
-   Improved support for using qr-backup in a pipe
-   Various bugfixes
-   See [CHANGELOG](https://github.com/za3k/qr-backup/blob/master/CHANGELOG) for complete details

P.S. As a special request, if anyone is on OS X, let me know if it works for you?
