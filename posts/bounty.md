---
author: admin
categories:
- Technical
date: 2025-04-09
tags:
- qr-backup
title: 'qr-backup bounties'
---
I am offering two bounties to improve qr-backup. I think both are worth doing regardless.

My rewards are time-in-trade. You can use 5 or 10 hours of my time however you like. I usually charge over $100/hr, so this is a good deal.

If the github bugs are open, the bounties are unclaimed. I will try to update this post when they are claimed, too.

#### Bounty 1: Improve QR code scanning on Linux

Chances are, there is exactly one command-line program your distro has available to scan QR codes: [zbar](https://github.com/mchehab/zbar/)

Even on digitally-generated images, which are perfectly correct, pixel-aligned, and generally perfect, it still fails to read the codes sometimes. At least one-third of the bugs in the issue tracker are about this problem.

The bounty is to fix this issue in zbar, getting it to read QR codes with a 0% failure rate. The current failure rate is at least 0.1%.

A reproduction case and some debugging tips are [in the bounty details](https://github.com/mchehab/zbar/issues/306).

The reward is 10 hours of my time.

#### Bounty 2: Code a <s>one-page</s> short C program to restore qr-backup backups

qr-backup is designed to save to paper, and restore from the command-line.

but, it's possible that someday we might lose all the nice infrastructure we have today. 

- you want to restore your backup, but you're poor and don't have an internet connection
- no one runs "unix" any more. we just have neural meshes
- it's been 50 years and you can't figure out how to install all these programs no one has heard of like "zbar" and "qr-backup"
- your country has become a totalitarian state, and you can't be seen downloading "archiving" programs.
- you are a lizard-person who has recovered piles of paper from a previous civilization. what secrets could they hold?

who knows! wouldn't it be great if you could **still** restore?

this feature request is to add a printable, <s>1-page</s> short C program which you can type in by hand, compile, and use to restore backups from an image.

---

This is a very difficult technical challenge in minimization. You should provide a <s>1-page (2KB)</s> short version of qr-backup's restore process, written in C. Library use is not allowed. <s>Arguments will be accepted for other short programs if 2KB is impossible. </s>

Details are [in the bounty description](https://github.com/za3k/qr-backup/issues/70).

A short version of the steps:

- **Read QR codes**
- Sort them, remove duplicates
- Base64 decode each code
- **Erasure coding**
- Append and truncate
- **Decrypt**
- **Decompress**
- **Print SHA256 checksum**

qr-backup actually prints a bash one-liner to do the restore, if you prefer to reference that.

Each of the steps is done by qr-backup in the most standard way possible. Decompression calls `zcat`, for example. You should be able to re-use existing code easily, the challenge is just to shrink it.

The reward is 5 hours of my time and everlasting fame.
