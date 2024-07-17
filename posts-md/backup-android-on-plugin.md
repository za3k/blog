---
author: admin
categories:
- Technical
date: 2015-04-23 23:03:49-07:00
markup: html
source: wordpress
tags:
- android
- arch linux
- backup
- linux
title: Backup android on plugin
updated: 2015-04-24 02:29:05-07:00
wordpress_id: 177
wordpress_slug: backup-android-on-plugin
---
In a [previous post](https://blog.za3k.com/android-backup-on-arch-linux/ "Android backup on arch linux") I discussed how to backup android with rsync. In this post, I’ll improve on that solution so it happens when you plug the phone in, rather than manually. My solution happens to know I have only one phone; you should adjust accordingly.

The process is

1.  Plug the phone in
2.  Unlock the screen (you’ll see a prompt to do this).
3.  Backup starts automatically
4.  Wait for the backup to finish before unplugging

First, let’s add a udev rule to auto-mount the phone when it’s plugged in and unlocked, and run appropriate scripts.

```
# 10-android.rules
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", ATTR{idProduct}=="4ee2", MODE="0660", GROUP="plugdev", SYMLINK+="android", RUN+="/usr/local/bin/android-connected"
ACTION=="remove", SUBSYSTEM=="usb", ENV{ID_MODEL}=="Nexus_4", RUN+="/usr/local/bin/android-disconnected"
```

Next, we’ll add android-connected and android-disconnected

```
#!/bin/bash
# /usr/local/bin/android-connected
if [[ "$1" != "-f" ]]
then
 echo "/usr/local/bin/android-connected -f" | /usr/bin/at now
 exit 0
fi

sudo -u zachary DISPLAY=:0 /usr/bin/notify-send "Android plugged in, please unlock."
sudo -u zachary /usr/local/bin/android-mountfs
sudo -u zachary DISPLAY=:0 /usr/bin/notify-send "Mounted, backing up..."
/usr/bin/flock /var/lock/phone-backup.pid sudo -u zachary /usr/local/bin/phone-backup-xenu
sudo -u zachary DISPLAY=:0 /usr/bin/notify-send "Backup completed."
```

```
# !/bin/sh
# /usr/local/bin/android-disconnected
#!/bin/sh
sudo -u zachary DISPLAY=:0 /usr/bin/notify-send "Android unplugged."
sudo -u zachary /usr/local/bin/android-umountfs
```

We’ll add something to mount and unmount the system. Keeping in mind that mounting only works when the screen is unlocked we’ll put that in a loop that checks if the mount worked:

```
#!/bin/sh
# /usr/local/bin/android-mountfs

android_locked()
{
ls /media/android 2>/dev/null >/dev/null
[ "$?" -eq 2 ]
}

jmtpfs /media/android # mount
while android_locked; do
  fusermount -u /media/android
  sleep 3
  jmtpfs /media/android # mount
done
```

```
#!/bin/sh
# /usr/local/bin/android-umountfs
fusermount -u /media/android
```

The contents of  /usr/local/bin/phone-backup are pretty me-specific so I’ll omit it, but it copies /media/android over to a server. (fun detail: MTP doesn’t show all information even on a rooted phone, so there’s more work to do)
