---
author: admin
categories:
- Technical
date: 2015-04-13 17:46:31-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- boot
- installer
- iso
- os
- system administration
- windows
- windows xp
title: XP Boot USB Stick
updated: 2015-04-13 17:51:06-07:00
wordpress_id: 158
wordpress_slug: xp-boot-usb-stick
---
Most of the following taken from : [http://www.msfn.org/board/topic/151992-install-xp-from-usb-without-extra-tools/](http://www.msfn.org/board/topic/151992-install-xp-from-usb-without-extra-tools/), just modified to include syslinux support.

Let me know if there are any omissions; it an XP installer bluescreens on boot for me so I can’t actually test.

1.  Obtain an XP iso file
2.  Format drive with one FAT parition, marked bootable.
3.  
    ```
    syslinux -i /dev/sdXX
    ```
    
4.  
    ```
    $ cp /usr/lib/syslinux/bios/mbr.bin >/dev/sdX
    ```
    
5.  
    ```
    $ mount /dev/sdXX /mnt
    ```
    
6.  
    ```
    mkdir /tmp/xp_iso
    mount xp.iso /tmp/xp_iso
    cp -ar /tmp/xp_iso/* /mnt
    umount /tmp/xp_iso
    rmdir xp_iso
    ```
    
7.  
    ```
    cp /usr/lib/syslinux/bios/{chain.c32,libutil.c32,menu.c32,libcom.c32} /mnt
    ```
    
8.  
    ```
    cp /mnt/I386/{NTDETECT.COM,SETUPLDR.BIN,TXTSETUP.SIF} /mnt
    ```
    
9.  Edit /mnt/syslinux.cfg:
    
    ```
    UI menu.c32# Windows XP
    LABEL windows_xp
    MENU LABEL Run Windows ^XP Setup
    COM32 chain.c32
    APPEND fs ntldr=SETUPLDR.BIN
    ```
    
10.  
    ```
    umount /mnt
    ```
    
11. Boot from the USB stick
