---
author: admin
categories:
- Non-Technical
date: 2015-06-28 17:07:34-07:00
markup: html
source: wordpress
tags:
- review
- yearly review
title: Year in Review
updated: 2020-05-17 12:57:07-07:00
wordpress_id: 229
wordpress_slug: year-in-review
---
Sep, Oct, Nov 2014: Vietnam.

A year ago, I left my job at Streak and moved to Vietnam. I felt like I needed change. Vietnam ended up being wonderful; I was really glad I travelled with my friends [Richard][1] and [Kathy][2], which ended up making the experience a hundred times better than it would have been otherwise. The basic environment was: everything is cheap, I newly have endless free time, I was automatically prompted by my friends in the evenings and sometimes during the day to go on small novel adventures involving physical activity, and I had little internet access. This is probably my perfect environment, and I was functioning very well (the vietnamese diet also has small, well-balanced meals which might have helped). For some reason, I was also able to intensely single-task. \[I’d like to write more about what Vietnam is like, but this article is quite long enough as it is\]

While I was in Vietnam, I made a to-do list. The to-do list had all the burning projects I actually wanted to do. I’ve ended up accomplishing most of them, at a rate of one every week or two, and it’s a decent summary of what I’ve been doing since. Two things made the to-do list a success. First, it had BIG tasks. These are projects like my recent “set up an IRC server” or “start a publishing company”. Because of that, I don’t get bogged down in minutae, and the tasks are always motivating. I find I function better when I try to carefully plan around having any logistics. The second reason, which I realized today, is that I was very careful to only include tasks I was planning to do (subtly different than tasks I wanted to do). The list was descriptive, not normative, although it certainly included some things like doing taxes I wasn’t wild about.

Looking at my journal and it really only starts up again in March, so I’m going to organize this post in terms of the to-do list. There are a couple items that don’t fit:

-   I started dating my wonderful pet, [Lealend][3], while I was in Vietnam. I went to visit them for a month in Puerto Rico where they live. This is very very important to me (the most important thing that happened in the last year), but I don’t usually write about things that personal on my blog so I’m not doing to say much. I’ve been emotionally maturing a lot by being with them.
-   Conventions. I went to [DEF CON][4], which was probably the best single week this year so far. I’m definitely going again next year. I attended a [mirix][5] \[paper\] in the South Bay, which ended up being stressful for transportation-related reasons but really good while I was there. I’m planning on going to [Burning Man][6] this year as well.
-   I started contracting, that’s how I’ve been alive for a year. I’ve been doing some work for [Zinc][7] and [Paul Christiano][8] on a [workflowy clone][9], mostly. I work two hours a day average.
-   I’ve been developing a [minecraft modpack][10] \[I’ll write more about this when it’s stable\], and recently taken an interest in livestreaming.

Now on to the to-do list.

-   Project: Printserver  
    Success: Success but obsolete  
    Description: I set up a printserver. It’s a little raspberry pi that talks to my printer, because getting printers set up is a pain and I don’t want to do it all the time. It went great, it saved me a ton of hassle to have it automatically print out my daily agenda every morning, and to just be able to transfer documents over with ‘scp’.  
    Future plans: Unfortunately, my printer died and we only recently got a new one. I need to set it up with the new server. I could also make printing completely automatic when new files show up with scp (right now it’s manual so I can switch out paper, but my roommates would be happier with scp I think).
    
-   Project: Set up my phone so dropping/losing it isn’t horrible  
    Success: Partial success  
    Description: I wanted to root and then [automatically backup][11] my phone. I did figure out how to do as much backing up as I can, and it is automatic. Unfortunately it turns out most of the filesystem (including SMS) just isn’t available over [Media Transfer Protocol][12] which android uses to display files, so I had to special case the things I desperately needed backed up. I’d prefer the state of the world let me back up everything on the phone, but that’s as much work as I’m willing to do.
    
-   Project: Get digital copies of all books I own  
    Success: Success  
    Description: I got digital copies of all books I own via a combination of pirating, buying copies, and getting the books scanned by a service. I did *not* get rid of the physical books.
    
