---
author: admin
categories:
- Technical
date: 2022-07-10 09:28:46-07:00
has-comments: false
source: wordpress
tags:
- backup
- linux
title: One Screenshot Per Minute
updated: 2022-07-10 09:37:53-07:00
wordpress_id: 748
wordpress_slug: one-screenshot-per-minute
---
One of my archiving and backup contingencies is taking one screenshot per minute. You can also use this to get a good idea of how you spend your day, by turning it into a movie. Although with a tiling window manager like I use, it’s a headache to watch.

I send the screenshots over to another machine for storage, so they’re not cluttering my laptop. It uses up 10-20GB per year.

I’ll go over my exact setup below in case anyone is interested in doing the same:

**/bin/screenlog**

```
GPG_KEY=Zachary
TEMPLATE=/var/screenlog/%Y-%m-%d/%Y-%m-%d.%H:%M:%S.jpg
export DISPLAY=:0
export XAUTHORITY=/tmp/XAuthority

IMG=$(\date +$TEMPLATE)
mkdir -p $(dirname "$IMG")
scrot "$IMG"
gpg --encrypt -r "$GPG_KEY" "$IMG"
shred -zu "$IMG"
```

The script

-   Prints everything to stderr if you run it manually
-   Makes a per-day directory. We store everything in /var/screenlog/2022-07-10/ for the day
-   Takes a screenshot. By default, crontab doesn’t have X Windows (graphics) access. To allow it, the XAuthority file which allows access needs to be somewhere my crontab can reliably access. I picked `/tmp/XAuthority`. It doesn’t need any unusual permissions, but the default location has some random characters in it.
-   [GPG](https://www.gnupg.org/)\-encrypts the screenshot with a public key and deletes the original. This is extra protection in case my backups somehow get shared, so I don’t literally leak all my habits, passwords, etc. I just use my standard key so I don’t lose it. It’s [public-key crypto](https://en.wikipedia.org/wiki/Public-key_cryptography), so put the public key on your laptop. Put the private key on neither, one, or both, depending on which you want to be able to read the photos.

**/etc/cron.d/screenlog**

```
* * * * * zachary  /bin/screenlog
20  * * * * zachary  rsync --remove-source-files -r /var/screenlog/ backup-machine:/data/screenlog/laptop
30  * * * * zachary  rmdir /var/screenlog/*
```

That’s

-   Take a screenshot once every minute. Change the first \* to \*/5 for every 5 minutes, and so on.
-   Copy over the gpg-encrypted screenshots hourly, deleting the local copy
-   Also hourly, delete empty per-day folders after the contents are copied, so they don’t clutter things

**~/.profile**

```
export XAUTHORITY=/tmp/XAuthority
```

I mentioned /bin/screenlog needs to know where XAuthority is. In Arch Linux this is all I need to do.
