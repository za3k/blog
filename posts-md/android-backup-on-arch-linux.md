---
author: admin
categories:
- Technical
date: 2014-11-23 13:51:31-07:00
markup: html
source: wordpress
tags:
- android
- arch linux
- backup
- phone
- system administration
title: Android backup on arch linux
updated: 2015-04-24 02:41:58-07:00
wordpress_id: 63
wordpress_slug: android-backup-on-arch-linux
---
Edit: See [here][1] for an automatic version of the backup portion.

Connecting android to Windows and Mac, pretty easy. On arch linux? Major pain. Here’s what I did, mostly via the help of the [arch wiki][2]:

1.  Rooted my phone. Otherwise you can’t back up major parts of the file system (including text messages and most application data) \[EDIT: Actually, you can’t back these up over MTP even once you root your phone. Oops.\]
2.  Installed [jmtpfs][3], a FUSE filesystem for mounting MTP, the new alternative to mount-as-storage on portable devices.
3.  Enabled ‘user\_allow\_other’ in /etc/fuse.conf. I’m not sure if I **needed** to, but I did.
4.  Plugged in the phone, and mounted the filesystem:
    
    jmtpfs /media/android
    
    The biggest pitfall I had was that if the phone’s screen is not unlocked at this point, mysterious failures will pop up later.
    
5.  Synced the contents of the phone. For reasons I didn’t diagnose (I assume specific to FUSE), this actually fails as root:
    
    rsync -aAXv --progress --fake-super --one-file-system /media/android --delete --delete-excluded "$SYNC\_DESTINATION"
    

1.  Pingback: [Backup android on plugin | Optimal Prime][4]
    

[1]: https://blog.za3k.com/backup-android-on-plugin/ "Backup android on plugin"
[2]: https://wiki.archlinux.org/index.php/MTP "arch wiki"
[3]: https://aur.archlinux.org/packages/jmtpfs/ "jmtpfs"
[4]: https://blog.za3k.com/backup-android-on-plugin/