-   Project: Switch to private email  
    Success: Not done  
    Description: I get a little nervous entrusting Google (or any third party) with the ability to read, lose, or add restrictions on what I can do with my email. I want to set up my own email address ([za3k@za3k.com][13]) and have it be my main point of contact. My email does work, but I can’t send outgoing email, and I haven’t switched everything over to it for that reason.
    
-   Project: Download ArXiV  
    Success: Done  
    Description: As an [archive nut][14], I worry that the [ArXiV][15] collection, one of the nicer collections of scientific papers I access regularly, might someday go down or get censored. I downloaded a copy and stashed it away somewhere. Unfortunately ArXiV’s licenses they get papers under doesn’t permit redistribution, so I can’t publicly host it. (This was really cool but I had to decide whether I was going to publicly mention, since it’s a legal gray area)  
    Future plans: Someone (not me) should host a torrent. Contact me and I can get you a copy.
    
-   Project: Pack and unpack storage bins (trip to vietnam)  
    Success: Success  
    Description: Okay I know this sounds stupid, but I spent about a month packing up to go to Vietnam, and all my physical stuff has stayed organized ever since. That’s a really big change for me.
    
-   Project: Host an IRC server  
    Success: [Success][16]
    
-   Project: Make hibernate work on my laptop  
    Success: Success  
    Description: This involved switching partitioning around since btrfs doesn’t support swap files. If I recall, my setup is now a swap partition and a root btrfs partition, inside LVM, inside LUKS.
    
-   Project: Extract bitcoins  
    Success: Success  
    Description: Extract bitcoins from all my computers and centralize them in one place
    
-   Project: iPhone  
    Success: Success  
    Description: Back up all my personal data from my iPhone, clear the contents, and sell it.
    
-   Project: N-grams  
    Success: Obsolete  
    Description: The [Google N-grams dataset][17] from their book scanning project is freely available, but in a terrible format (split across set-size file chunks, but in random rather than sorted order). My plan was to convert the formatting and offer it as a torrent / s3 bucket. Google has corrected the problem in a revised version of the dataset.
    
-   Project: NNTP over tor  
    Success: Didn’t do  
    Description: I run a private newsserver, and I wanted to let people access the newsserver (and anything else on that physical server) over tor. I decided the newsserver was too dead to bother with, and I didn’t feel enthusiastic about setting up tor, so I dropped the project.  
    Future plans: I don’t care about the original project, but if there’s a compelling stimulus, I want to set up tor for my server to learn how and leave flexibility.
    
-   Project: Textmode backup  
    Success: Success  
    Description: ‘textmode’ is the name of a virtual machine on my OS X machine. The project was to back up contents of the machine once, and then delete the virtual machine
    
-   Project: Post pdfmailer website  
    Success: Success  
    Description: I wanted people to be able to get a physical copy of a pdf document they had mailed to them. I think this project was an especial success, because I’d been failing at an over-engineered version of this off and on for a year. I decided to have the website email me instead of trying to do everything automatically, and ended up getting the books to be a factor of 10 cheaper or so by going with a publisher with no API.  
    Future plans: I’d like to popularize the website more. I think there are also some small technical improvements to be made. I’m not going to automate things unless it starts using up a lot of my time to process requests myself.
    
-   \[Censored project involving an arbitrage opportunity I haven’t cornered\]
-   Project: Back up email  
    Success: [Success][18]
-   Project: Flatten backups  
    Success: Good enough  
    Description: Oh just go read the [XKCD][19]. Now imagine you’ve been archiving computers onto other computers for 15 years, and buy cheap laptops.
    
-   Project: QR codes for ebooks  
    Success: [Success][20]
-   Project: Business cards  
    Success: Not done  
    Description: Make some personal business cards
    
-   Project: QR Punchcodes  
    Success: Didn’t do  
    Description: So you know how QR codes can contain any data? That means you could show them to a camera and the camera could run any code. Like, code to wait for another couple of QR codes, or to print out some more QR codes…
    
