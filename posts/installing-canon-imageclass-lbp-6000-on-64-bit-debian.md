---
author: admin
categories:
- Technical
date: 2015-10-05 01:44:36-07:00
has-comments: false
source: wordpress
tags:
- command-line
- install
- linux
- printer
title: Installing Canon imageClass LBP-6000 on 64-bit Debian
updated: 2015-10-17 19:27:12-07:00
wordpress_id: 263
wordpress_slug: installing-canon-imageclass-lbp-6000-on-64-bit-debian
---
(From [Stack Overflow](http://askubuntu.com/questions/463289/cant-get-my-canon-lbp-printer-to-run-under-ubuntu-14-04/464334))

1.  64 bit requirements for pre-made binaries:
    
    ```
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install libstdc++6:i386 libxml2:i386 zlib1g:i386 libpopt0:i386
    ```
    
2.  Install CUPS
    
    ```
    sudo apt-get update
    sudo apt-get install cups
    ```
    
3.  Download DriverGo to [http://support-au.canon.com.au/contents/AU/EN/0100459602.html](http://support-au.canon.com.au/contents/AU/EN/0100459602.html) and download driver
    
    ```
    64e2d00f0c8764d4032687d29e88f06727d88825 Linux_CAPT_PrinterDriver_V270_uk_EN.tar.gz
    ```
    
4.  Extract and enter extracted folder
    
    ```
    tar xf Linux_CAPT_PrinterDriver_V270_uk_EN.tar.gz
    cd Linux_CAPT_PrinterDriver_V270_uk_EN
    ```
    
5.  Install the custom drivers and ccpd
    
    ```
    sudo dpkg -i 64-bit_Driver/Debian/*.deb
    ```
    
6.  Add the printer to CUPS and ccpd
    
    ```
    sudo lpadmin -p CANON_LBP6000 -m CNCUPSLBP6018CAPTS.ppd -v ccp://localhost:59687
    sudo lpadmin -p CANON_LBP6000 -E
    
    sudo ccpdadmin -p CANON_LBP6000 -o /dev/usb/lp0
    ```
    
7.  Set the default printer
    
    ```
    sudo lpoptions -d CANON_LBP6000
    ```
    
8.  Set ccpd to start on boot
    
    ```
    sudo update-rc.d ccpd defaults
    ```
