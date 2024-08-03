---
author: admin
categories:
- Technical
date: 2014-11-23 13:14:46-07:00
has-comments: false
source: wordpress
tags:
- backup
- email
- gmail
title: Archiving gmail
updated: 2014-11-23 13:14:46-07:00
wordpress_id: 59
wordpress_slug: archiving-gmail
---
I set up an automatic archiver for gmail, using the special-purpose tool [gm-vault](http://gmvault.org/). It was fairly straightforward, no tutorial here. The daily sync:

```
@daily cd ~gmail && cronic gmvault sync -d "/home/gmail/vanceza@gmail.com" vanceza@gmail.com
```

I’m specifying a backup folder here (-d) so I can easily support multiple accounts, one per line.

[Cronic](http://habilis.net/cronic/ "Cronic") is a tool designed to make cron’s default email behavior better, so I get emailed only on actual backup failures.
