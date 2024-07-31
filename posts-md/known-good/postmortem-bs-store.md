---
author: admin
categories:
- Technical
date: 2020-05-12 14:00:28-07:00
markup: html
source: wordpress
tags:
- immutable
- linux
- postmortem
- storage
title: 'Postmortem: bs-store'
updated: 2020-05-17 12:52:32-07:00
wordpress_id: 523
wordpress_slug: postmortem-bs-store
---
Between 2020-03-14 and 2020-12-03 I ran an experimental computer storage setup. I movied or copied 90% of my files into a content-addressable storage system. I’m doing a writeup of why I did it, how I did it, and why I stopped. My hope is that it will be useful to anyone considering using a similar system.

The assumption behind this setup, is that 99% of my files never change, so it’s fine to store only one, static copy of them. (Think movies, photos… they’re most of your computer space, and you’re never going to modify them). There are files you change, I just didn’t put them into this system. If you run a database, this ain’t for you.

Because I have quite a lot of files and 42 drives (7 in my computer, ~35 in a huge media server chassis), there is a problem of how to organize files across drives. To explain why it’s a problem, let’s look at the two default approaches:

-   **One Block Device / RAID 0**. Use some form of system that unifies block devices, such as RAID0 or a ZFS’s striped vdevs. Writing files is very easy, you see a single 3000GB drive.
    -   Many forms of RAID0 use striping. Striping splits each file across all available drives. 42 drives could spin up to read one file (wasteful).
    -   You need all the drives mounted to read anything–I have ~40 drives, and I’d like a solution that works if I move and can’t keep my giant media server running. Also, it’s just more reassuring that nothing can fail if you can read each drive individually.
-   **JBOD / Just a Bunch of Disks**. Label each drive with a category (ex. ‘movies’), and mount them individually.
    -   It’s hard to aim for 100% (or even >80%) drive use. Say you have 4x 1000GB drives, and you have 800GB movies, 800GB home video footage, 100GB photographs, and 300GB datasets. How do you arrange that? One drive per dataset is pretty wasteful, as everything fits on 3. But, with three drives, you’ll need to split at least one dataset across drives. Say you put together 800GB home video and 100GB photographs. If you get 200GB more photographs, do you split a 300 GB collection across drives, or move the entire thing to another drive? It’s a lot of manual management and shifting things around for little reason.

Neither approach adds any redundancy, and 42 drives is a bit too many to deal with for most things. Step 1 is to split the 42 drives into 7 ZFS vdevs, each with 2-drive redundancy. That way, if a drive fails or there is a small data corruption (likely), everything will keep working. So now we only have to think about accessing 7 drives (but keep in mind, many physical drives will spin up for each disk access).

The ideal solution:

-   Will not involve a lot of manual management
-   Will fill up each drive in turn to 100%, rather than all drives at an equal %.
-   Will deduplicate identical content (this is a “nice to have”)
-   Will only involve accessing one drive to access one file
-   Will allow me to get and remove drives, ideally across heterogenous systems.

I decided a content-addressable system was ideal for me. That is, you’d look up each file by its hash. I don’t like having an extra step to access files, so files would be accessed by symlink–no frontend program. Also, it was important to me that I be able to transparently swap out the set of drives backing this. I wanted to make the content-addressable system basically a set of 7 content-addressable systems, and somehow wrap those all into one big content-addressable system with the same interface. Here’s what I settled on:

-   (My drives are mounted as /zpool/bs0, /zpool/bs1, … /zpool/bs6)
-   Files will be stored in each pool in turn by hash. So my movie ‘cat.mpg’ with sha hash ‘8323f58d8b92e6fdf190c56594ed767df90f1b6d’ gets stored in /zpool/bs0/83/23/f58d8b9 \[shortened for readability\]
-   Initially, we just copy files into the content-addressable system, we don’t delete the original. I’m cautious, and I wanted to make everything worked before getting rid of the originals.
-   To access a file, I used read-only unionfs-fuse for this. This checks each of /zpool/bs{0..6}/\<hash\> in turn. So in the final version, /data/movies/cat.mpg would be a symlink to ‘/bs-union/83/23/f58d8b9’
-   We store some extra metadata on the original file (if not replaced by a symlink) and the storied copy–what collection it’s part of, when it was added, how big it is, what it’s hash is, etc. I chose to use xattrs.

The plan here is that it would be really easy to swap out one backing blockstore of 30GB, for two of 20GB–just copy the files to the new drives and add it to the unionfs.

Here’s what went well:

-   No problems during development–only copying files meant it was easy and safe to debug prototypes.
-   Everything was trivial to access (except see note about mounting disks below)
-   It was easy to add things to the system
-   Holding off on deleting the original content until I was 100% out of room on my room disks, meant it was easy to migrate off of, rather risk-free
-   Running the entire thing on top of zfs ZRAID2 was the right decision, I had no worries about failing drives or data corruption, despite a lot of hardware issues developing at one point.
-   My assumption that files would never change was correct. I made the unionfs filesystem read-only as a guard against error, but it was never a problem.
-   Migrating off the system went smoothly

Here are the implementation problems I found

-   I wrote the entire thing as bash scripts operating directly on files, which was OK for access and putting stuff in the store, but just awful for trying to get an overview of data or migrating things. I definitely should have used a database. I maybe should have used a programming language.
-   Because there was no database, there wasn’t really any kind of regular check for orphans (content in the blobstore with no symlinks to it), and other similar checks.
-   unionfs-fuse suuucks. Every union filesystem I’ve tried sucks. Its read bandwidth is much lower than the component devices (unclear, probably), it doesn’t cache where to look things up, and it has zero xattrs support (can’t read xattrs from the underlying filesystem).
-   gotcha: zfs xattrs waste a lot of space by default, you need to reconfigure the default.

But the biggest problem was disk access patterns:

-   I thought I could cool 42 drives spinning, or at least a good portion of them. This was WRONG by far, and I am not sure how possible it is in a home setup. To give you an idea how bad this was, I had to write a monitor to shut off my computer if the drives went above 60C, and I was developing fevers in my bedroom (where the server is) from overheating. Not healthy.
-   unionfs has to check each backing drive. So we see 42 drives spin up. I have ideas on fixing this, but it doesn’t deal with the other problems
-   To fix this, you could use double-indirection.
    -   Rather than pointing a symlink at a unionfs: /data/cat.mpg -> /bs-union/83/23/f58d8b9 (which accesses /zpool/bs0/83/23/f58d8b9)
    -   Point a symlink at another symlink that points directly to the data: /data/cat.mpg -> /bs-indirect/83/23/f58d8b9 -> /zpool/bs0/83/23/f58d8b9
-   The idea is that backing stores are kinda “whatever, just shove it somewhere”. But, actually it would be good to have a collection in one place–not only to make it easy to copy, but to spin up only one drive when you go through everything in a collection. It might even be a good idea to have a separate drive for more frequently-accessed content. This wasn’t a huge deal for me since migrating existing content meant it coincidentally ended up pretty localized.
-   Because I couldn’t spin up all 42 drives, I had to keep a lot of the array unmounted, and mount the drives I needed into the unionfs manually.

So although I could have tried to fix things with double-indirection, I decided there were some other disadvantages to symlinks: estimating sizes, making offsite backups foolproof. I decided to migrate off the system entirely. The migration went well, although it required running all the drives at once, so some hardware errors popped up. I’m currently on a semi-JBOD system (still on top of the same 7 ZRAID2 devices).

Hopefully this is useful to someone planning a similar system someday. If you learned something useful, or there are existing systems I should have used, feel free to leave a comment.
