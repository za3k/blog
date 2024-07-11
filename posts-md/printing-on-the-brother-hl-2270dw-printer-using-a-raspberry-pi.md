---
author: admin
categories:
- Technical
date: 2020-04-18 16:47:39-07:00
markup: html
source: wordpress
tags:
- linux
- printer
- raspberry pi
title: Printing on the Brother HL-2270DW printer using a Raspberry Pi
updated: 2020-12-12 13:29:42-07:00
wordpress_id: 517
wordpress_slug: printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi
---
Although the below directions work on Raspberry Pi, they should also work on any other system. The brother-provided driver does not run on arm processors\[1\] like the raspberry pi, so we will instead use the open-source [brlaser][1]\[2\].

Edit: This setup should also work on the following Brother monochrome printers, just substitute the name where needed:

-   brlaser 4, just install from package manager: DCP-1510, DCP-1600 series, DCP-7030, DCP-7040, DCP-7055, DCP-7055W, DCP-7060D, DCP-7065DN, DCP-7080, DCP-L2500D series, HL-1110 series, HL-1200 series, HL-L2300D series, HL-L2320D series, HL-L2340D series, HL-L2360D series, HL-L2375DW series, HL-L2390DW, MFC-1910W, MFC-7240, MFC-7360N, MFC-7365DN, MFC-7420, MFC-7460DN, MFC-7840W, MFC-L2710DW series
-   brlaser 6, follow full steps below: DCP-L2520D series, DCP-L2520DW series, DCP-L2540DW series (unclear, may only need 4), HL-2030 series, HL-2140 series, HL-2220 series, HL-2270DW series, HL-5030 series

Also, all these steps are command-line based, and you can do the whole setup headless (no monitor or keyboard) using SSH.

1.  Get the latest raspbian image up and running on your pi, with working networking. At the time of writing the latest version is 10 (buster)–once 11+ is released this will be much easier. I have written a [convenience tool][2]\[3\] for this step, but you can also find any number of standard guides. Log into your raspberry pi to run the following steps
2.  (Option 1, not recommended) Upgrade to Debian 11 bullseye (current testing release). This is because we need brlaser 6, not brlaser 4 from debian 10 buster (current stable release). Then, install the print system and driver\[2\]:  
    `sudo apt-get update && sudo apt-get install lpr cups ghostscript printer-driver-brlaser`
3.  (Option 2, recommended) Install ‘brlaser’ from source.
    1.  Install print system and build tools  
        `sudo apt-get update && sudo apt-get install lpr cups ghostscript git cmake libcups2-dev libcupsimage2-dev`
    2.  Download the source  
        `wget https://github.com/pdewacht/brlaser/archive/v6.tar.gz && tar xf v6.tar.gz`
    3.  Build the source and install  
        `cd brlaser-6 && cmake . && make` && `sudo make install`
4.  Plug in the printer, verify that it shows up using `sudo lsusb` or `sudo dmesg`. (author’s shameful note: if you’re not looking, I find it surprisingly easy to plug USB B into the ethernet jack)
5.  Install the printer.
    1.  Run `sudo lpinfo -v | grep usb` to get the device name of your printer. It will be something like `usb://Brother/HL-2270DW%20series?serial=D4N207646`  
        If you’re following this in the hopes that it will work on another printer, run `sudo lpinfo -m | grep HL-2270DW` to get the PPD file for your printer.
    2.  Install and enable the printer  
        `sudo lpadmin -p HL-2270DW -E -v usb://Brother/HL-2270DW%20series?serial=D4N207646 -m drv:///brlaser.drv/br2270dw.ppd`  
        Note, `-p HL-2270DW` is just the name I’m using for the printer, feel free to name the printer whatever you like.
    3.  Enable the printer (did not work for me)  
        `sudo lpadmin -p HL-2270DW -E`
    4.  (Optional) Set the printer as the default destination  
        `sudo lpoptions -d HL-2270DW`
    5.  (Optional) Set any default options you want for the printer  
        `sudo lpoptions -p HL-2270DW -o media=letter`
6.  Test the printer (I’m in the USA so we use ‘letter’ size paper, you can substitute whichever paper you have such as ‘a4’).
    1.  `echo "Hello World" | PRINTER=HL-2270DW lp -o media=letter` (Make sure anything prints)
    2.  `cat <test document> | PRINTER=HL-2270DW lp -o media=letter` (Print an actual test page to test alignment, etc)
    3.  `cat <test document> | PRINTER=HL-2270DW lp -o media=letter -o sides=two-sided-short-edge` (Make sure duplex works if you plan to use that)
7.  (Optional) Set up an [scp print server][3], so any file you copy to a `/printme` directory gets printed. For the 2270DW, I also have a `/printme.duplex` directory.

Links  
\[1\] brother driver [does not work][4] on arm (also verified myself)  
\[2\] [brlaser][5], the open-source Brother printer driver  
\[3\] [rpi-setup][6], my convenience command-line script for headless raspberry pi setup  
\[4\] [stack overflow answer][7] on how to install one package from testing in debian

