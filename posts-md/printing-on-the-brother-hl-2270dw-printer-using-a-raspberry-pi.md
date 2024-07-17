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
Although the below directions work on Raspberry Pi, they should also work on any other system. The brother-provided driver does not run on arm processors\[1\] like the raspberry pi, so we will instead use the open-source [brlaser](https://github.com/pdewacht/brlaser)\[2\].

Edit: This setup should also work on the following Brother monochrome printers, just substitute the name where needed:

-   brlaser 4, just install from package manager: DCP-1510, DCP-1600 series, DCP-7030, DCP-7040, DCP-7055, DCP-7055W, DCP-7060D, DCP-7065DN, DCP-7080, DCP-L2500D series, HL-1110 series, HL-1200 series, HL-L2300D series, HL-L2320D series, HL-L2340D series, HL-L2360D series, HL-L2375DW series, HL-L2390DW, MFC-1910W, MFC-7240, MFC-7360N, MFC-7365DN, MFC-7420, MFC-7460DN, MFC-7840W, MFC-L2710DW series
-   brlaser 6, follow full steps below: DCP-L2520D series, DCP-L2520DW series, DCP-L2540DW series (unclear, may only need 4), HL-2030 series, HL-2140 series, HL-2220 series, HL-2270DW series, HL-5030 series

Also, all these steps are command-line based, and you can do the whole setup headless (no monitor or keyboard) using SSH.

1.  Get the latest raspbian image up and running on your pi, with working networking. At the time of writing the latest version is 10 (buster)–once 11+ is released this will be much easier. I have written a [convenience tool](https://github.com/za3k/rpi-setup)\[3\] for this step, but you can also find any number of standard guides. Log into your raspberry pi to run the following steps
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
7.  (Optional) Set up an [scp print server](https://blog.za3k.com/linux-print-server/), so any file you copy to a `/printme` directory gets printed. For the 2270DW, I also have a `/printme.duplex` directory.

Links  
\[1\] brother driver [does not work](https://www.raspberrypi.org/forums/viewtopic.php?t=15526) on arm (also verified myself)  
\[2\] [brlaser](https://github.com/pdewacht/brlaser), the open-source Brother printer driver  
\[3\] [rpi-setup](https://github.com/za3k/rpi-setup), my convenience command-line script for headless raspberry pi setup  
\[4\] [stack overflow answer](https://serverfault.com/questions/22414/how-can-i-run-debian-stable-but-install-some-packages-from-testing) on how to install one package from testing in debian
