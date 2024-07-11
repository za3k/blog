---
author: admin
categories:
- Technical
date: 2024-06-18 16:57:08-07:00
markup: html
source: wordpress
tags:
- linux
title: Even more URI handlers in Linux
updated: 2024-06-18 17:01:53-07:00
wordpress_id: 1403
wordpress_slug: even-more-uri-handlers-in-linux
---
Sometimes Linux wants to open files. I mostly use the command line, so I wrote some helper programs to open things in terminals.

-   `open-text-file` opens your default text editor in a terminal. I set it as my program to open all text files.
-   `open-directory` opens a terminal with that working directory. I set it as my program to open all directories.

They’re both available in [short-programs][1]. Both default to xterm.

[1]: https://github.com/za3k/short-programs?tab=readme-ov-file#open-directorytext-file