1.  ![](https://secure.gravatar.com/avatar/bc00b207944738af582a91c5352ef163?s=40&d=mm&r=g)Joel says:
    
    [August 2, 2020 at 12:52 pm][8]
    
    There appears to be a typo in step 5A. The page currently reads “lpinfo -m” but I believe should be “lpinfo -v”. Per the man page, the m flag lists drivers and the v flag lists devices.
    
    The USB device can be found in the -v output for step 5A but the driver can be found in the -m output for step 5B.
    
    [Reply][9]
    
2.  ![](https://secure.gravatar.com/avatar/b99febd9d3367d3306947a8e159c6445?s=40&d=mm&r=g)Scott says:
    
    [October 19, 2020 at 5:10 pm][10]
    
    Thank you so very much for this. Worked like a charm.
    
    Any tips on how to print over the network?
    
    [Reply][11]
    
3.  ![](https://secure.gravatar.com/avatar/dffffda5bcb146c22d8be3ef6b4f6554?s=40&d=mm&r=g)rathesun01 says:
    
    [December 8, 2020 at 6:44 pm][12]
    
    Awesome post. Joel is supposedly correct. It should have been “lpinfo -v” in the step 5A.
    
    [Reply][13]
    
4.  ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
    
    [December 12, 2020 at 1:31 pm][14]
    
    Corrected ‘lpinfo -v’, thanks.  
    No clue how to print over the network, sorry. That’s actually why I set up a raspberry pi to connect to the printer instead–it’s my wifi interface.  
    
    [Reply][15]
    
5.  ![](https://secure.gravatar.com/avatar/b851d521102349bbfd71e7d7df8bef44?s=40&d=mm&r=g)steve says:
    
    [December 30, 2020 at 9:05 am][16]
    
    I have the Brother HL-2270DW, and I had to install from source to get it to work. I’m not using USB, but port forwarding across via NAT to another internal network.
    
    I just used the cups admin pages to complete setting things up. Before using this package, I picked some other closely related printer. It was printing the page, sucking it back in, then finally printing. Not terrible, but I was annoyed. Now it’s perfect!
    
    For printing over the network, I used the socket::9100 setting. No idea the command line knobs or dials, just did it through the cups web page.
    
    Another reason for me to do this is now my little rasperry pi zero w shows my printer as an AirPrint printer, so now I can print from my iDevices. Brother has their own app for this printer, but I was annoyed having to install a special app for this. My HL2270DW was made without AirPrint. It’s a fine little machine and don’t want to throw it out.
    
    [Reply][17]
    
    -   ![](https://secure.gravatar.com/avatar/1edcef9b0ab9150a7e2d22cd18371609?s=40&d=mm&r=g)Jaye Horn says:
        
        [February 18, 2021 at 3:19 pm][18]
        
        How did you install from source? and how did you do the port forwarding across via NAT to another internal network? I’m new to this so any help would be very much appreciated.
        
        Thank you.
        
        [Reply][19]
        
6.  ![](https://secure.gravatar.com/avatar/173de507afbda1d5933757bb66e863eb?s=40&d=mm&r=g)Job says:
    
    [January 20, 2021 at 8:09 pm][20]
    
    Would this work for brother hl-l2395dw scanner?
    
    [Reply][21]
    
7.  ![](https://secure.gravatar.com/avatar/285bae3dce12d6c20103a5ff2a4bcddb?s=40&d=mm&r=g)Adam Trask says:
    
    [October 22, 2021 at 5:00 am][22]
    
    Thanks so much for posting this. This helped get my HL-L2300D working properly.
    
    [Reply][23]
    
8.  ![](https://secure.gravatar.com/avatar/76652e498c8089550fa09056625d5899?s=40&d=mm&r=g)Danial Foster says:
    
    [December 24, 2021 at 1:39 am][24]
    
    \>>> (author’s shameful note: if you’re not looking, I find it  
    \>>>surprisingly easy to plug USB B into the ethernet jack)  
    
    I smiled when I saw this because you are clearly a ding dong; that sounds like a rookie mistake.
    
    I couldn’t get your instructions to work, so I tried troubleshooting through Google. Couldn’t figure it out. sudo lpinfo -v | grep usb wasn’t showing jack.
    
    It was because I had my USB B plugged into the ethernet jack of my BR-2270DW.
    
    Everything works now. Thank you so much.
    
    [Reply][25]
    
9.  ![](https://secure.gravatar.com/avatar/fe520de38df86000b2d31661c96cd28a?s=40&d=mm&r=g)J Bot says:
    
    [January 3, 2023 at 4:03 pm][26]
    
    Any steps to do this with a wifi connected HL-2270DW? Thanks!
    
    [Reply][27]
    

[1]: https://github.com/pdewacht/brlaser
[2]: https://github.com/za3k/rpi-setup
[3]: https://blog.za3k.com/linux-print-server/
[4]: https://www.raspberrypi.org/forums/viewtopic.php?t=15526
[5]: https://github.com/pdewacht/brlaser
[6]: https://github.com/za3k/rpi-setup
[7]: https://serverfault.com/questions/22414/how-can-i-run-debian-stable-but-install-some-packages-from-testing
[8]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4165
[9]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4165#respond
[10]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4213
[11]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4213#respond
[12]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4277
[13]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4277#respond
[14]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4279
[15]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4279#respond
[16]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4319
[17]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4319#respond
[18]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4380
[19]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4380#respond
[20]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-4341
[21]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=4341#respond
[22]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-5178
[23]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=5178#respond
[24]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-5438
[25]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=5438#respond
[26]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/#comment-9429
[27]: https://blog.za3k.com/printing-on-the-brother-hl-2270dw-printer-using-a-raspberry-pi/?replytocom=9429#respond
