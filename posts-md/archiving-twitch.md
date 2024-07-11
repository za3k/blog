---
author: admin
categories:
- Technical
date: 2015-10-19 22:33:34-07:00
markup: html
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

curl https://api.twitch.tv/kraken/channels/${TWITCH\_USER}/videos?broadcasts=true&limit=100 | 
  jq -r '.videos\[\].url' > past\_broadcasts.txt

Save them locally:

youtube-dl -a past\_broadcasts.txt -o "%(upload\_date)s.%(title)s.%(id)s.%(ext)s"

Did it. youtube-dl is smart enough to avoid re-downloading videos it already has, so as long as you run this often enough (I do daily), you should avoid losing videos before they’re deleted.

Thanks [jrayhawk][1] for the API info.

[1]: http://www.omgwallhack.org/home/jrayhawk/