-   \[Censored project involving an arbitrage opportunity I haven’t cornered\]
    
-   \[Censored project involving a mildly illegal thing\]
    
-   Project: Make a desk out of cardboard  
    Success: Ongoing  
    Description: I want to make a desk out of cardboard, because it sounds fun. I’m proud of doing the design right here. I’ve finished mocking it out of cardstock, and actually noticed a lot of flaws and fixed the design instead of hoping them away. Now I mostly have to get the cardboard and make it, should be fun.
    
-   Project: Make a whiteboard partition  
    Success: [Success][21]
    
-   Project: Write about paper backups  
    Success: [Success][22]
    
-   Project: Sort physical scans  
    Success: Success  
    Description: As part of packing up all my possessions to go to Vietnam, I scanned every physical document I own (and mostly threw them out). Twenty years of stuff is a lot of stuff, but I eventually sorted it all out. I’ve been increasingly finding that a flat folder structure ends up working out best for me in the long term, so that’s what I used.
    
-   Project: Two-location backup  
    Success: Not done  
    Description: My backup server uses RAID-1, but I’d like to have a second copy on an external hard drive somewhere.  Also, I have a bunch of external hard drives which are currently not backed up anywhere (mostly with stuff like movies) which I’d like to have some kind of redundancy
    
-   Project: Treemap finances  
    Success: Not done  
    Description: I’ve made my [finances public][23], but my analysis tools aren’t great. I’d like to update some old work I’ve done and add a web interface to see where I spent money during a particular time span, using a [treemap][24] display.
    
-   Project: Archive Github (aka download all the code in the world)  
    Success: Not done, on hold  
    Description: I’m kind of burnt out on archiving tasks lately, so this doesn’t sound fun to me. I decided to work with [archive team][25] on this one. It’ll get done if it sounds low-stress and no one else seems to be doing it, but it’s less likely than the older archiving projects, despite being important for the world.
    
-   Project: Encrypt backup  
    Success: Not done  
    Description: I’d like a way to back up my data to untrusted media, like tarsnap does, especially a way that avoids leaking file metadata (like access times and file lengths). Failing that, I should at least encrypt the drive backups are to so I can turn off that computer if needed.
    
-   Project: Gwernify  
    Success: Not done  
    Description: Gwern writes about how to [protect links][26] against link rot. He does this for all links on his website. I ambitiously plan to automatically save a copy of every site I visit (not just the actual URL I visit ideally, but the whole page).
    

[1]: http://www.jollybit.com/
[2]: http://thedragonseyelashes.tumblr.com/
[3]: http://sick-ghost.tumblr.com/
[4]: https://www.defcon.org/
[5]: https://intelligence.org/mirix/
[6]: http://burningman.org/
[7]: http://priceyak.com/
[8]: http://paulfchristiano.com/
[9]: https://github.com/WuTheFWasThat/vimflowy
[10]: http://za3k.com/colony.md
[11]: https://blog.za3k.com/backup-android-on-plugin/ "Backup android on plugin"
[12]: https://en.wikipedia.org/wiki/Media_Transfer_Protocol
[13]: mailto:za3k@za3k.com
[14]: https://blog.za3k.com/tag/backup/
[15]: http://arxiv.org/
[16]: https://blog.za3k.com/irc/ "IRC"
[17]: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html
[18]: https://blog.za3k.com/archiving-gmail/ "Archiving gmail"
[19]: https://xkcd.com/1360/
[20]: https://blog.za3k.com/the-double-lives-of-books/ "The Double Lives of Books"
[21]: https://blog.za3k.com/whiteboard-partition/ "Whiteboard Partition"
[22]: https://blog.za3k.com/paper-archival/ "Paper archival"
[23]: http://za3k.com/money.html
[24]: https://en.wikipedia.org/wiki/Treemapping
[25]: http://archiveteam.org/index.php?title=Main_Page
[26]: http://www.gwern.net/Archiving%20URLs
