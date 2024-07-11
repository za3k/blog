---
author: admin
categories:
- Technical
date: 2021-05-31 19:41:26-07:00
markup: html
source: wordpress
tags:
- announcements
- backup
- papercrafts
- qr
title: qr-backup
updated: 2021-06-05 15:39:22-07:00
wordpress_id: 587
wordpress_slug: qr-backup
---
I made a new project called [qr-backup][1]. It’s a command-line program to back up any file to physical paper, using a number of QR codes. You can then restore it, even WITHOUT the qr-backup program, using the provided instructions.

[![](https://blog.za3k.com/wp-content/uploads/2021/05/example.png)][2]

I’m fairly satisfied with its current state (can actually back up my files, makes a PDF). There’s definitely some future features I’m looking forward to adding, though.

1.  ![](https://secure.gravatar.com/avatar/d8731f49a2e6864ba0675c4639ef08be?s=40&d=mm&r=g)[scruss][3] says:
    
    [June 9, 2021 at 6:58 am][4]
    
    nice! I’ve played with some similar ideas, using tar and QR Code output to a thermal printer. The used to be a thing (Twibright Optar, IIRC: it’s fallen off the web) that made full-page scannable codes that got an almost useful data density. But they weren’t QR Codes, so needed their own decoder.
    
    [Reply][5]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [June 9, 2021 at 2:06 pm][6]
        
        Actually, I link to it in the [FAQ][7], it’s still on the [web][8]. An even better version was “Paperback”, but it’s 9 years unmaintained–I’m looking into seeing if there is a maintained Linux port. Both do a lot of things right, even if they have a slightly different goal (high data density, over ease-of-use and foolproof restore).
        
        [Reply][9]
        
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [June 9, 2021 at 2:08 pm][10]
        
        Also, feel free to recommend me a good, cheap thermal printer. I tried to do a “poloroid” thing (take a picture of yourself with webcam, immediately print to thermal) and found that mine was shit and the heat overexposed unrelated parts. QR codes seem like a reasonable application, although I’d be concerned about the longevity of thermal paper for backups (can easily fade in heat).
        
        Edit: If I remember correctly, I wanted to make a thermal-paper typewriter for a zine?
        
        [Reply][11]
        

[1]: https://github.com/za3k/qr-backup
[2]: https://blog.za3k.com/wp-content/uploads/2021/05/example.png
[3]: https://scruss.com/blog/
[4]: https://blog.za3k.com/qr-backup/#comment-4642
[5]: https://blog.za3k.com/qr-backup/?replytocom=4642#respond
[6]: https://blog.za3k.com/qr-backup/#comment-4644
[7]: https://github.com/za3k/qr-backup/blob/master/docs/FAQ.md#what-other-paper-backup-projects-exist
[8]: http://ronja.twibright.com/optar/
[9]: https://blog.za3k.com/qr-backup/?replytocom=4644#respond
[10]: https://blog.za3k.com/qr-backup/#comment-4645
[11]: https://blog.za3k.com/qr-backup/?replytocom=4645#respond
