---
author: admin
categories:
- Technical
date: 2021-06-11 17:50:31-07:00
markup: html
source: wordpress
tags:
- debian
- linux
- system administration
title: 'Encrypted root on debian part 2: unattended boot'
updated: 2021-06-11 18:12:38-07:00
wordpress_id: 630
wordpress_slug: encrypted-root-on-debian-part-2-unattended-boot
---
I want my debian boot to work as follows:

1.  If it’s in my house, it can boot without my being there. To make that happen, I’ll put the root disk key on a USB stick, which I keep in the computer.
2.  If it’s not in my house, it needs a password to boot. This is the normal boot process.

As in part 1, this guide is **debian-specific**. To learn more about the Linux boot process, see [part 1.][1]

First, we need to prepare the USB stick. Use ‘dmesg’ and/or ‘lsblk’ to make a note of the USB stick’s path (/dev/sdae for me). I chose to write to a filesystem rather than a raw block device.

    sudo mkfs.ext4 /dev/sdae # Make a filesystem directly on the device. No partition table.
    sudo blkid /dev/sdae # Make a note of the filesystem UUID for later

Next, we’ll generate a key.

    sudo mount /dev/sdae /mnt
    sudo dd if=/dev/urandom of=/mnt/root-disk.key bs=1000 count=8

Add the key to your root so it can actually decrypt things. You’ll be prompted for your password:

    sudo cryptsetup luksAddKey ROOT_DISK_DEVICE /mnt/root-disk.key

Make a script at /usr/local/sbin/unlockusbkey.sh

    #!/bin/sh
    USB_DEVICE=/dev/disk/by-uuid/a4b190b8-39d0-43cd-b3c9-7f13d807da48 # copy from blkid's output UUID=XXXX
    
    if [ -b $USB_DEVICE ]; then
      # if device exists then output the keyfile from the usb key
      mkdir -p /usb
      mount $USB_DEVICE -t ext4 -o ro /usb
      cat /usb/root-disk.key
      umount /usb
      rmdir /usb
      echo "Loaded decryption key from USB key." >&2
    else
      echo "FAILED to get USB key file ..." >&2
      /lib/cryptsetup/askpass "Enter passphrase"
    fi

Mark the script as executable, and optionally test it.

    chmod +x /usr/local/sbin/unlockusbkey.sh
    sudo /usr/local/sbin/unlockusbkey.sh | cmp /mnt/root-disk.key

Edit /etc/crypttab to add the script.

    root PARTLABEL=root_cipher none luks,keyscript=/usr/local/sbin/unlockusbkey.sh

Finally, re-generate your initramfs. I recommend either having a live USB or keeping a backup initramfs.

    sudo update-initramfs -u

\[1\] This post is loosely based on a chain of tutorials based on each other, including [this][2]  
\[2\] However, those collectively looked both out of date and like they were written without true understanding, and I wanted to clean up the mess. More definitive information was sourced from the actual [cryptsetup][3] documentation.

[1]: https://blog.za3k.com/migrating-an-existing-debian-installation-to-encrypted-root/
[2]: https://www.oxygenimpaired.com/ubuntu-with-grub2-luks-encrypted-lvm-root-hidden-usb-keyfile
[3]: https://cryptsetup-team.pages.debian.net/cryptsetup/README.initramfs.html
