---
author: admin
categories:
- Technical
date: 2021-06-11 13:28:52-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- debian
- linux
- system administration
title: Migrating an existing debian installation to encrypted root
updated: 2021-06-11 18:06:48-07:00
wordpress_id: 606
wordpress_slug: migrating-an-existing-debian-installation-to-encrypted-root
---
In this article, I migrate an existing debian 10 buster release, from an unencrypted root drive, to an encrypted root. I used a second hard drive because it’s safer–this is NOT an in-place migration guide. We will be encrypting / (root) only, not /boot. My computer uses UEFI. This guide **is specific to debian**–I happen to know these steps would be different on Arch Linux, for example. They probably work great on a different debian version, and might even work on something debian-based like Ubuntu.

In [part 2](https://blog.za3k.com/encrypted-root-on-debian-part-2-unattended-boot/), I add an optional extra where root decrypts using a special USB stick rather than a keyboard passphrase, for unattended boot.

Apologies if I forget any steps–I wrote this after I did the migration, and not during, so it’s not copy-paste.

Q: Why aren’t we encrypting /boot too?

1.  Encrypting /boot doesn’t add much security. Anyone can guess what’s on my /boot–it’s the same as on everyone debian distro. And encrypting /boot doesn’t prevent tampering–someone can easily replace my encrypted partition by an unencrypted one without my noticing. Something like [Secure Boot](https://www.rodsbooks.com/efi-bootloaders/secureboot.html) would resist tampering, but still doesn’t require an encrypted /boot.
2.  I pull a special trick in [part 2](https://blog.za3k.com/encrypted-root-on-debian-part-2-unattended-boot/). Grub2’s has new built-in encryption support, which is what would allow encrypting /boot. But grub2 can’t handle keyfiles or keyscripts as of writing, which I use.

**How boot works**

For anyone that doesn’t know, here’s how a typical boot process works:

1.  Your computer has built-in firmware, which on my computer meets a standard called UEFI. On older computers this is called BIOS. The firmware is built-in, closed-source, and often specific to your computer. You can replace it with something open-source if you wish.
2.  The firmware has some settings for what order to boot hard disks, CD drives, and USB sticks in. The firmware tries each option in turn, failing and using the next if needed.
3.  At the beginning of each hard disk is a *partition table*, a VERY short info section containing information about what partitions are on the disk, and where they are. There are two partition table types: MBR (older) and GPT (newer). UEFI can only read GPT partition tables. The first thing the firmware does for each boot disk is read the partition table, to figure out which partitions are there.
4.  For UEFI, the firmware looks for an “EFI” partition on the boot disk–a special partition which contains bootloader executables. EFI always has a FAT filesystem on it. The firmware runs an EFI executable from the partition–which one is configured in the UEFI settings. In my setup there’s only one executable–the grub2 bootloader–so it runs that without special configuration.
5.  Grub2 starts. The first thing Grub2 does is… read the partition table(s) again. It finds the /boot partition, which contains grub.cfg, and reads grub.cfg. (There is a file in the efi partition right next to the executable, which tells grub where and how to find /boot/grub.cfg. This second file is confusingly also called grub.cfg, so let’s forget it exists, we don’t care about it).
6.  Grub2 invokes the Linux Kernel specified in grub.cfg, with the options specified in grub.cfg, including the an option to use a particular initramfs. Both the Linux kernel and the initramfs are also in /boot.
7.  Now the kernel starts, using the initramfs. initramfs is a tiny, compressed, read-only filesystem only used in the bootloading process. The initramfs’s only job is to find the real root filesystem and open it. grub2 is pretty smart/big, which means initramfs may not have anything left to do on your system before you added encryption. **If you’re doing decryption, it happens here.** This is also how Linux handles weird filesystems (ZFS, btrfs, squashfs), some network filesystems, or hardware the bootloader doesn’t know about. At the end of the process, we now have switched over to the REAL root filesystem.
8.  The kernel starts. We are now big boys who can take care of ourselves, and the bootloading process is over. The kernel always runs /bin/init from the filesystem, which on my system is a symlink to systemd. This does all the usual startup stuff (start any SSH server, print a bunch of messages to the console, show a graphical login, etc).

**Setting up the encrypted disk**

First off, I used TWO hard drives–this is not an in-place migration, and that way nothing is broken if you mess up. One disk was in my root, and stayed there the whole time. The other I connected via USB.

Here’s the output of `gdisk -l` on my original disk:

```
Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048         1050623   512.0 MiB   EF00  # EFI, mounted at /boot/efi
   2         1050624       354803711   168.7 GiB   8300  # ext4, mounted at /
   3       354803712       488396799   63.7 GiB    8200  # swap
```

Here will be the final output of `gdisk -l` on the new disk:

```
Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048          526335   256.0 MiB   EF00  efi # EFI, mounted at /boot/efi
   2         1050624       135268351   64.0 GiB    8200  swap # swap
   3       135268352       937703054   382.6 GiB   8300  root_cipher # ext4-on-LUKS. ext4 mounted at /
   4          526336         1050623   256.0 MiB   8300  boot # ext4, mounted at /boot
```

1.  Stop anything else running. We’re going to do a “live” copy from the running system, so at least stop doing anything else. Also most of the commands in this guide need root (`sudo`).
2.  Format the new disk. I used `gdisk` and you must select a gpt partition table. Basically I just made everything match the original. The one change I need is to add a /boot partition, so grub2 will be able to do the second stage. I also added partition labels with the `c` gdisk command to all partitions: boot, root\_cipher, efi, and swap. I decided I’d like to be able to migrate to a larger disk later without updating a bunch of GUIDs, and filesystem or partition labels are a good method.
3.  Add encryption. I like filesystem-on-LUKS, but most other debian guides use filesystem-in-LVM-on-LUKS. You’ll enter your new disk password twice–once to make an encrypted partition, once to open the partition.  
    ```
    cryptsetup luksFormat /dev/disk/by-partlabel/root_cipher
    cryptsetup open /dev/disk-by-partlabel/root_cipher root
    ```
4.  Make the filesystems. For my setup:  
    ```
    mkfs.ext4 /dev/disk/by-partlabel/root
    mkfs.ext4 /dev/disk/by-partlabel/boot  
    mkfs.vfat /dev/disk/by-partlabel/efi
    ```
5.  Mount all the new filesystems at `/mnt`. Make sure everything (cryptsetup included) uses EXACTLY the same mount paths (ex /dev/disk/by-partlabel/boot instead of /dev/sda1) as your final system will, because debian will examine your mounts to generate boot config files.
    ```
    mount /dev/disk/by-partlabel/root /mnt
    mkdir /mnt/boot && mount /dev/disk/by-partlabel/boot /mnt/boot 
    mkdir /mnt/boot/efi && mount /dev/disk/by-partlabel/efi /mnt/boot/efi
    mkdir /mnt/dev && mount --bind /dev /mnt/dev # for chroot
    mkdir /mnt/sys && mount --bind /sys /mnt/sys
    mkdir /mnt/proc && mount --bind /dev /mnt/proc
    ```
6.  Copy everything over. I used `rsync -axAX`, but you can also use `cp -ax`. To learn what all these options are, read the man page. Make sure to keep the trailing slashes in the folder paths for rsync.  
    ```
    rsync -xavHAX / /mnt/ --no-i-r --info=progress2
    rsync -xavHAX /boot/ /mnt/boot/
    rsync -xavHAX /boot/efi/ /mnt/boot/efi/
    ```
7.  Chroot in. You will now be “in” the new system using your existing kernel.  
    `chroot /mnt`
8.  Edit /etc/crypttab. Add:  
    `root PARTLABEL=root_cipher none luks`
9.  Edit /etc/fstab. Mine looks like this:  
    ```
    /dev/mapper/root / ext4 errors=remount-ro 0 1
    PARTLABEL=boot /boot ext4 defaults,nofail 0 1
    PARTLABEL=efi /boot/efi vfat umask=0077,nofail
    PARTLABEL=swap none swap sw,nofail 0 0
    tmpfs /tmp tmpfs mode=1777,nosuid,nodev 0 0
    ```
10.  Edit /etc/default/grub. On debian you don’t need to edit `GRUB_CMDLINE_LINUX`.  
    ```
    GRUB_DISABLE_LINUX_UUID=true
    GRUB_ENABLE_LINUX_PARTLABEL=true
    ```
11.  Run `grub-install`. This will install the bootloader to efi. I forget the options to run it with… sorry!
12.  Run `update-grub` (with no options). This will update /boot/grub.cfg so it knows how to find your new drive. You can verify the file by hand if you know how.
13.  Run `update-initramfs` (with no options). This will update the initramfs so it can decrypt your root drive.
14.  If there were any warnings or errors printed in the last three steps, something is wrong. Figure out what–it won’t boot otherwise. Especially make sure your /etc/fstab and /etc/crypttab *exactly* match what you’ve already used to mount filesystems.
15.  Exit the chroot. Make sure any changes are synced to disk (you can unmount everything under /mnt in reverse order to make sure if you want)
16.  Shut down your computer. Remove your root disk and boot from the new one. It should work now, asking for your password during boot.
17.  Once you boot successfully and verify everything mounted, you can remove the `nofail` from /etc/fstab if you want.
18.  (In my case, I also set up the swap partition after successful boot.) Edit: Oh, also don’t use unencrypted swap with encrypted root. That was dumb.
