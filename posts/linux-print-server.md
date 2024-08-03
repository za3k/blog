---
author: admin
categories:
- Technical
date: 2015-10-11 11:39:05-07:00
has-comments: false
source: wordpress
tags:
- linux
- printer
- system administration
title: Linux Print Server
updated: 2015-10-17 19:19:19-07:00
wordpress_id: 293
wordpress_slug: linux-print-server
---
So have you ever used a web printer and it was great?

…

Yeah, me neither. It’s probably possible on windows, but try to add more than one OS to the network and it’s horrible. And actually printing is a major pain in Linux anyway. Theoretically ‘lp’ and the like have no problem with remote printers, but I wanted something I understood. So today I’m going to post my setup I use instead.

I have a computer physically connected to the printer. Let’s call it ‘printserver’. On that server there is a folder, /printme, which is constantly monitored by inode. Any file added to that directory is printed.

Suppose I downloaded cutecats.pdf and I want to print it. Then I run:

```
scp cutecats.pdf printserver:/printme
```

And voila, the cute cats get printed.

---

Here’s the setup for the server:

1.  Get the printer to work. This is the hard step.
2.  Make a directory /printme. Add any missing users, add a new group called ‘print’ and add everyone who needs to print to that, etc.
3.  Set up /printme to be a tmpfs with the sticky bit set. (So we don’t fill up the hard drive)
    
    ```
    /etc/fstab
    tmpfs           /printme        tmpfs   rw,nodev,nosuid,noexec,uid=nobody,gid=print,mode=1770,size=1G  0       0
    ```
    
4.  Install incron and add this to the incrontab (of user ‘print’ or ‘sudo’):
    
    ```
    # incrontab -l
    /printme IN_CLOSE_WRITE,IN_MOVED_TO lp $@/$#
    ```
    
    Note that this will preserve files after they’re printed, because my server is low-volume enough I don’t need to care.
