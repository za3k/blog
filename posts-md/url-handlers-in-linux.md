---
author: admin
categories:
- Technical
date: 2024-06-08 19:46:00-07:00
markup: html
source: wordpress
tags:
- linux
title: URI handlers in Linux
updated: 2024-06-09 08:22:47-07:00
wordpress_id: 1398
wordpress_slug: url-handlers-in-linux
---
When you click an email address, it automatically opens in your email client. But I don’t have an email client, I use webmail. I wrote a custom handler for Linux.  
  
First write a program to open [mailto](https://en.wikipedia.org/wiki/Mailto) links. Mailto links look like “**mailto:me@mail.com**” or maybe even “**mailto:me@mail.com?subject=mysubject&body=mybody**“. Test it by hand on a few links. Mine ([mailto-opener](https://github.com/za3k/short-programs?tab=readme-ov-file#mailto-opener)) composes a new message using my webmail.

Next, write a desktop file for the opener. Here’s one:

```
#/usr/local/share/applications/mailto-opener.desktop 
[Desktop Entry]
Type=Application
Name=mailto: link opener (github.com/za3k/short-programs)

# The executable of the application, possibly with arguments.
Exec=/home/zachary/.projects/short-programs/mailto-opener %u
```

Note the %u in the **Exec=** line. That’s required.

Now update your system mimetype database. On my Arch Linux install, I run

```
xdg-mime default mailto-opener.desktop x-scheme-handler/mailto
```

Finally, restart your browser. Really. Firefox and Chromium/Chrome both cache mimetype openers.

---

A related opener I added recently was for [magnet links](https://en.wikipedia.org/wiki/Magnet_URI_scheme), such as are popularly used for bittorrent.

```
~ $ cat /usr/local/share/applications/transmission-remote.desktop 
[Desktop Entry]
Type=Application
Name=transmission-remote magnet link opener
Exec=transmission-remote <TRANSMISSION INSTANCE> -a
```

`transmission-remote` is the name of a command-line Linux program. It connects to an instance of Tranmission (a popular torrent client) running on another machine.
