---
author: admin
categories:
- Technical
date: 2015-10-19 22:33:34-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- backup
- linux
- osx
- twitch
title: Archiving Twitch
updated: 2015-10-19 23:12:30-07:00
wordpress_id: 327
wordpress_slug: archiving-twitch
---
Install jq and youtube-dl

Get a list of the last 100 URLs:

```
curl https://api.twitch.tv/kraken/channels/${TWITCH_USER}/videos?broadcasts=true&limit=100 | 
  jq -r '.videos[].url' > past_broadcasts.txt
```

Save them locally:

```
youtube-dl -a past_broadcasts.txt -o "%(upload_date)s.%(title)s.%(id)s.%(ext)s"
```

Did it. youtube-dl is smart enough to avoid re-downloading videos it already has, so as long as you run this often enough (I do daily), you should avoid losing videos before they’re deleted.

Thanks [jrayhawk](http://www.omgwallhack.org/home/jrayhawk/) for the API info.
