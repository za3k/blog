---
author: admin
categories:
- Technical
date: 2014-10-04 02:10:39-07:00
markup: html
source: wordpress
tags:
- minecraft
title: Running a forge server on headless linux
updated: 2014-10-18 03:29:32-07:00
wordpress_id: 13
wordpress_slug: running-a-forge-server-on-headless-linux
---
I’ve had a lot of trouble getting Minecraft Forge to run headless. They have a friendly installer option that I just can’t use in my situation, but one of the devs seems actively hostile around providing help to headless servers, so I didn’t bother asking forge for help. I thought I’d write up what I had to do to get things working. As a warning, it requires some local work; you can’t do everything headless with these directions.

I’m running Minecraft 1.6.4, with the latest version of forge for that, 9.11.1.965.

1.  Locally, download and start the minecraft client for the correct version at least once. Not sure if you’ll need to ‘play online’ or not. If you have the current installer, you need to make a new profile with the correct minecraft version and play that.
2.  Copy ~/.minecraft/libraries to the headless machine.
3.  Download forge (the installer version, not the universal) from [http://files.minecraftforge.net/][1]. The non-adly version is the little star for non-interactive use.
4.  Run
    
    java -jar forge-1.6.4-9.11.1.965-installer.jar --installServer
    
5.  Delete the installer, you don’t need it any more.
6.  Install any mods you want to the ‘mods’ directory, edit server.properties, etc. Normal server setup.
7.  To execute the server, run the file indicated in the installer. In my case, I run
    
    java -jar minecraftforge-universal-1.6.4-9.11.1.965-v164-pregradle.jar nogui
    

Alternatively, you can install the entire server locally and copy it over.

1.  ![](https://secure.gravatar.com/avatar/eca9fbfd1236b50f30aec8f7b95ef721?s=40&d=mm&r=g)[Susan Tatun][2] says:
    
    [July 10, 2015 at 11:31 pm][3]
    
    An honest sharing about downloaing and installing Minecraft 1.6.4. I followed what you mentioned and did it sucessfully. Right now, I’m playing with my little son and guiding him what the terrific things are. Anyway, thanks a lot!
    
    [Reply][4]
    
2.  ![](https://secure.gravatar.com/avatar/f386723170dfc6b4122c5fe2d95ffbbc?s=40&d=mm&r=g)Lynx says:
    
    [August 18, 2015 at 1:44 am][5]
    
    4am installs of servers is hard, and trying to follow the Forge wiki which is inaccurate at best is hard.  
    You got me from dead brick to running box in ten minutes. Thank you.
    
    [Reply][6]
    
3.  ![](https://secure.gravatar.com/avatar/746c2f840c27e88b6bfc135f14f4ce37?s=40&d=mm&r=g)crumpuppet says:
    
    [September 7, 2015 at 1:32 pm][7]
    
    Thanks so much! I’ve been looking for these steps for a while, and finally found something that works. Would have been first prize if it could be used along with a GUI frontend like mcmyadmin, but oh well 🙂
    
    [Reply][8]
    
4.  ![](https://secure.gravatar.com/avatar/48ef5c93bf1c483b50dd6b7977b9cbca?s=40&d=mm&r=g)Dave says:
    
    [November 9, 2015 at 11:14 am][9]
    
    Same here. Searched all over found yours and running in moments. My kids have been hooked on mods and wanted a server. I have VMware and can spin up a linux box up in moments. This was so easy. Thanks.
    
    [Reply][10]
    
5.  ![](https://secure.gravatar.com/avatar/8cc161f40686089efa4eb9dbc381797a?s=40&d=mm&r=g)[Minecraft Lover][11] says:
    
    [February 6, 2019 at 6:40 am][12]
    
    Very useful information, Thank you
    
    [Reply][13]
    
6.  ![](https://secure.gravatar.com/avatar/4589e18b3dc7de6c60e1b99052acfe1d?s=40&d=mm&r=g)Leon says:
    
    [September 9, 2019 at 9:12 am][14]
    
    Does anyone here have problems with installing the mods. Im donwloading them in the mods directory with the cmd “wget” and nothing works.Am i using the wrong command or what?
    
    [Reply][15]
    
7.  ![](https://secure.gravatar.com/avatar/b50d1a265153eee6da6b41d6adc0eb06?s=40&d=mm&r=g)[Rajan Chopra][16] says:
    
    [March 7, 2020 at 3:45 pm][17]
    
    Thanks for sharing Minecraft. Can you also share Roblox Apk?
    
    [Reply][18]
    
8.  ![](https://secure.gravatar.com/avatar/52ce2f57adc4ccfc3e6274ffa86bf9f5?s=40&d=mm&r=g)Neckbeard Hater says:
    
    [January 4, 2021 at 10:22 pm][19]
    
    “one of the devs seems actively hostile around providing help to …”
    
    this is so typical of the linux community. really. And I am a developer with 20 years experience, I hate the Linux community.
    
    [Reply][20]
    
9.  ![](https://secure.gravatar.com/avatar/cca172695c7bd7d417748775c1ad3c36?s=40&d=mm&r=g)nat says:
    
    [February 14, 2023 at 9:17 am][21]
    
    lol this tutorial still works 9 years later thanks tho this helped so much!!
    
    [Reply][22]
    

[1]: http://files.minecraftforge.net/
[2]: https://2dminecraft.wordpress.com/
[3]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-511
[4]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=511#respond
[5]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-1349
[6]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=1349#respond
[7]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-1689
[8]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=1689#respond
[9]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-2468
[10]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=2468#respond
[11]: https://minecraftapkmod.info/download/
[12]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-3252
[13]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=3252#respond
[14]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-3788
[15]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=3788#respond
[16]: https://apkstreet.com/roblox-mod-apk-unlimited-robux/
[17]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-3991
[18]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=3991#respond
[19]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-4324
[20]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=4324#respond
[21]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/#comment-9669
[22]: https://blog.za3k.com/running-a-forge-server-on-headless-linux/?replytocom=9669#respond
